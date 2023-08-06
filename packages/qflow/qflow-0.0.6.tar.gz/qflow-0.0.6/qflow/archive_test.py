import datetime
import json
import os
import shutil
import tempfile
import time
import unittest

import boto3
from moto import mock_s3

from . import archive
from .topic_record import (
    TopicRecord,
    TopicRecordReader,
    TopicRecordWriter)


# Set TZ to UTC
os.environ['TZ'] = 'UTC'


def _make_fake_topic_record(
    relpath, root_dir, first_timestamp=None, empty_file=False,
    corrupted_file=False, num_records=1024):
  filepath = os.path.join(root_dir, relpath)
  dirpath = os.path.dirname(filepath)
  if not os.path.isdir(dirpath):
    os.makedirs(dirpath)

  if empty_file:
    with open(filepath, 'wb') as f:
      return

  if corrupted_file:
    with open(filepath, 'wb') as f:
      f.write(b'Hello')
      return

  with TopicRecordWriter(filepath) as writer:
    first_timestamp = first_timestamp or (int(time.time() * 10**6) * 1000)
    for i in range(0, num_records):
      writer.write(None, 0, None, first_timestamp + i, 'record-%d' % i)


def _upload_to_s3(bucket, prefix, upload_srcdir):
  client = boto3.client('s3')
  client.create_bucket(Bucket=bucket)
  for dirpath, dirnames, filenames in os.walk(upload_srcdir):
    for filename in filenames:
      filepath = os.path.relpath(os.path.join(dirpath, filename), upload_srcdir)
      key = os.path.join(prefix, filepath)
      with open(os.path.join(dirpath, filename), 'rb') as f:
        client.put_object(Bucket=bucket, Key=key, Body=f)


