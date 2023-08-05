import datetime
import logging
from typing import List, Optional, Union

from recordclass import recordclass

from .archive import ArchiveReader, INT64MAX, to_timestamp_int
from .topic_map import get_default_topic_map


logger_name = 'flow'


QueueData = recordclass('QueueData', ['queue_name', 'reader_data', 'user_data'])
TopicData = recordclass('TopicData', ['topic_id', 'topic_string', 'user_data'])


class TopicNotFoundError(Exception):
  pass


class _FlowSubscriberBase(object):
  SubscriptionEntry = recordclass('SubscriptionEntry',
                                  ['callback', 'topic_data'])

  def __init__(self, topic_map=None, logger=None):
    self._logger = logger or logging.getLogger(logger_name)
    self._topic_map = topic_map or get_default_topic_map()
    self._error_callback = self._log_error
    self._subscription = {}

  def _log_error(self, error):
    try:
      raise error
    except:
      self._logger.exception('Exception')

  def set_error_callback(self, error_callback):
    self._error_callback = error_callback

  def dispatch_topic_record(self, queue_data, record,
                            propagate_handler_exception: bool=False):
    try:
      entry = self._subscription[record.topic_id]
    except KeyError:  # Skip the record.
      return
    try:
      for callback in entry.callback:
        callback(record, queue_data, entry.topic_data)
    except Exception as e:
      if propagate_handler_exception:
        raise
      self._error_callback(e)

  def subscribe(self, topic: Union[str, int], callback):
    topics = self._topic_map.search_topic_id(topic)
    if not topics:
      raise TopicNotFoundError(topic)

    for topic_string, topic_id in topics:
      if topic_id in self._subscription:
        entry = self._subscription[topic_id]
        entry.callback.append(callback)
      else:
        topic_data = TopicData(topic_id, topic_string, None)
        entry = self.SubscriptionEntry([callback], topic_data)
        self._subscription[topic_id] = entry

  def unsubscribe(self, topic: Union[str, int], callback=None):
    topics = self._topic_map.search_topic_id(topic)
    for topic_string, topic_id in topics:
      try:
        if callback is None:
          del self._subscription[topic_id]
        else:
          self._subscription[topic_id].callback.remove(callback)
      except (KeyError, ValueError):
        pass

  def start(self):
    raise NotImplemented()

  def read_once(self, timeout=None):
    raise NotImplemented()

  def stop(self):
    raise NotImplemented()


class _FlowSubscriber_SimpleQueue(_FlowSubscriberBase):
  def __init__(self, reader, topic_map=None, logger=None):
    super().__init__(topic_map, logger)
    self._queue_data = QueueData(
        reader.queue.queue_name, None, None)
    self._reader = reader
    self._reader.set_handler(self)

  def __del__(self):
    self.stop()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()

  def on_error(self, error):
    self._error_callback(error)

  def on_topic_record(self, record):
    self.dispatch_topic_record(self._queue_data, record)

  def start(self):
    self._reader.start()

  def read_once(self, timeout=None):
    self._reader.read_once(timeout=timeout)

  def stop(self):
    if self._reader is not None:
      self._reader.stop()
      self._reader = None


class _FlowSubscriber_Archive(_FlowSubscriberBase):
  def __init__(self, reader, topic_map=None, logger=None):
    super().__init__(topic_map, logger)
    self._queue_data = None
    self._reader = reader
    self._until = INT64MAX

  def __del__(self):
    self.stop()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()

  def start(self, until=INT64MAX):
    self._until = to_timestamp_int(until)
    try:
      while True:
        self.read_once(raise_on_eof=True)
    except EOFError:
      pass

  def read_once(self, timeout=None, raise_on_eof=False):
    if self._reader is None:
      raise EOFError()
    record = self._reader.read()
    if record is None or record.timestamp > self._until:  # EOF
      if raise_on_eof:
        raise EOFError()
      return
    self.dispatch_topic_record(self._queue_data, record,
                               propagate_handler_exception=True)

  def stop(self):
    if self._reader is not None:
      self._reader.close()
      self._reader = None


def from_queue(queue, threaded=False, topic_map=None, logger=None):
  if not threaded:
    reader = queue.get_reader(logger=logger)
  else:
    reader = queue.get_threaded_reader(logger=logger)
  return _FlowSubscriber_SimpleQueue(reader, topic_map, logger)


def from_archive(from_timestamp: Union[int, datetime.datetime, datetime.date],
                 machine: Union[str, List[str], None]=None,
                 queue_name: Union[str, List[str], None]=None,
                 topic_string: Union[str, List[str], None]=None,
                 root_dir: Optional[str]=None,
                 topic_map=None,
                 logger=None):
  reader = ArchiveReader.from_archive(
      from_timestamp, machine, queue_name, topic_string, root_dir)
  return _FlowSubscriber_Archive(reader, topic_map, logger)


def from_file(archive_file: Union[str, List[str]], topic_map=None, logger=None):
  reader = ArchiveReader.from_file(archive_file)
  return _FlowSubscriber_Archive(reader, topic_map, logger)
