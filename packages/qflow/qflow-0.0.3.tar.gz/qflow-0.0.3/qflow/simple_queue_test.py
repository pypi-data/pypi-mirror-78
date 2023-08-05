import datetime
import shutil
import tempfile
import threading
import time
import unittest

import archive as archive
from util import get_timestamp
from simple_queue import SimpleQueue, ThreadedQueueArchiver


class ListAppender(object):
  def __init__(self, records):
    self._records = records

  def on_error(self, error):
    self._records.append(error)

  def on_topic_record(self, record):
    self._records.append(record)


class SimpleQueueTest(unittest.TestCase):
  def test_basic(self):
    queue = SimpleQueue()
    writers = []
    for i in range(17):
      writers.append(queue.get_writer(topic_id=1000+i))

    records_1 = []
    reader_1 = queue.get_reader(ListAppender(records_1))
    records_2 = []
    reader_2 = queue.get_reader(ListAppender(records_2))

    base_ts = get_timestamp()
    for i in range(0, 10000):
      writers[i % len(writers)].write(base_ts + i * 1000, b'record-%d' % i)

    for idx, record in enumerate(records_1):
      self.assertEqual(idx, record.queue_seq)
      self.assertEqual(1000 + (idx % len(writers)), record.topic_id)
      self.assertEqual(int(idx / len(writers)), record.topic_seq)
      self.assertEqual(base_ts + idx * 1000, record.timestamp)
      self.assertEqual(b'record-%d' % idx, record.data)

    for idx, record in enumerate(records_2):
      self.assertEqual(idx, record.queue_seq)
      self.assertEqual(1000 + (idx % len(writers)), record.topic_id)
      self.assertEqual(int(idx / len(writers)), record.topic_seq)
      self.assertEqual(base_ts + idx * 1000, record.timestamp)
      self.assertEqual(b'record-%d' % idx, record.data)

  def test_reader_stop(self):
    queue = SimpleQueue()
    writer = queue.get_writer(topic_id=1000)

    records_1 = []
    reader_1 = queue.get_reader(ListAppender(records_1))
    records_2 = []
    reader_2 = queue.get_reader(ListAppender(records_2))

    writer.write(get_timestamp(), 'record-0')
    self.assertEqual(1, len(records_1))
    self.assertEqual(1, len(records_2))

    reader_1.stop()
    writer.write(get_timestamp(), 'record-1')
    self.assertEqual(1, len(records_1))
    self.assertEqual(2, len(records_2))

    writer.write(get_timestamp(), 'record-2')
    self.assertEqual(1, len(records_1))
    self.assertEqual(3, len(records_2))

  def test_threaded_reader(self):
    queue = SimpleQueue()
    writers = []
    for i in range(17):
      writers.append(queue.get_writer(topic_id=1000+i))

    records_1 = []
    reader_1 = queue.get_threaded_reader(ListAppender(records_1))
    records_2 = []
    reader_2 = queue.get_threaded_reader(ListAppender(records_2))

    def worker(reader):
      reader.start()

    t1 = threading.Thread(target=worker, args=(reader_1,))
    t1.start()

    t2 = threading.Thread(target=worker, args=(reader_2,))
    t2.start()

    base_ts = get_timestamp()
    for i in range(0, 10):
      writers[i % len(writers)].write(base_ts + i * 1000, b'record-%d' % i)

    reader_1.stop()
    reader_2.stop()
    t1.join()
    t2.join()

    for idx, record in enumerate(records_1):
      self.assertEqual(idx, record.queue_seq)
      self.assertEqual(1000 + (idx % len(writers)), record.topic_id)
      self.assertEqual(int(idx / len(writers)), record.topic_seq)
      self.assertEqual(base_ts + idx * 1000, record.timestamp)
      self.assertEqual(b'record-%d' % idx, record.data)

    for idx, record in enumerate(records_2):
      self.assertEqual(idx, record.queue_seq)
      self.assertEqual(1000 + (idx % len(writers)), record.topic_id)
      self.assertEqual(int(idx / len(writers)), record.topic_seq)
      self.assertEqual(base_ts + idx * 1000, record.timestamp)
      self.assertEqual(b'record-%d' % idx, record.data)

  def test_threaded_reader_timeout(self):
    queue = SimpleQueue()
    reader = queue.get_threaded_reader(None)
    with self.assertRaises(TimeoutError):
      reader.read_once(timeout=datetime.timedelta(seconds=0.1))

    writer = queue.get_writer(topic_id=1000)
    def write():
      for i in range(0, 50):
        writer.write(get_timestamp(), b'record')
        time.sleep(0.01)
    t = threading.Thread(target=write)
    t.start()

    t1 = datetime.datetime.now()
    reader.start(duration=datetime.timedelta(seconds=0.3))
    t2 = datetime.datetime.now()
    self.assertLess(t2 - t1, datetime.timedelta(seconds=0.4))
    t.join()


class ThreadedQueueArchiverTest(unittest.TestCase):
  def setUp(self):
    self._tmpdir = tempfile.mkdtemp(prefix='test_')

  def tearDown(self):
    shutil.rmtree(self._tmpdir)

  def test_basic(self):
    queue = SimpleQueue('test-queue')
    reader = queue.get_threaded_reader(None)
    archiver = ThreadedQueueArchiver(reader, root_dir=self._tmpdir)

    writers = []
    for i in range(17):
      writers.append(queue.get_writer(topic_id=1000+i))

    base_ts = get_timestamp()
    for i in range(0, 10000):
      writers[i % len(writers)].write(base_ts + i * 1000, b'record-%d' % i)

    time.sleep(1)
    archiver.stop()

    reader = archive.ArchiveReader.from_archive(
        base_ts, root_dir=self._tmpdir)
    with reader:
      for i in range(0, 10000):
        record = reader.read()
        self.assertTrue(record is not None)
        self.assertEqual(i, record.queue_seq)
        self.assertEqual(1000 + (i % len(writers)), record.topic_id)
        self.assertEqual(int(i / len(writers)), record.topic_seq)
        self.assertEqual(base_ts + i * 1000, record.timestamp)
        self.assertEqual(b'record-%d' % i, record.data)
      self.assertEqual(None, reader.read())


if __name__ == "__main__":
  unittest.main()