class ArchiveUtilTest(unittest.TestCase):
  def setUp(self):
    self._tmpdir = tempfile.mkdtemp(prefix='test_')

  def tearDown(self):
    shutil.rmtree(self._tmpdir)

  def test_to_timestamp_int(self):
    self.assertEqual(0, archive.to_timestamp_int(datetime.date(1970, 1, 1)))
    self.assertEqual(
        86400000000000, archive.to_timestamp_int(datetime.date(1970, 1, 2)))

  def test_to_date_str(self):
    self.assertEqual(
        '20171220', archive.to_date_str(datetime.date(2017, 12, 20)))

  def test_get_first_timestamp(self):
    filepath_1 = os.path.join(self._tmpdir, 'record_1')
    with TopicRecordWriter(filepath_1) as writer:
      writer.write(None, 0, None, 12345678901, 'record1')
      writer.write(None, 0, None, 12345678902, 'record2')
      writer.write(None, 0, None, 12345678903, 'record3')
    self.assertEqual(12345678901, archive.get_first_timestamp(filepath_1))

    filepath_2 = os.path.join(self._tmpdir, 'record_2')
    with open(filepath_2, 'wb') as f:
      pass
    with self.assertRaises(EOFError):
      archive.get_first_timestamp(filepath_2)

  @mock_s3
  def test_get_first_timestamp_s3(self):
    # Prepare data
    filepath_1 = os.path.join(self._tmpdir, 'record_1')
    with TopicRecordWriter(filepath_1) as writer:
      writer.write(None, 0, None, 12345678901, 'record1')
      writer.write(None, 0, None, 12345678902, 'record2')
      writer.write(None, 0, None, 12345678903, 'record3')

    filepath_2 = os.path.join(self._tmpdir, 'record_2')
    with open(filepath_2, 'wb') as f:
      pass

    _upload_to_s3('test-bucket', 'data', self._tmpdir)

    # Test
    self.assertEqual(
        12345678901,
        archive.get_first_timestamp('s3://test-bucket/data/record_1'))

    with self.assertRaises(EOFError):
      archive.get_first_timestamp('s3://test-bucket/data/record_2')

  def test_decompose_archive_filename(self):
    self.assertEqual(
        ('test', 'default', datetime.datetime(2017, 12, 20, 21, 30, 29)),
        archive.decompose_archive_filename('test.default.20171220-213029Z'))
    self.assertEqual(
        ('a.b.c', 'default', datetime.datetime(2017, 12, 20, 11, 30, 28)),
        archive.decompose_archive_filename('a.b.c.default.20171220-113028Z'))

    # Archive timestamp, wrong time
    with self.assertRaises(ValueError):
      archive.decompose_archive_filename('a.b.c.default.20171235-113028Z')

    # Archive timestamp, timezone not supported
    with self.assertRaises(ValueError):
      archive.decompose_archive_filename('a.b.c.default.20171235-113028+0800')

    # topic_string or queue_name is missing
    with self.assertRaises(ValueError):
      archive.decompose_archive_filename('a.20171235-113028Z')

  def test_query_machine_archive_file_empty(self):
    root_dir = os.path.join(self._tmpdir, 'archive')
    os.makedirs(root_dir)

    # No file.
    self.assertEqual(
        [], archive.query_machine_archive_file(
                'machine-0', '20171220', root_dir=root_dir))

  def test_query_machine_archive_file_basic(self):
    root_dir = os.path.join(self._tmpdir, 'archive')
    os.makedirs(root_dir)

    file_list = [
        {'relpath': 'machine-1/20171219/a.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171219/b.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171219/c.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/a.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/b.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/c.default.20171229-000000Z',
         'empty_file': True},
        {'relpath': 'machine-1/20171220/d.default.20171229-000000Z',
         'corrupted_file': True},
        {'relpath': 'machine-1/20171220/e.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/wrong_filename.20171229-000000Z'}
    ]

    for entry in file_list:
      _make_fake_topic_record(root_dir=root_dir, **entry)

    def abspath(relpath):
      return os.path.join(root_dir, relpath)

    self.assertEqual(
        [abspath('machine-1/20171219/a.default.20171229-000000Z'),
         abspath('machine-1/20171219/b.default.20171229-000000Z'),
         abspath('machine-1/20171219/c.default.20171229-000000Z')],
        archive.query_machine_archive_file(
            'machine-1', '20171219', root_dir=root_dir))

    self.assertEqual(
        [abspath('machine-1/20171220/a.default.20171229-000000Z'),
         abspath('machine-1/20171220/b.default.20171229-000000Z'),
         abspath('machine-1/20171220/e.default.20171229-000000Z')],
        archive.query_machine_archive_file(
            'machine-1', '20171220', root_dir=root_dir))

    self.assertEqual(
        [abspath('machine-1/20171220/a.default.20171229-000000Z'),
         abspath('machine-1/20171220/b.default.20171229-000000Z'),
         abspath('machine-1/20171220/e.default.20171229-000000Z')],
        archive.query_machine_archive_file(
            'machine-1', '20171220', queue_name='de*', root_dir=root_dir))

    self.assertEqual(
        [],
        archive.query_machine_archive_file(
            'machine-1', '20171220', queue_name='*z*', root_dir=root_dir))

    self.assertEqual(
        [abspath('machine-1/20171220/a.default.20171229-000000Z'),
         abspath('machine-1/20171220/b.default.20171229-000000Z'),
         abspath('machine-1/20171220/e.default.20171229-000000Z')],
        archive.query_machine_archive_file(
            'machine-1', '20171220', queue_name=['*z*', 'def*'],
            root_dir=root_dir))

    self.assertEqual(
        [abspath('machine-1/20171220/a.default.20171229-000000Z'),
         abspath('machine-1/20171220/e.default.20171229-000000Z')],
        archive.query_machine_archive_file(
            'machine-1', '20171220', queue_name=['*z*', 'def*'],
            topic_string=['a', '*e*'], root_dir=root_dir))

  def test_query_archive_file_basic(self):
    root_dir = os.path.join(self._tmpdir, 'archive')
    os.makedirs(root_dir)

    def abspath(relpath):
      return os.path.join(root_dir, relpath)

    file_list = [
        {'relpath': 'machine-0/20171220/a.default.20171229-000000Z'},
        {'relpath': 'machine-0/20171220/b.default.20171229-000000Z'},
        {'relpath': 'machine-0/20171220/c.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/a.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/b.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/c.default.20171229-000000Z',
         'empty_file': True},
        {'relpath': 'machine-1/20171220/d.default.20171229-000000Z',
         'corrupted_file': True},
        {'relpath': 'machine-1/20171220/e.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171220/wrong_filename.20171229-000000Z'}
    ]

    for entry in file_list:
      _make_fake_topic_record(root_dir=root_dir, **entry)

    self.assertEqual(
        [abspath('machine-0/20171220/a.default.20171229-000000Z'),
         abspath('machine-0/20171220/b.default.20171229-000000Z'),
         abspath('machine-0/20171220/c.default.20171229-000000Z')],
        archive.query_archive_file(
            'machine-0', '20171220', root_dir=root_dir))

    self.assertEqual(
        [abspath('machine-0/20171220/a.default.20171229-000000Z'),
         abspath('machine-0/20171220/b.default.20171229-000000Z'),
         abspath('machine-0/20171220/c.default.20171229-000000Z'),
         abspath('machine-1/20171220/a.default.20171229-000000Z'),
         abspath('machine-1/20171220/b.default.20171229-000000Z'),
         abspath('machine-1/20171220/e.default.20171229-000000Z')],
        archive.query_archive_file(
            'machine*', '20171220', root_dir=root_dir))

  def test_iter_archive_file(self):
    root_dir = os.path.join(self._tmpdir, 'archive')
    os.makedirs(root_dir)

    def abspath(relpath):
      return os.path.join(root_dir, relpath)

    file_list = [
        {'relpath': 'machine-0/20171120/a.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171120/b.default.20171229-000000Z'},
        {'relpath': 'machine-0/20171121/c.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171121/a.default.20171229-000000Z'},
        {'relpath': 'machine-0/20171124/b.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171124/c.default.20171229-000000Z',
         'empty_file': True},
        {'relpath': 'machine-0/20171126/d.default.20171229-000000Z',
         'corrupted_file': True},
        {'relpath': 'machine-0/20171202/e.default.20171229-000000Z'},
        {'relpath': 'machine-1/20171202/wrong_filename.20171229-000000Z'}
    ]

    for entry in file_list:
      _make_fake_topic_record(root_dir=root_dir, **entry)

    res = [fp for fp in archive.iter_archive_file(
               datetime.date(2017, 11, 19), 'machine*', root_dir=root_dir)]
    self.assertEqual(
        [abspath('machine-0/20171120/a.default.20171229-000000Z'),
         abspath('machine-1/20171120/b.default.20171229-000000Z'),
         abspath('machine-0/20171121/c.default.20171229-000000Z'),
         abspath('machine-1/20171121/a.default.20171229-000000Z'),
         abspath('machine-0/20171124/b.default.20171229-000000Z'),
         abspath('machine-0/20171202/e.default.20171229-000000Z')],
        res)

    res = [fp for fp in archive.iter_archive_file(
               datetime.date(2017, 11, 24), 'machine*', root_dir=root_dir)]
    self.assertEqual(
        [abspath('machine-0/20171124/b.default.20171229-000000Z'),
         abspath('machine-0/20171202/e.default.20171229-000000Z')],
        res)

    res = [fp for fp in archive.iter_archive_file(
               datetime.date(2017, 12, 2), 'machine*', root_dir=root_dir)]
    self.assertEqual(
        [abspath('machine-0/20171202/e.default.20171229-000000Z')],
        res)

    res = [fp for fp in archive.iter_archive_file(
               datetime.date(2017, 12, 3), 'machine*', root_dir=root_dir)]
    self.assertEqual([], res)


