import unittest

from reader import (
    _ContainerBase,
    MergeReader,
    Reader)


class FakeRecordReader(Reader):
  def __init__(self, record_list):
    self._record_list = record_list
    self._index = 0

  def read(self):
    record = self.peek()
    self._index = min(self._index + 1, len(self._record_list))
    return record

  def peek(self):
    if self._index >= len(self._record_list):
      return None  # EOF.
    return self._record_list[self._index]


class TestContainer(_ContainerBase):
  def query_priority(self):
    if self.reader is None:
      return self.INT64MIN
    record = self.reader.peek()
    if record is None:
      # On EOF, return the lowest number to make it out of pqueue.
      return self.INT64MIN
    return record  # record should be integer


class MergeReaderTest(unittest.TestCase):
  def test_empty(self):
    mreader = MergeReader(TestContainer)
    self.assertEqual(None, mreader.peek())
    self.assertEqual(None, mreader.peek())  # Peek twice.
    self.assertEqual(None, mreader.read())

  def test_single_reader(self):
    mreader = MergeReader(TestContainer)
    reader = FakeRecordReader([0, 1, 2, 3, 4])
    mreader.add_reader(reader)

    for i in range(0, 5):
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.peek())  # Peek twice.
      self.assertEqual(i, mreader.read())

    self.assertEqual(None, mreader.peek())
    self.assertEqual(None, mreader.read())

  def test_multi_reader_1(self):
    mreader = MergeReader(TestContainer)
    reader_1 = FakeRecordReader([1, 3, 5, 7, 9])
    mreader.add_reader(reader_1)
    reader_2 = FakeRecordReader([2, 4, 6, 8, 10, 11, 12])
    mreader.add_reader(reader_2)

    for i in range(1, 13):
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.peek())  # Peek twice.
      self.assertEqual(i, mreader.read())

    self.assertEqual(None, mreader.peek())
    self.assertEqual(None, mreader.read())

  def test_multi_reader_2(self):
    mreader = MergeReader(TestContainer)
    reader_1 = FakeRecordReader([1, 2, 3, 4, 5])
    mreader.add_reader(reader_1)
    for i in [1, 2, 3]:
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.read())

    reader_2 = FakeRecordReader([2, 3, 6, 7])
    mreader.add_reader(reader_2)
    for i in [2, 3, 4, 5, 6, 7]:
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.read())

    self.assertEqual(None, mreader.peek())
    self.assertEqual(None, mreader.read())

  def test_eof_callback(self):
    def HandleEOF(reader):
      raise EOFError(reader)

    mreader = MergeReader(TestContainer)
    reader_1 = FakeRecordReader([1, 3, 5, 7, 9])
    mreader.add_reader(reader_1, HandleEOF)
    reader_2 = FakeRecordReader([2, 4, 6, 8, 10, 11, 12])
    mreader.add_reader(reader_2, HandleEOF)

    for i in range(1, 10):
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.read())

    with self.assertRaises(EOFError) as ex:
      mreader.peek()  # reader_1 eof_callback is called.
    self.assertEqual(reader_1, ex.exception.args[0])

    self.assertEqual(10, mreader.peek())
    self.assertEqual(10, mreader.read())

    for i in range(11, 13):
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.read())

    with self.assertRaises(EOFError) as ex:
      mreader.peek()  # reader_1 eof_callback is called.
    self.assertEqual(reader_2, ex.exception.args[0])

    self.assertEqual(None, mreader.peek())
    self.assertEqual(None, mreader.read())

  def test_remove_reader(self):
    mreader = MergeReader(TestContainer)
    reader_1 = FakeRecordReader([1, 2, 3, 4, 5])
    mreader.add_reader(reader_1)
    for i in [1, 2, 3]:
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.read())

    reader_2 = FakeRecordReader([2, 3, 6, 7])
    mreader.add_reader(reader_2)
    for i in [2, 3]:
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.read())
    mreader.remove_reader(reader_2)

    for i in [4, 5]:
      self.assertEqual(i, mreader.peek())
      self.assertEqual(i, mreader.read())

    self.assertEqual(None, mreader.peek())
    self.assertEqual(None, mreader.read())

  def test_peek_after_add(self):
    mreader = MergeReader(TestContainer)
    self.assertEqual(None, mreader.peek())

    reader_1 = FakeRecordReader([2, 3, 4])
    mreader.add_reader(reader_1)
    self.assertEqual(2, mreader.peek())

    reader_2 = FakeRecordReader([1])
    mreader.add_reader(reader_2)
    self.assertEqual(1, mreader.peek())

  def test_peek_after_remove(self):
    mreader = MergeReader(TestContainer)
    reader_1 = FakeRecordReader([2, 3, 4])
    mreader.add_reader(reader_1)
    reader_2 = FakeRecordReader([1])
    mreader.add_reader(reader_2)
    self.assertEqual(1, mreader.peek())

    mreader.remove_reader(reader_2)
    self.assertEqual(2, mreader.peek())
    mreader.remove_reader(reader_1)
    self.assertEqual(None, mreader.peek())


if __name__ == "__main__":
  unittest.main()
