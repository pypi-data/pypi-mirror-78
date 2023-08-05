import binascii
import datetime
import gzip
import os
import struct
from collections import namedtuple
from enum import Enum
from typing import Union, Optional

from .util import nanoseconds_from_epoch
from .archive_backend import get_archive_backend


class TopicRecordReaderError(Exception):
  pass


class InvalidMagicError(TopicRecordReaderError):
  # Unrecovabale.
  pass


class CrcLengthError(TopicRecordReaderError):
  # Unrecovabale.
  pass


class CrcRecordError(TopicRecordReaderError):
  # Possible to skip a record.
  pass


def crc32_masked(bytes_in: bytes):
  # Masked CRC32:
  # https://www.tensorflow.org/api_guides/python/python_io#tfrecords_format_details
  crc = binascii.crc32(bytes_in)
  masked_crc = (((crc >> 15) | (crc << 17)) + 0xa282ead8) & 0xffffffff
  return masked_crc


class ReadContext(object):
  DEFAULT_BUFSIZE = 1024

  def __init__(self, file_obj):
    assert file_obj is not None
    self._file = file_obj
    self._length = 0
    self._offset = 0
    self._buf = bytearray(self.DEFAULT_BUFSIZE)
    self._buf_ownership = True

  def reset(self, length: int, custom_buf=None):
    assert length >= 0
    self._length = length
    self._offset = 0

    if custom_buf:
      assert len(custom_buf) >= length
      self._buf = custom_buf
      self._buf_ownership = False
      return

    if not self._buf_ownership:
      self._buf = None
      self._buf_ownership = True

    buf_len = (len(self._buf)
               if self._buf is not None else self.DEFAULT_BUFSIZE)
    while buf_len < length:
      buf_len *= 2
      assert buf_len <= 2**30
    if self._buf is None or buf_len != len(self._buf):
      self._buf = bytearray(buf_len)

  def get_buf(self):
    return memoryview(self._buf)[0:self._offset]

  def release_buf(self):
    try:
      buf = self._buf
      buf_len = self._offset
      return memoryview(buf)[0:buf_len]
    finally:
      self._buf = bytearray(max(self.DEFAULT_BUFSIZE, buf_len))
      self._buf_ownership = True
      self.reset(0)

  def read(self):
    if self._length == self._offset:
      return True
    buf = memoryview(self._buf)[self._offset:self._length]
    try:
      read_len = self._file.readinto(buf)
    except EOFError:
      read_len = None
    if read_len is None:
      return False
    self._offset += read_len
    assert self._offset <= self._length
    return self._length == self._offset


class TopicRecordCompressionType(Enum):
  NONE = 1
  GZIP = 2


# Note: 00 3.14159 00 01 00 00
MAGIC_BYTES = b'\x00\x31\x41\x59\x00\x01\x00\x00'

TopicRecord = namedtuple(
    'TopicRecord',
    ['queue_seq', 'topic_id', 'topic_seq', 'timestamp', 'data'])