class MultiFileReaderTest(unittest.TestCase):
  def setUp(self):
    self._tmpdir = tempfile.mkdtemp(prefix='test_')

  def tearDown(self):
    shutil.rmtree(self._tmpdir)

  def test_empty(self):
    with archive.MultiFileReader(iter([])) as mf_reader:
      self.assertEqual(None, mf_reader.peek())
      self.assertEqual(None, mf_reader.read())
      self.assertEqual(None, mf_reader.peek())
      self.assertEqual(None, mf_reader.read())

  def _prepare(self, base_ts):
    files = [
        'machine-0/20171220/a.default.20171220-000000Z',
        'machine-0/20171220/b.default.20171220-000000Z',
        'machine-0/20171220/c.default.20171220-000000Z',
        'machine-0/20171220/d.default.20171220-000000Z',
        'machine-0/20171220/e.default.20171220-000000Z',
        'machine-0/20171221/c.default.20171221-000000Z',
        'machine-0/20171221/d.default.20171221-000000Z'
    ]
    files = [os.path.join(self._tmpdir, relpath) for relpath in files]

    writers = []
    for filepath in files:
      writers.append(TopicRecordWriter(filepath))
      dirpath = os.path.dirname(filepath)
      if not os.path.isdir(dirpath):
        os.makedirs(dirpath)

    for i in range(0, 5000):
      idx = i % len(writers)
      writers[idx].write(None, 0, None, base_ts + i * 100, 'record-%d' % i)
    for writer in writers:
      writer.close()
    return files

  def test_basic(self):
    base_ts = 1513848255372063000
    files = self._prepare(base_ts)
    with archive.MultiFileReader(iter(files)) as mf_reader:
      for i in range(0, 5000):
        record = mf_reader.read()
        self.assertEqual(base_ts + i * 100, record.timestamp)
        self.assertEqual((b'record-%d' % i), record.data)

      self.assertEqual(None, mf_reader.peek())
      self.assertEqual(None, mf_reader.read())
      self.assertEqual(None, mf_reader.peek())
      self.assertEqual(None, mf_reader.read())

  @mock_s3
  def test_basic_s3(self):
    base_ts = 1513848255372063000
    files = self._prepare(base_ts)
    _upload_to_s3('test-bucket', 'data', self._tmpdir)

    s3_files = []
    for f in files:
      f = os.path.relpath(f, self._tmpdir)
      s3_files.append('s3://test-bucket/data/%s' % f)

    with archive.MultiFileReader(iter(s3_files)) as mf_reader:
      for i in range(0, 5000):
        record = mf_reader.read()
        self.assertEqual(base_ts + i * 100, record.timestamp)
        self.assertEqual((b'record-%d' % i), record.data)

      self.assertEqual(None, mf_reader.peek())
      self.assertEqual(None, mf_reader.read())
      self.assertEqual(None, mf_reader.peek())
      self.assertEqual(None, mf_reader.read())


