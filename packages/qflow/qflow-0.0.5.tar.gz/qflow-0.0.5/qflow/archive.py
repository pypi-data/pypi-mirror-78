import collections
import datetime
import fnmatch
import functools
import json
import logging
import os
from typing import Dict, List, Optional, Union

from .reader import Reader, TimestampMergeReader
from .util import (
    nanoseconds_from_epoch,
    to_datetime,
    get_hostname)
from .archive_backend import (
    get_archive_backend_type,
    get_archive_backend)
from .topic_map import get_default_topic_map
from .topic_record import (
    CrcRecordError,
    TopicRecordReaderError,
    TopicRecordCompressionType,
    TopicRecord,
    TopicRecordReader,
    TopicRecordWriter)


INT64MIN = -9223372036854775808
INT64MAX = 9223372036854775807

default_archive_root_dir = '~/data/flow'
logger_name = 'qflow'
print(__package__)


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


def to_date_str(date: Union[datetime.date, datetime.datetime, str]):
  if isinstance(date, str):
    return date
  elif isinstance(date, (datetime.date, datetime.datetime)):
    return date.strftime('%Y%m%d')
  else:
    raise ValueError()


def to_list(x):
  if isinstance(x, list):
    return x
  return [x]


# Take only filepath as a cache key
@functools.lru_cache(maxsize=65536)
def get_first_timestamp(filepath, archive_backend=None, max_try=100):
  archive_backend = archive_backend or get_archive_backend(filepath)
  with TopicRecordReader(filepath, archive_backend=archive_backend) as reader:
    for try_count in range(0, max_try):
      try:
        record = reader.peek()
        if record is None:
          raise EOFError()
        return record.timestamp
      except CrcRecordError:
        continue  # Skip a corrupted record.
    raise TopicRecordReaderError()


def decompose_archive_filename(filename):
  # <topic_string>.<queue_name>.<archive timestamp> (.gz)
  if filename.endswith('.gz'):
    filename = filename[:-3]

  sep_idx_1 = filename.rfind('.')
  if sep_idx_1 == -1:
    raise ValueError()
  queue_time_str = filename[sep_idx_1 + 1:]
  # timezone UTC
  queue_time = datetime.datetime.strptime(queue_time_str, '%Y%m%d-%H%M%SZ')

  sep_idx_2 = filename.rfind('.', 0, sep_idx_1)
  if sep_idx_2 == -1:
    raise ValueError()

  queue_name = filename[sep_idx_2 + 1:sep_idx_1]
  topic_string = filename[0:sep_idx_2]
  return topic_string, queue_name, queue_time


def query_machine_archive_file(
    machine: str,
    archive_date: Union[datetime.date, str],
    queue_name: Union[str, List[str], None]=None,
    topic_string: Union[str, int, List[Union[str, int]], None]=None,
    root_dir: Optional[str]=None,
    archive_backend=None,
    logger=None):
  logger = logger or logging.getLogger(logger_name)

  # Find and return archive file list with a specific machine and archive_date.
  archive_backend = archive_backend or \
                    get_archive_backend(root_dir or default_archive_root_dir)
  root_dir = archive_backend.normpath(root_dir or default_archive_root_dir)
  archive_date = to_date_str(archive_date)
  queue_name_list = to_list(queue_name or '*')
  topic_string_list = to_list(topic_string or '*')

  archive_path = os.path.join(root_dir, machine, archive_date)

  files = []
  for filepath in archive_backend.iter_file(archive_path):
    filename = os.path.basename(filepath)
    if filename.startswith('.'):
      continue

    try:
      topic_string, queue_name, _ = \
          decompose_archive_filename(filename)
    except ValueError:
      logger.warning('Invalid filename format: %s' % filepath)
      # Skip the file
      continue

    for pattern in queue_name_list:
      if fnmatch.fnmatch(queue_name, pattern):
        break
    else:
      continue

    for pattern in topic_string_list:
      if isinstance(pattern, int):
        pattern = '0x%016d' % pattern
      if fnmatch.fnmatch(topic_string, pattern):
        break
    else:
      continue

    try:
      get_first_timestamp(filepath, archive_backend=archive_backend)
    except (TopicRecordReaderError, EOFError):
      logger.warning('File %s seems corrupted, skipped.' % filepath)
      continue

    # Matched.
    files.append(filepath)

  return sorted(files)