class TopicRecordReader(object):
  class State(Enum):
    OPEN_FILE = 0
    READ_MAGIC = 1
    READ_LENGTH = 2
    READ_RECORD = 3
    ERROR = 4

  def __init__(self, filepath: Optional[str]=None, fileobj=None,
               compression_type: Optional[TopicRecordCompressionType]=None,
               archive_backend=None):
    self._last_record = None
    self._last_error = None
    self._record = None
    self._file = None
    self._underlying_file = None

    # Set filepath
    if filepath is not None:
      self._filepath = filepath
    else:
      try:
        self._filepath = fileobj.filepath
      except AttributeError:
        self._filepath = None

    # Set compression_type
    self._compression_type = (compression_type or
                              TopicRecordCompressionType.NONE)
    if (compression_type is None and
        self._filepath is not None and self._filepath.endswith('.gz')):
      self._compression_type = TopicRecordCompressionType.GZIP

    self._state = self.State.OPEN_FILE
    self._read_context = None
    self._open_file(fileobj, archive_backend=archive_backend)

  @property
  def filepath(self):
    return self._filepath

  @property
  def compression_type(self):
    return self._compression_type

  def __del__(self):
    self.close()

  def close(self):
    if self._file is not None:
      self._file.close()
      self._file = None
    if self._underlying_file is not None:
      self._underlying_file.close()
      self._underlying_file = None

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def _open_file(self, fileobj=None, read_next=False, archive_backend=None):
    assert self._file is None

    if fileobj is None:
      archive_backend = archive_backend or get_archive_backend(self._filepath)
      fileobj = archive_backend.open(self._filepath, 'rb')

    if self.compression_type == TopicRecordCompressionType.NONE:
      self._file = fileobj
    elif self.compression_type == TopicRecordCompressionType.GZIP:
      self._file = gzip.GzipFile(fileobj=fileobj)
      self._underlying_file = fileobj
    else:
      raise ValueError('Unknown compression type: %s'
                       % str(self.compressino_type))

    self._state = self.State.READ_MAGIC
    self._read_context = ReadContext(self._file)
    self._read_context.reset(8)
    if read_next:
      return self._read_magic(True)

  def _read_magic(self, read_next=False):
    read_all = self._read_context.read()
    buf = self._read_context.get_buf()
    if buf != memoryview(MAGIC_BYTES)[0:len(buf)]:
      self._state = self.State.ERROR
      raise InvalidMagicError()
    if not read_all:
      return None

    self._state = self.State.READ_LENGTH
    self._read_context.reset(12)
    if read_next:
      return self._read_length()

  def _read_length(self):
    if not self._read_context.read():
      return None
    buf = self._read_context.get_buf()
    length, crc_length = struct.unpack('<QI', buf)
    if crc_length != 0 and crc32_masked(buf[0:8]) != crc_length:
      self._state = self.State.ERROR
      raise CrcLengthError()

    self._state = self.State.READ_RECORD
    self._read_context.reset(length + 4)
    return self._read_record()

  def _read_record(self) -> Optional[TopicRecord]:
    if not self._read_context.read():
      return None
    try:
      buf = self._read_context.get_buf()
      queue_seq, topic_id, topic_seq, timestamp = \
        struct.unpack('<QQQq', buf[0:32])
      crc_record = struct.unpack('<I', buf[-4:])[0]
      if crc_record != 0 and crc32_masked(buf[0:-4]) != crc_record:
        raise CrcRecordError()

      # check release_buf() performance
      # data = self._read_context.release_buf()[32:-4]
      data = memoryview(buf[32:-4].tobytes())

      return TopicRecord(
          queue_seq=queue_seq, topic_id=topic_id, topic_seq=topic_seq,
          timestamp=timestamp, data=data)
    finally:
      self._state = self.State.READ_LENGTH
      self._read_context.reset(12)

  def peek(self) -> Optional[TopicRecord]:
    if self._record is not None:
      return self._record

    try:
      if self._state == self.State.READ_LENGTH:
        self._record = self._read_length()
      elif self._state == self.State.READ_RECORD:
        self._record = self._read_record()
      elif self._state == self.State.READ_MAGIC:
        self._record = self._read_magic(True)
      elif self._state == self.State.ERROR:
        raise self._last_error
      else:
        raise ValueError('Unknown state: %s' % str(self._state))
      return self._record
    except TopicRecordReaderError as e:
      self._last_error = e
      raise

  def read(self) -> Optional[TopicRecord]:
    record = self.peek()
    self._record = None
    return record

  def read_records(self):
    while True:
      record = self.read()
      if record is None:
        break
      yield record