class QueueWriterTest(unittest.TestCase):
  def setUp(self):
    self._tmpdir = tempfile.mkdtemp(prefix='test_')

  def tearDown(self):
    shutil.rmtree(self._tmpdir)

  def test_basic(self):
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    today_str = now.strftime('%Y%m%d')
    queue_name = 'test'
    machine = 'test-machine'
    num_topic = 10
    num_record = 1007
    with archive.QueueWriter(queue_name, now, machine=machine,
                             root_dir=self._tmpdir) as writer:
      for seq in range(0, num_record):
        timestamp = archive.to_timestamp_int(now) + seq * 1000
        record = TopicRecord(seq, seq % num_topic, None, timestamp,
                             b'record-%d' % seq)
        writer.write(record)

    for topic_id in range(num_topic):
      filepath = os.path.join(
          self._tmpdir, machine, today_str,
          '0x%016x.%s.%s.gz' % (topic_id, queue_name,
                                now.strftime('%Y%m%d-%H%M%SZ')))
      self.assertTrue(os.path.isfile(filepath))
      reader = TopicRecordReader(filepath)
      topic_seq = 0
      for seq in range(0, num_record):
        if seq % num_topic != topic_id:
          continue
        record = reader.read()
        self.assertTrue(record is not None)
        self.assertEqual(record.queue_seq, seq)
        self.assertEqual(record.topic_id, topic_id)
        self.assertEqual(record.topic_seq, topic_seq)
        self.assertEqual(record.timestamp,
                         archive.to_timestamp_int(now) + seq * 1000)
        self.assertEqual(record.data, b'record-%d' % seq)
        topic_seq += 1
      self.assertEqual(None, reader.read())

  def test_reset_queue(self):
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    today_str = now.strftime('%Y%m%d')

    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y%m%d')

    queue_name = 'test'
    machine = 'test-machine'
    num_topic = 10
    num_record = 1007
    with archive.QueueWriter(queue_name, now, machine=machine,
                             root_dir=self._tmpdir) as writer:
      for seq in range(0, num_record):
        timestamp = archive.to_timestamp_int(now) + seq * 1000
        record = TopicRecord(seq, seq % num_topic, None, timestamp,
                             b'record-%d' % seq)
        writer.write(record)
      for seq in range(num_record, 2 * num_record):
        timestamp = archive.to_timestamp_int(tomorrow) + seq * 1000
        record = TopicRecord(seq, seq % num_topic, None, timestamp,
                             b'record-%d' % seq)
        writer.write(record)

    for topic_id in range(num_topic):
      filepath = os.path.join(
          self._tmpdir, machine, today_str,
          '0x%016x.%s.%s.gz' % (topic_id, queue_name,
                                now.strftime('%Y%m%d-%H%M%SZ')))
      self.assertTrue(os.path.isfile(filepath))
      reader = TopicRecordReader(filepath)
      topic_seq = 0
      for seq in range(0, num_record):
        if seq % num_topic != topic_id:
          continue
        record = reader.read()
        self.assertTrue(record is not None)
        self.assertEqual(record.queue_seq, seq)
        self.assertEqual(record.topic_id, topic_id)
        self.assertEqual(record.topic_seq, topic_seq)
        self.assertEqual(record.timestamp,
                         archive.to_timestamp_int(now) + seq * 1000)
        self.assertEqual(record.data, b'record-%d' % seq)
        topic_seq += 1
      self.assertEqual(None, reader.read())

    for topic_id in range(num_topic):
      filepath = os.path.join(
          self._tmpdir, machine, tomorrow_str,
          '0x%016x.%s.%s.gz' % (topic_id, queue_name,
                                tomorrow.strftime('%Y%m%d-%H%M%SZ')))
      self.assertTrue(os.path.isfile(filepath))
      reader = TopicRecordReader(filepath)
      topic_seq = 0
      for seq in range(num_record, 2 * num_record):
        if seq % num_topic != topic_id:
          continue
        record = reader.read()
        self.assertTrue(record is not None)
        self.assertEqual(record.queue_seq, seq)
        self.assertEqual(record.topic_id, topic_id)
        self.assertEqual(record.topic_seq, topic_seq)
        self.assertEqual(record.timestamp,
                         archive.to_timestamp_int(tomorrow) + seq * 1000)
        self.assertEqual(record.data, b'record-%d' % seq)
        topic_seq += 1
      self.assertEqual(None, reader.read())

  def test_serializer(self):
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    today_str = now.strftime('%Y%m%d')
    queue_name = 'test'
    machine = 'test-machine'
    num_topic = 10
    num_record = 1007
    with archive.QueueWriter(queue_name, now, machine=machine,
                             root_dir=self._tmpdir) as writer:
      for seq in range(0, num_record):
        timestamp = archive.to_timestamp_int(now) + seq * 1000
        record = TopicRecord(seq, seq % num_topic, None, timestamp,
                             {'data': ('record-%d' % seq)})
        writer.write(record)

    for topic_id in range(num_topic):
      filepath = os.path.join(
          self._tmpdir, machine, today_str,
          '0x%016x.%s.%s.gz' % (topic_id, queue_name,
                                now.strftime('%Y%m%d-%H%M%SZ')))
      self.assertTrue(os.path.isfile(filepath))
      reader = TopicRecordReader(filepath)
      topic_seq = 0
      for seq in range(0, num_record):
        if seq % num_topic != topic_id:
          continue
        record = reader.read()
        self.assertTrue(record is not None)
        self.assertEqual(record.queue_seq, seq)
        self.assertEqual(record.topic_id, topic_id)
        self.assertEqual(record.topic_seq, topic_seq)
        self.assertEqual(record.timestamp,
                         archive.to_timestamp_int(now) + seq * 1000)
        self.assertEqual(json.loads(record.data.tobytes()),
                         {'data': ('record-%d' % seq)})
        topic_seq += 1
      self.assertEqual(None, reader.read())


class ArchiveReaderTest(unittest.TestCase):
  def setUp(self):
    self._tmpdir = tempfile.mkdtemp(prefix='test_')

  def tearDown(self):
    shutil.rmtree(self._tmpdir)

  def test_write_read(self):
    begin_time = datetime.datetime.now() - datetime.timedelta(days=30)
    queue_name = 'test'
    machine = 'test-machine'
    num_topic = 19
    num_record = 1000
    ts_step = 600 * 10**9  # 10mins

    with archive.ArchiveWriter(queue_name, begin_time, {}, machine=machine,
                               root_dir=self._tmpdir) as writer:
      for seq in range(0, num_record):
        timestamp = archive.to_timestamp_int(begin_time) + seq * ts_step
        record = TopicRecord(seq, seq % num_topic, None, timestamp,
                             b'record-%d' % seq)
        writer.write(record)

    with archive.ArchiveReader.from_archive(begin_time, machine,
                                            root_dir=self._tmpdir) \
         as reader:
      for seq in range(0, num_record):
        record = reader.read()
        self.assertTrue(record is not None)

      self.assertEqual(None, reader.read())
      self.assertEqual(None, reader.peek())


if __name__ == "__main__":
  unittest.main()