def query_archive_file(
    machine: Union[str, List[str], None],
    archive_date: Union[datetime.date, str],
    queue_name: Union[str, List[str], None]=None,
    topic_string: Union[str, int, List[Union[str, int]], None]=None,
    root_dir: Optional[str]=None,
    archive_backend=None):
  archive_backend = archive_backend or \
                    get_archive_backend(root_dir or default_archive_root_dir)
  root_dir = archive_backend.normpath(root_dir or default_archive_root_dir)

  machine_patterns = to_list(machine or '*')

  machine_list = []
  for dirpath in archive_backend.iter_dir(root_dir):
    if dirpath.endswith('/'):
      dirpath = dirpath[:-1]
    machine = os.path.basename(dirpath)
    for pattern in machine_patterns:
      if fnmatch.fnmatch(machine, pattern):
        machine_list.append(machine)
        break

  files = []
  for machine in machine_list:
    files += query_machine_archive_file(
        machine, archive_date, queue_name, topic_string, root_dir,
        archive_backend=archive_backend)
  return sorted(files)


def sort_archive_file_in_timestamp(files, skip_error=True, archive_backend=None,
                                   logger=None):
  logger = logger or logging.getLogger(logger_name)
  selected = []
  for fp in to_list(files):
    try:
      selected.append(
          (get_first_timestamp(fp, archive_backend=archive_backend), fp))
    except (EOFError, TopicRecordReaderError):
      logger.warning('File %s seems corrupted.' % fp)
      if not skip_error:
        raise
      continue
  return [filepath for _, filepath in sorted(selected)]


def iter_archive_file(
    from_timestamp: Union[int, datetime.datetime, datetime.date],
    machine: Union[str, List[str], None]=None,
    queue_name: Union[str, List[str], None]=None,
    topic_string: Union[str, int, List[Union[str, int]], None]=None,
    root_dir: Optional[str]=None,
    archive_backend=None):
  from_timestamp = to_timestamp_int(from_timestamp)
  archive_date = datetime.date.fromtimestamp(from_timestamp / 10.**9)
  while archive_date <= datetime.date.today() + datetime.timedelta(days=2):
    files = query_archive_file(
        machine, archive_date, queue_name, topic_string, root_dir,
        archive_backend=archive_backend)
    selected = sort_archive_file_in_timestamp(
        files, archive_backend=archive_backend)
    for filepath in selected:
      # Yield in timestamp-ascending order.
      yield filepath

    archive_date += datetime.timedelta(days=1)


class MultiFileReader(Reader):
  def __init__(self, filepath_iterator, archive_backend=None, logger=None):
    self._logger = logger or logging.getLogger(logger_name)

    # Use QueueSeqMergeReader for files with same queue
    # |filepath_iterator| must yield filepaths in timestamp-ascending order
    self._filepath_iterator = filepath_iterator
    self._merge_reader = TimestampMergeReader()
    self._archive_backend = archive_backend

    self._next_file = None
    self._next_file_timestamp = INT64MAX
    self._set_next_file()
    self._add_next_reader()

  def __del__(self):
    self.close()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def close(self):
    if self._merge_reader is not None:
      for topic_record_reader in self._merge_reader.readers:
        topic_record_reader.close()
      self._merge_reader = None

  def _on_reader_eof(self, topic_record_reader):
    topic_record_reader.close()

  def _reset_next_file(self):
    self._next_file = None
    self._next_file_timestamp = INT64MAX

  def _set_next_file(self):
    while True:
      try:
        self._next_file = next(self._filepath_iterator)
        self._next_file_timestamp = get_first_timestamp(
            self._next_file, archive_backend=self._archive_backend)
        return
      except (EOFError, TopicRecordReaderError):
        # Skip the file
        self._logger.warning(
            'File %s seems corrupted, skipped.' % self._next_file)
        self._reset_next_file()
        continue
      except StopIteration:
        self._reset_next_file()
        return

  def _add_next_reader(self):
    if self._next_file is None:
      return
    topic_record_reader = TopicRecordReader(
        self._next_file, archive_backend=self._archive_backend)
    self._merge_reader.add_reader(topic_record_reader, self._on_reader_eof)
    self._set_next_file()

  def read(self) -> Optional[TopicRecord]:
    record = self.peek()
    self._merge_reader.read()
    return record

  def peek(self) -> Optional[TopicRecord]:
    record = self._merge_reader.peek()
    if record is None:
      if self._next_file is None:
        return None  # EOF
      self._add_next_reader()
      return self.peek()

    if record.timestamp > self._next_file_timestamp:
      self._add_next_reader()
      return self.peek()
    return record


def _try_get_archive_backend(archive_file: Union[str, List[str]]):
  archive_file = to_list(archive_file)
  types = set()
  for fp in archive_file:
    types.add(get_archive_backend_type(fp))
  if len(types) == 1:
    return get_archive_backend(archive_file[0])
  else:
    return None


