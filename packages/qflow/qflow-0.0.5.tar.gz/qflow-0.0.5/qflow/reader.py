import heapq
from typing import Any, Callable, Optional

from .topic_record import TopicRecord


class Reader(object):
  def __init__(self):
    raise NotImplementedError()

  def read(self) -> Optional[TopicRecord]:
    # Return None on EOF.
    raise NotImplementedError()

  def peek(self) -> Optional[TopicRecord]:
    # Return None on EOF.
    raise NotImplementedError()


class _ContainerBase(object):
  INT64MIN = -9223372036854775808

  def __init__(self, reader, eof_callback):
    self.reader = reader
    self.eof_callback = eof_callback

  def abandon(self):
    self.reader = None
    self.eof_callback = None

  @property
  def abandoned(self):
    return self.reader is None

  def query_priority(self):
    raise NotImplementedError()


class _TimestampContainer(_ContainerBase):
  def query_priority(self):
    if self.reader is None:
      return self.INT64MIN
    record = self.reader.peek()
    if record is None:
      # On EOF, return the lowest number to make it out of pqueue.
      return (self.INT64MIN, 0)
    return (record.timestamp, record.topic_id)


class _QueueSeqContainer(_ContainerBase):
  def query_priority(self):
    if self.reader is None:
      return self.INT64MIN
    record = self.reader.peek()
    if record is None:
      # On EOF, return the lowest number to make it out of pqueue.
      return (self.INT64MIN, 0)
    return (record.queue_seq, record.topic_id)


class PriorityQueue(object):
  def __init__(self):
    self._heap = []

  def put(self, obj):
    heapq.heappush(self._heap, obj)

  def get(self):
    return heapq.heappop(self._heap)


class MergeReader(Reader):
  def __init__(self, container_type):
    self._container_type = container_type
    self._readers = {}
    self._pqueue = PriorityQueue()
    self._record_cache = None

  @property
  def readers(self):
    return self._readers.keys()

  def add_reader(self, reader,
                 eof_callback: Callable[[Any], None]=(lambda _: None)):
    # At EOF, reader will be removed and eod_callback will be called.
    # eof_callback is safe to raise an exception to stop peek().
    assert reader not in self._readers
    container = self._container_type(reader, eof_callback)
    self._readers[reader] = container
    self._pqueue.put((container.query_priority(), container))
    self._record_cache = None

  def remove_reader(self, reader):
    if reader not in self._readers:
      return
    container = self._readers[reader]
    container.abandon()
    del self._readers[reader]
    self._record_cache = None

  def update_reader(self, reader):
    assert reader in self._readers
    container = self._readers[reader]
    new_container = self._container_type(container.reader,
                                         container.eof_callback)
    container.abandon()
    self._pqueue.put((new_container.query_priority(), new_container))
    self._record_cache = None

  def read(self) -> Optional[TopicRecord]:
    record = self._get_top_record(consume=True)
    self._record_cache = None
    return record

  def peek(self) -> Optional[TopicRecord]:
    if self._record_cache is not None:
      return self._record_cache
    self._record_cache = self._get_top_record(consume=False)
    return self._record_cache

  def _get_top_record(self, consume: bool=False) -> Optional[TopicRecord]:
    while True:
      try:
        _, container = self._pqueue.get()
      except IndexError:
        # No reader. Return EOF.
        return None

      if container.abandoned:
        # Removed reader.
        continue

      if consume:
        record = container.reader.read()
      else:
        record = container.reader.peek()

      if record is None:  # EOF
        eof_callback = container.eof_callback
        del self._readers[container.reader]
        eof_callback(container.reader)
        continue

      self._pqueue.put((container.query_priority(), container))
      return record


class TimestampMergeReader(MergeReader):
  def __init__(self):
    super().__init__(_TimestampContainer)


class QueueSeqMergeReader(MergeReader):
  def __init__(self):
    super().__init__(_QueueSeqContainer)
