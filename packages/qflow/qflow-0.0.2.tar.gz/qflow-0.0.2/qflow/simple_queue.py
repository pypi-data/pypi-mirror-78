import datetime
import logging
import queue
import threading
from enum import Enum
from typing import Dict, Optional, Union

import archive
from .topic_record import TopicRecord


logger_name = 'qflow'


class SimpleQueueError(Exception):
  pass


class TopicRecordHandler(object):
  def on_error(self, error):
    pass

  def on_topic_record(self, record):
    pass


class SimpleQueue_Writer(object):
  def __init__(self,
               target_queue,
               topic_id: int,
               next_topic_seq: Optional[int]=None):
    self._queue = target_queue
    self._topic_id = topic_id
    self._next_topic_seq = next_topic_seq or 0

  def close(self):
    self._queue = None

  @property
  def queue(self):
    return self._queue

  @property
  def topic_id(self):
    return self._topic_id

  @property
  def next_topic_seq(self):
    return self._next_topic_seq

  def reset_topic_seq(self, next_topic_seq: Optional[int]=None):
    self._next_topic_seq = next_topic_seq or 0

  def write(self, timestamp, data):
    topic_seq = self._next_topic_seq
    self._next_topic_seq += 1
    timestamp = archive.to_timestamp_int(timestamp)
    self._queue._write(self._topic_id, topic_seq, timestamp, data)


class SimpleQueue_Reader(object):
  def __init__(self,
               target_queue,
               handler: Optional[TopicRecordHandler]=None,
               logger=None):
    self._logger = logger or logging.getLogger(logger_name)
    self._queue = target_queue
    self._stopped = False
    self._handler = handler or TopicRecordHandler()

  @property
  def queue(self):
    return self._queue

  def __del__(self):
    self.stop()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()

  def set_handler(self, handler):
    self._handler = handler or TopicRecordHandler()

  def stop(self):
    self._stopped = True

  @property
  def stopped(self):
    return self._stopped

  def on_error(self, error):
    try:
      self._handler.on_error(error)
    except Exception:
      self._logger.exception('handler raises an exception')

  def on_topic_record(self, record):
    try:
      self._handler.on_topic_record(record)
    except Exception:
      self._logger.exception('handler raises an exception')


class SimpleQueue_ThreadedReader(object):
  class ReaderStop(Exception):
    pass

  class EventType(Enum):
    TOPIC_RECORD = 1
    ERROR = 2
    CONTROL = 3

  def __init__(self,
               target_queue,
               handler: Optional[TopicRecordHandler]=None,
               logger=None):
    self._logger = logger or logging.getLogger(logger_name)
    self._queue = target_queue
    self._stopped = False
    self._handler = handler or TopicRecordHandler()
    self._fifo = queue.Queue()

  @property
  def queue(self):
    return self._queue

  def __del__(self):
    self.stop()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()

  def read_once(self,
                timeout: Optional[datetime.timedelta]=None,
                propagate_handler_exception: bool=False):
    if timeout is not None:
      timeout_sec = timeout.total_seconds()
      if timeout_sec < 0:
        raise TimeoutError()
    else:
      timeout_sec = None

    try:
      event_type, data = self._fifo.get(timeout=timeout_sec)
    except queue.Empty:
      raise TimeoutError()

    try:
      if event_type == self.EventType.TOPIC_RECORD:
        self._handler.on_topic_record(data)
      elif event_type == self.EventType.ERROR:
        self._handler.on_error(data)
      elif event_type == self.EventType.CONTROL:
        raise self.ReaderStop()
      else:
        raise SimpleQueueError()
    except (SimpleQueueError, self.ReaderStop):
      raise
    except Exception:
      self._logger.exception('handler raises an exception')
      if propagate_handler_exception:
        raise
    finally:
      self._fifo.task_done()

  def start(self,
            duration: Optional[datetime.timedelta]=None,
            propagate_handler_exception: bool=False):
    # Run this on a reader thread.
    assert not self._stopped

    until = (datetime.datetime.now() + duration if duration is not None
             else None)
    while True:
      try:
        timeout = (until - datetime.datetime.now() if duration is not None
                   else None)
        self.read_once(
            timeout=timeout,
            propagate_handler_exception=propagate_handler_exception)
      except (TimeoutError, self.ReaderStop):
        break

  def set_handler(self, handler):
    self._handler = handler or TopicRecordHandler()

  def stop(self):
    if not self._stopped:
      self._stopped = True
      self._fifo.put((self.EventType.CONTROL, None))

  @property
  def stopped(self):
    return self._stopped

  def on_error(self, error):
    self._fifo.put((self.EventType.ERROR, error))

  def on_topic_record(self, record):
    self._fifo.put((self.EventType.TOPIC_RECORD, record))