class ArchiveReader(Reader):
  @staticmethod
  def from_file(archive_file: Union[str, List[str]]):
    archive_file = sort_archive_file_in_timestamp(archive_file)
    archive_backend = _try_get_archive_backend(archive_file)
    return ArchiveReader(INT64MIN, iter(archive_file),
                         archive_backend=archive_backend)

  @staticmethod
  def from_archive(from_timestamp: Union[int, datetime.datetime, datetime.date],
                   machine: Union[str, List[str], None]=None,
                   queue_name: Union[str, List[str], None]=None,
                   topic_string: Union[str, List[str], None]=None,
                   root_dir: Optional[str]=None,
                   archive_backend=None):
    archive_backend = archive_backend or \
                      get_archive_backend(root_dir or default_archive_root_dir)
    filepath_iterator = iter_archive_file(
        from_timestamp, machine, queue_name, topic_string, root_dir,
        archive_backend=archive_backend)
    return ArchiveReader(from_timestamp, filepath_iterator,
                         archive_backend=archive_backend)

  def __init__(self, from_timestamp, filepath_iterator, archive_backend=None):
    self._past_record_skipped = False
    self._from_timestamp = to_timestamp_int(from_timestamp)
    self._reader = MultiFileReader(filepath_iterator,
                                   archive_backend=archive_backend)

  def __del__(self):
    self.close()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def close(self):
    if self._reader is not None:
      self._reader.close()
      self._reader = None

  def _skip_past_records(self):
    # WARNING: this would take long time.
    # Skip records written before |first_timestamp|.
    assert not self._past_record_skipped
    while True:
      record = self._reader.peek()
      if record is None:
        break  # EOF
      if record.timestamp >= self._from_timestamp:
        self._past_record_skipped = True
        break
      self._reader.read()

  def peek(self):
    if not self._past_record_skipped:
      self._skip_past_records()

    # After all skipped, return without checking.
    return self._reader.peek()

  def read(self):
    if not self._past_record_skipped:
      self._skip_past_records()

    # After all skipped, return without checking.
    return self._reader.read()


def ensure_dir_exists(dirpath):
  if os.path.isdir(dirpath):
    return
  try:
    os.makedirs(dirpath)
  except FileExistsError:
    if not os.path.isdir(dirpath):
      raise


# Implement per-topic serializer.
def serialize_topic_record_data(record: TopicRecord):
  if not isinstance(record.data, (dict, list)):
    return record
  assert isinstance(record.data, (dict, list))
  serialized_data = json.dumps(record.data)
  return TopicRecord(record.queue_seq, record.topic_id, record.topic_seq,
                     record.timestamp, serialized_data)


class QueueWriter(object):
  def __init__(self,
               queue_name: str,
               queue_time: Union[datetime.datetime, datetime.date, None],
               topic_map=None,
               machine: Optional[str]=None,
               root_dir: Optional[str]=None,
               compression_type: TopicRecordCompressionType
                   =TopicRecordCompressionType.GZIP,
               serializer=None):
    self._queue_name = queue_name
    self._topic_map = topic_map or get_default_topic_map()
    self._machine = machine or get_hostname()
    self._root_dir = os.path.expanduser(root_dir or default_archive_root_dir)
    self._compression_type = compression_type
    self._serializer = serializer or serialize_topic_record_data
    self._writers = {}  # map: topid_id -> writer

    self._queue_time = None
    self._queue_reset_timestamp = None
    self.reset_queue(queue_time)

  def __del__(self):
    self.close()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def close(self):
    if self._writers:
      for _, writer in self._writers.items():
        writer.close()
      self._writers = {}
    self._queue_time = None
    self._queue_reset_timestamp = None

  def reset_queue(self,
                  queue_time: Union[datetime.datetime, datetime.date, None]):
    self.close()
    self._queue_time = to_datetime(queue_time or datetime.datetime.now())
    self._queue_reset_timestamp = to_timestamp_int(
        self._queue_time.date() + datetime.timedelta(days=1))
    # timezone

  def _get_writer(self, topic_id):
    try:
      return self._writers[topic_id]
    except KeyError:
      pass

    assert self._queue_time is not None
    queue_time_str = self._queue_time.strftime('%Y%m%d-%H%M%SZ')
    filename = '%s.%s.%s' % (
        self._topic_map.search_topic_string(topic_id),
        self._queue_name, queue_time_str)
    if self._compression_type == TopicRecordCompressionType.GZIP:
      filename += '.gz'

    date_str = self._queue_time.strftime('%Y%m%d')
    dirpath = os.path.join(self._root_dir, self._machine, date_str)
    ensure_dir_exists(dirpath)
    filepath = os.path.join(dirpath, filename)
    writer = TopicRecordWriter(filepath, self._compression_type)
    self._writers[topic_id] = writer
    return writer

  def write(self, record: TopicRecord):
    if record.timestamp >= self._queue_reset_timestamp:
      self.reset_queue(to_datetime(record.timestamp).date())
    try:
      writer = self._writers[record.topic_id]
    except KeyError:
      writer = self._get_writer(record.topic_id)
    writer.write_record(self._serializer(record))

  def flush(self):
    for _, writer in self._writers.items():
      writer.flush()


# Make ArchiveWriter supporting multiple queue.
class ArchiveWriter(QueueWriter):
  pass
