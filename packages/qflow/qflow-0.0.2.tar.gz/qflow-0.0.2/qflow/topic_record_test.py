import datetime
import os
import shutil
import tempfile
import unittest

from . import topic_record
from .util import nanoseconds_from_epoch


class TopicRecordTest(unittest.TestCase):
  def setUp(self):
    self._tmpdir = tempfile.mkdtemp(prefix='test_')

  def tearDown(self):
    shutil.rmtree(self._tmpdir)

  def test_writer_magic(self):
    filepath = os.path.join(self._tmpdir, 'record')
    compression_type = topic_record.TopicRecordCompressionType.NONE

    with topic_record.TopicRecordWriter(
             filepath, compression_type=compression_type, lazy_open=False):
      pass
    with open(filepath, 'rb') as f:
      magic = f.read()
      self.assertEqual(magic, topic_record.MAGIC_BYTES)

  def _test_rw(self, compression_type):
    filepath = os.path.join(self._tmpdir, 'record')

    base_ts = nanoseconds_from_epoch(datetime.datetime.now())
    with topic_record.TopicRecordWriter(
            filepath, compression_type=compression_type) as writer:
      self.assertFalse(os.path.exists(filepath))
      for idx in range(0, 1000):
        writer.write(None, idx % 17, None, base_ts + idx * 1000000,
                     'record-%d' % idx)

    with topic_record.TopicRecordReader(
             filepath, compression_type=compression_type) as reader:
      for idx, record in enumerate(reader.read_records()):
        self.assertEqual(idx, record.queue_seq)
        self.assertEqual(idx % 17, record.topic_id)
        self.assertEqual(int(idx / 17), record.topic_seq)
        self.assertEqual(base_ts + idx * 1000000, record.timestamp)
        self.assertEqual('record-%d' % idx,
                         record.data.tobytes().decode('utf-8'))

  def test_rw(self):
    self._test_rw(topic_record.TopicRecordCompressionType.NONE)

  def test_rw_gzip(self):
    self._test_rw(topic_record.TopicRecordCompressionType.GZIP)

  def test_fileobj_read(self):
    filepath = os.path.join(self._tmpdir, 'record.gz')

    base_ts = nanoseconds_from_epoch(datetime.datetime.now())
    with topic_record.TopicRecordWriter(filepath) as writer:
      self.assertFalse(os.path.exists(filepath))
      for idx in range(0, 1000):
        writer.write(None, idx % 17, None, base_ts + idx * 1000000,
                     'record-%d' % idx)

    compression_type = topic_record.TopicRecordCompressionType.GZIP
    with open(filepath, 'rb') as fileobj, \
         topic_record.TopicRecordReader(
             fileobj=fileobj, compression_type=compression_type) as reader:
      for idx, record in enumerate(reader.read_records()):
        self.assertEqual(idx, record.queue_seq)
        self.assertEqual(idx % 17, record.topic_id)
        self.assertEqual(int(idx / 17), record.topic_seq)
        self.assertEqual(base_ts + idx * 1000000, record.timestamp)
        self.assertEqual('record-%d' % idx,
                         record.data.tobytes().decode('utf-8'))

  def test_partial_read(self):
    filepath_1 = os.path.join(self._tmpdir, 'record_1')
    compression_type = topic_record.TopicRecordCompressionType.NONE

    ts = nanoseconds_from_epoch(datetime.datetime.now())
    with topic_record.TopicRecordWriter(
            filepath_1, compression_type=compression_type) as writer:
      self.assertFalse(os.path.exists(filepath_1))
      writer.write(None, 1234, None, ts, 'record')

    with open(filepath_1, 'rb') as f:
      content = f.read()

    filepath_2 = os.path.join(self._tmpdir, 'record_2')
    with open(filepath_2, 'wb') as f, \
         topic_record.TopicRecordReader(
             filepath_2, compression_type=compression_type) as reader:
      for idx in range(0, len(content)):
        self.assertEqual(None, reader.read())
        f.write(content[idx:idx+1])
        f.flush()
      record = reader.read()
      self.assertNotEqual(None, record)
      self.assertEqual(0, record.queue_seq)
      self.assertEqual(1234, record.topic_id)
      self.assertEqual(0, record.topic_seq)
      self.assertEqual(ts, record.timestamp)
      self.assertEqual('record', record.data.tobytes().decode('utf-8'))

      # No more record
      self.assertEqual(None, reader.read())

  def test_invalid_magic(self):
    filepath = os.path.join(self._tmpdir, 'record')
    compression_type = topic_record.TopicRecordCompressionType.NONE
    with open(filepath, 'wb') as f, \
         topic_record.TopicRecordReader(
             filepath, compression_type=compression_type) as reader:
      f.write(b'a')
      f.flush()
      with self.assertRaises(topic_record.InvalidMagicError):
        reader.read()

    for idx in range(7, 0, -1):
      with open(filepath, 'wb') as f, \
           topic_record.TopicRecordReader(
               filepath, compression_type=compression_type) as reader:
        f.write(topic_record.MAGIC_BYTES[0:idx])
        f.flush()
        self.assertEqual(None, reader.read())
        f.write(b'x')
        f.flush()
        with self.assertRaises(topic_record.InvalidMagicError):
          reader.read()


if __name__ == "__main__":
  unittest.main()