class SimpleQueue(object):
  # SimpleQueue does not allow writing from multiple threads.
  def __init__(self, queue_name: str=None, logger=None):
    self._logger = logger or logging.getLogger(logger_name)
    self._queue_name = queue_name
    self._next_queue_seq = 0
    self._readers = []

  @property
  def queue_name(self):
    return self._queue_name

  def get_next_queue_seq(self):
    return self._next_queue_seq.value

  def _clean_up_stopped_readers(self):
    new_readers = [reader for reader in self._readers if not reader.stopped]
    self._readers = new_readers

  def _write(self, topic_id, topic_seq, timestamp, data):
    queue_seq = self._next_queue_seq
    self._next_queue_seq += 1
    record = TopicRecord(queue_seq, topic_id, topic_seq, timestamp, data)

    clean_up_stopped_readers = False
    for reader in self._readers:
      if reader.stopped:
        clean_up_stopped_readers = True
        continue
      try:
        reader.on_topic_record(record)
      except Exception:
        self._logger.exception('reader raises an exception')

    if clean_up_stopped_readers:
      self._clean_up_stopped_readers()

  def get_writer(self, *args, **kwargs):
    return SimpleQueue_Writer(self, *args, **kwargs)

  def get_reader(self, *args, **kwargs):
    reader = SimpleQueue_Reader(self, *args, **kwargs)
    self._readers.append(reader)
    return reader

  def get_threaded_reader(self, *args, **kwargs):
    reader = SimpleQueue_ThreadedReader(self, *args, **kwargs)
    self._readers.append(reader)
    return reader

  def start_archiver(self, *args, **kwargs):
    # Return new archiver instance and start it.
    reader = self.get_threaded_reader(None)
    return ThreadedQueueArchiver(reader, *args, **kwargs)


class ThreadedQueueArchiver(object):
  def __init__(self,
               queue_reader,
               queue_name: Optional[str]=None,
               queue_time: Union[datetime.datetime, datetime.date, None]=None,
               topic_id_to_string_map: Optional[Dict[int, str]]=None,
               machine: Optional[str]=None,
               root_dir: Optional[str]=None,
               flush_period: Optional[datetime.timedelta]=None,
               logger=None):
    self._logger = logger or logging.getLogger(logger_name)
    self._queue_reader = queue_reader
    self._flush_period = flush_period or datetime.timedelta(seconds=1)

    queue_name = queue_name or queue_reader.queue.queue_name
    queue_time = queue_time or datetime.datetime.now()
    self._thread = threading.Thread(
        target=self._writer,
        args=(queue_name, queue_time, topic_id_to_string_map, machine,
              root_dir))
    self._thread.start()

  def __del__(self):
    self.stop()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.stop()

  def stop(self):
    if not self._queue_reader.stopped:
      self._queue_reader.stop()
    if self._thread:
      self._thread.join()
      self._thread = None

  def _writer(self, queue_name, queue_time, topic_id_to_string_map,
              machine, root_dir):
    logger = self._logger
    writer = archive.QueueWriter(queue_name, queue_time, topic_id_to_string_map,
                                 machine, root_dir)
    with writer:
      class Handler(object):
        def on_error(self, error):
          logger.error(error)

        def on_topic_record(self, record):
          writer.write(record)

      self._queue_reader.set_handler(Handler())
      while not self._queue_reader.stopped:
        self._queue_reader.start(duration=self._flush_period)
        writer.flush()
