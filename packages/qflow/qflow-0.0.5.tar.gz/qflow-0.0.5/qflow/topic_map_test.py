import unittest

from .topic_map import TopicMap


class TopicMapTest(unittest.TestCase):
  def test_search_topic_string(self):
    topic_map = TopicMap({
        0x0000102030405001: 'topic1',
        0x0000102030405002: 'topic2'
    })

    self.assertEqual(
        'topic1',
        topic_map.search_topic_string(0x0000102030405001))
    self.assertEqual(
        'topic2',
        topic_map.search_topic_string(0x0000102030405002))
    self.assertEqual(
        '0x0000102030405003',
        topic_map.search_topic_string(0x0000102030405003))

  def test_search_topic_id(self):
    topic_map = TopicMap({
        0x0000102030405001: 'aaa',
        0x0000102030405002: 'aab',
        0x0000102030405003: 'ccc'
    })

    self.assertEqual(
        [('aaa', 0x0000102030405001)],
        topic_map.search_topic_id('aaa'))

    self.assertEqual(
        [('aab', 0x0000102030405002)],
        topic_map.search_topic_id('aab'))

    self.assertEqual(
        [('aaa', 0x0000102030405001),
         ('aab', 0x0000102030405002)],
        topic_map.search_topic_id('aa*'))

    self.assertEqual(
        [('aaa', 0x0000102030405001),
         ('aab', 0x0000102030405002),
         ('ccc', 0x0000102030405003)],
        topic_map.search_topic_id('*'))

    self.assertEqual(
        [],
        topic_map.search_topic_id('unknown_topic'))

    self.assertEqual(
        [('0x1234123412341234', 0x1234123412341234)],
        topic_map.search_topic_id('0x1234123412341234'))

    self.assertEqual(
        [('aaa', 0x0000102030405001)],
        topic_map.search_topic_id(0x0000102030405001))

    self.assertEqual(
        [('ccc', 0x0000102030405003)],
        topic_map.search_topic_id(0x0000102030405003))


if __name__ == "__main__":
  unittest.main()
