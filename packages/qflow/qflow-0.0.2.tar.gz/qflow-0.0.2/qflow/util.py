import datetime
import functools
import platform
import time
import urllib.error
import urllib.request

from typing import Union


class DateFormatError(Exception):
  pass


def to_datetime(timestamp: Union[datetime.datetime, datetime.date, int]) \
    -> datetime.datetime:
  if isinstance(timestamp, int):
    return datetime.datetime.utcfromtimestamp(timestamp / 10.**9)
  elif isinstance(timestamp, datetime.datetime):
    return timestamp
  elif isinstance(timestamp, datetime.date):
    return datetime.datetime(timestamp.year, timestamp.month, timestamp.day)
  else:
    raise ValueError()


def to_timestamp_int(timestamp: Union[int, datetime.datetime, datetime.date]):
  if isinstance(timestamp, int):
    return timestamp
  elif isinstance(timestamp, datetime.datetime):
    return nanoseconds_from_epoch(timestamp)
  elif isinstance(timestamp, datetime.date):
    timestamp = datetime.datetime(
        timestamp.year, timestamp.month, timestamp.day)
    return nanoseconds_from_epoch(timestamp)
  else:
    raise ValueError()


def nanoseconds_from_epoch(datetime_in: datetime.datetime) -> int:
  if not isinstance(datetime_in, datetime.datetime):
    raise TypeError()
  td = datetime_in - datetime.datetime.fromtimestamp(0, datetime_in.tzinfo)
  seconds = td.seconds + td.days * 24 * 3600
  nanoseconds = td.microseconds * 10 ** 3 + seconds * 10 ** 9
  # 0x7fffffffffffffff is year 2262.
  if not 0x7fffffffffffffff >= nanoseconds >= -0x8000000000000000:
    raise OverflowError(
        '0x%x is out of range (min_int64, max_int64)' % nanoseconds)
  return nanoseconds


def parse_end_time(end_time_string=None, now=None, margin=None):
  if end_time_string is None:
    return None
  splitted = end_time_string.split(':')
  assert len(splitted) == 3 or len(splitted) == 2
  now = now or datetime.datetime.now()
  margin = margin or datetime.timedelta(minutes=10)
  end_time = now.replace(hour=int(splitted[0]), minute=int(splitted[1]),
                         second=int(0 if len(splitted) == 2 else splitted[2]),
                         microsecond=0)
  if now + margin >= end_time:
    end_time += datetime.timedelta(days=1)
    assert now < end_time
  return end_time


def convert_string_to_dates(date_specifier):
  if not isinstance(date_specifier, str):
    raise DateFormatError('Invalid data type: %s'  % type(date_specifier))

  res = []
  date_chunks = date_specifier.split(',')
  for date_chunk in date_chunks:
    date_pair = date_chunk.strip().split('-')
    if len(date_pair) == 1:
      if len(date_pair[0]) != 8:
        raise DateFormatError("Wrong date format: %s" % date_chunk)
      year = int(date_pair[0][:4])
      month = int(date_pair[0][4:6])
      day = int(date_pair[0][6:8])
      begin_date = datetime.date(year, month, day)
      end_date = datetime.date(year, month, day)
    elif len(date_pair) == 2:
      if len(date_pair[0]) != 8 or len(date_pair[1]) != 8:
        raise DateFormatError("Wrong date format: %s" % date_chunk)
      begin_date = datetime.date(
          int(date_pair[0][:4]),
          int(date_pair[0][4:6]),
          int(date_pair[0][6:8]))
      end_date = datetime.date(
          int(date_pair[1][:4]),
          int(date_pair[1][4:6]),
          int(date_pair[1][6:8]))
    else:
      raise DateFormatError("Wrong date format: %s" % date_chunk)
    add_delta = datetime.timedelta(days=1)
    while begin_date <= end_date:
      res.append(begin_date)
      begin_date += add_delta
  return res


def iterate_date(start_date: datetime.date,
                 end_date: datetime.date,
                 reverse=False):
  cur_date = start_date
  if reverse:
    while cur_date > end_date:
      yield cur_date
      cur_date -= datetime.timedelta(days=1)
  else:
    while cur_date < end_date:
      yield cur_date
      cur_date += datetime.timedelta(days=1)


def get_timestamp():
  return int(time.time() * 1e9)


@functools.lru_cache(maxsize=1)
def query_ec2_region():
  try:
    zone_url = ('http://169.254.169.254/latest/meta-data/placement/'
                'availability-zone')
    with urllib.request.urlopen(zone_url) as f:
      return f.read().decode('ascii').strip()
  except urllib.error.HTTPError:
    raise ValueError()


@functools.lru_cache(maxsize=1)
def get_hostname():
  return platform.node()


@functools.lru_cache(maxsize=1)
def get_region_or_fqdn():
  try:
    return query_ec2_region()
  except ValueError:
    return get_hostname()


def main():
  print(get_hostname())
  print(get_region_or_fqdn())


if __name__ == '__main__':
  main()
