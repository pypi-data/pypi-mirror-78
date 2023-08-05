import fnmatch
from typing import Dict, List, Optional, Tuple, Union

from .default_topic_map import topic_id_to_string_map as default_topic_id_to_string_map
from .topic_map_util import check_topic_id_to_string_map


class TopicMap(object):
  def __init__(
      self,
      topic_id_to_string_map: Union[Dict[int, str], List[Tuple[int, str]]]):
    self._topic_id_to_string_map = \
        dict(check_topic_id_to_string_map(topic_id_to_string_map))
    self._topic_string_to_id_map = {
        topic_string: topic_id
        for topic_id, topic_string in self._topic_id_to_string_map.items()}

  @property
  def topic_id_to_string_map(self) -> Dict[int, str]:
    return self._topic_id_to_string_map

  @property
  def topic_string_to_id_map(self) -> Dict[str, int]:
    return self._topic_string_to_id_map

  def search_topic_string(self, topic_id: int) -> str:
    try:
      return self._topic_id_to_string_map[topic_id]
    except KeyError:
      return '0x%016x' % topic_id

  def search_topic_id(self, topic_string_pattern: Union[int, str]) \
      -> List[Tuple[str, int]]:
    if isinstance(topic_string_pattern, int):
      topic_string_pattern = '0x%016X' % topic_string_pattern

    if (topic_string_pattern.startswith('0x') and
        len(topic_string_pattern) == 18):
      try:
        topic_id = int(topic_string_pattern[2:], 16)
      except ValueError:  # Invalid topic_id hex string
        return []
      topic_string = self.search_topic_string(topic_id)
      return [(topic_string, topic_id)]

    ret = []
    for topic_string, topic_id in self._topic_string_to_id_map.items():
      if fnmatch.fnmatch(topic_string, topic_string_pattern):
        ret.append((topic_string, topic_id))
    return sorted(ret)


_DEFAULT_TOPIC_MAP = TopicMap(default_topic_id_to_string_map)


def set_default_topic_map(topic_map):
  global _DEFAULT_TOPIC_MAP
  if isinstance(topic_map, (dict, list)):
    _DEFAULT_TOPIC_MAP = TopicMap(topic_map)
  else:
    _DEFAULT_TOPIC_MAP = topic_map


def get_default_topic_map():
  return _DEFAULT_TOPIC_MAP


def search_topic_string(topic_id: int) -> str:
  return get_default_topic_map().search_topic_string(topic_id)


def search_topic_id(topic_string_pattern: Union[int, str]) \
    -> List[Tuple[str, int]]:
  return get_default_topic_map().search_topic_id(topic_string_pattern)