class TopicRecordWriter(object):
  def __init__(
      self,
      filepath,
      compression_type: Optional[TopicRecordCompressionType]=None,
      lazy_open=True):
    self._compression_type = (compression_type or
                              TopicRecordCompressionType.NONE)
    if compression_type is None and filepath.endswith('.gz'):
      self._compression_type = TopicRecordCompressionType.GZIP

    self._filepath = filepath
    self._file = None
    self._next_queue_seq = 0
    self._next_topic_seq = {}
    self._buf = bytearray(1024)
    if not lazy_open:
      self._ensure_file_ready()

  @property
  def filepath(self):
    return self._filepath

  @property
  def compression_type(self):
    return self._compression_type

  def __del__(self):
    self.close()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def close(self):
    if self._file is not None:
      self._file.close()
      self._file = None

  def _ensure_file_ready(self):
    if self._file is not None:
      return
    if os.path.exists(self._filepath):
      raise FileExistsError()

    if self.compression_type == TopicRecordCompressionType.NONE:
      self._file = open(self._filepath, 'wb')
    elif self.compression_type == TopicRecordCompressionType.GZIP:
      self._file = gzip.GzipFile(self._filepath, 'wb', compresslevel=5)
    else:
      raise ValueError('Unknown compression type: %s'
                       % str(self.compressino_type))
    self._file.write(MAGIC_BYTES)

  def _get_queue_seq(self, queue_seq: Optional[int], auto_queue_seq: bool):
    if queue_seq is None:
      if not auto_queue_seq:
        raise ValueError()
      queue_seq = self._next_queue_seq
      self._next_queue_seq += 1
    elif auto_queue_seq:
      self._next_queue_seq = queue_seq + 1
    return queue_seq

  def _get_topic_seq(self, topic_id: int, topic_seq: Optional[int],
                     auto_topic_seq: bool):
    if topic_seq is None:
      if not auto_topic_seq:
        raise ValueError()
      topic_seq = self._next_topic_seq.get(topic_id, 0)
      self._next_topic_seq[topic_id] = topic_seq + 1
    elif auto_topic_seq:
      self._next_topic_seq[topic_id] = topic_seq + 1
    return topic_seq

  def _ensure_buf(self, length):
    buf_len = len(self._buf)
    while buf_len < length:
      buf_len *= 2
      assert buf_len <= 2**30
    if buf_len != len(self._buf):
      self._buf = bytearray(buf_len)

  def write_record(self, topic_record: TopicRecord):
    self.write(
        queue_seq=topic_record.queue_seq, topic_id=topic_record.topic_id,
        topic_seq=topic_record.topic_seq, timestamp=topic_record.timestamp,
        data=topic_record.data)

  def write(
      self,
      queue_seq: Optional[int],
      topic_id: int,
      topic_seq: Optional[int],
      timestamp: Union[int, datetime.datetime],
      data: Union[bytes, str],
      flush: bool=False,
      crc: bool=True,
      data_str_encoding: str='utf-8',
      auto_queue_seq: bool=True,
      auto_topic_seq: bool=True):
    queue_seq = self._get_queue_seq(queue_seq, auto_queue_seq)
    topic_seq = self._get_topic_seq(topic_id, topic_seq, auto_topic_seq)
    if isinstance(timestamp, datetime.datetime):
      timestamp = nanoseconds_from_epoch(timestamp)
    if isinstance(data, str):
      data = data.encode(data_str_encoding)

    '''
    offset  size  type    description
    --------------------------------------------
         0     8  uint64  length
         8     4  uint32  masked_crc32_of_length
        12     8  uint64  queue_seq
        20     8  uint64  topic_id
        28     8  uint64  topic_seq
        36     8  int64   timestamp
        44   len  byte    data[length - 32]
    44+len     4  uint32  masked_crc32_of_record
                          (queue_seq, topic_id, topic_seq, timestamp, data)
    48+len     0  -       RECORD_END
    '''

    total_len = 48 + len(data)
    self._ensure_buf(total_len)

    buf = memoryview(self._buf)[0:total_len]
    struct.pack_into('<Q', buf, 0, len(data) + 32)
    crc_length = crc32_masked(buf[0:8]) if crc else 0
    struct.pack_into('<I', buf, 8, crc_length)
    struct.pack_into('<QQQq', buf, 12, queue_seq, topic_id, topic_seq,
             timestamp)
    buf[44:44+len(data)] = data
    crc_record = crc32_masked(buf[12:44+len(data)]) if crc else 0
    struct.pack_into('<I', buf, 44+len(data), crc_record)

    self._ensure_file_ready()
    self._file.write(buf)
    if flush:
      self.flush()

  def flush(self):
    if self._file is not None:
      self._file.flush()
