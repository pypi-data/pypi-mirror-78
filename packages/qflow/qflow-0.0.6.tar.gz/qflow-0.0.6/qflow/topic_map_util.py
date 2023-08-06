from typing import Dict, List, Tuple, Union


def get_worker_id(topic_id):
  return str(topic_id % 0x10 + 1)


def expand_worker(base_topic_id, topic_string_prefix, num_worker):
  assert num_worker <= 16
  table = []
  for worker_idx in range(num_worker):
    worker_id = str(worker_idx + 1)
    topic_string = '%s%s' % (topic_string_prefix, worker_id)
    topic_id = base_topic_id + worker_idx
    table.append((topic_id, topic_string))
  return table


def expand_group_worker(base_topic_id, topic_string_prefix, num_group,
                        num_worker):
  assert num_group <= 16 and num_worker <= 16
  table = []
  for group_idx in range(num_group):
    for worker_idx in range(num_worker):
      group_id = chr(ord('a') + group_idx)
      worker_id = str(worker_idx + 1)
      topic_string = '%s%s%s' % (topic_string_prefix, group_id, worker_id)
      topic_id = base_topic_id + group_idx * 0x10 + worker_idx
      table.append((topic_id, topic_string))
  return table


def expand_list(target_list):
  res = []
  for elem in target_list:
    if isinstance(elem, list):
      res += elem
    else:
      res.append(elem)
  return res


def _explode_int64(value):
  c = []
  for i in range(8):
    c.append((value >> (8 * i)) & 0xFF)
  return c


def topic_id_to_multicast_addr(topic_id, strip=True):
  c = _explode_int64(topic_id)
  if c[6] != 0 or c[7] != 0:
    raise ValueError('topic_id=0x%016X cannot be converted to multicast address'
                     % topic_id)
  port = c[1] * 255 + c[0]
  ip_addr_str = '%d.%d.%d.%d:%d' % (c[5], c[4], c[3], c[2], port)
  if strip:
    return ip_addr_str
  else:
    return '%21s' % ip_addr_str


def check_topic_id_to_string_map(
    topic_id_to_string_map: Union[Dict[int, str], List[Tuple[int, str]]],
    check_topic_id_multicastable=False):
  if isinstance(topic_id_to_string_map, dict):
    topic_id_to_string_map = topic_id_to_string_map.items()

  # NOTE: We assume topic_string and topic_id are mapped 1 to 1, for now.
  topic_id_set = set()
  topic_string_set = set()

  for topic_id, topic_string in topic_id_to_string_map:
    if topic_id in topic_id_set:
      raise ValueError('duplicated topic_id: 0x%016X' % topic_id)
    topic_id_set.add(topic_id)

    if topic_string in topic_string_set:
      raise ValueError('duplicated topic_string: %s' % topic_string)
    topic_string_set.add(topic_string)

    if topic_string.startswith('0x'):
      raise ValueError('topic string cannot start with "0x"')

    if check_topic_id_multicastable:
      c = _explode_int64(topic_id)
      if c[6] != 0 or c[7] != 0:
        raise ValueError('First two significant bytes are reserved: 0x%016X'
                         % topic_id)

      if c[5] != 237:
        raise ValueError('Use 237.x.x.x: 0x%016X' % topic_id)

      port = c[1] * 255 + c[0]
      if port < 1024:
        raise ValueError('Do not use port under 1024: 0x%016X' % topic_id)

  assert len(topic_id_set) == len(topic_string_set)
  return topic_id_to_string_map
