import datetime
import json
import sys

from .topic_record import TopicRecordReader, TopicRecordWriter
from .util import get_timestamp


class RecordWriter(object):
  def __init__(self, filename=None):
    default_filename = 'record_%s.gz' % datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    self._filename = filename or default_filename
    self._record_writer = TopicRecordWriter(self._filename)

  def write(self, msg, timestamp=None):
    timestamp = timestamp or get_timestamp()
    if isinstance(msg, (dict, list)):
      msg = json.dumps(msg, default=str)
    self._record_writer.write(None, 0, None, timestamp, msg)
    self._record_writer.flush()


default_record_writer = RecordWriter()
debuginfo_write = default_record_writer.write


def main():
  record_file = sys.argv[1]
  reader = TopicRecordReader(record_file)
  for record in reader.read_records():
    data = json.loads(record.data.tobytes())
    human_readable_ts = datetime.datetime.fromtimestamp(record.timestamp / 1e9)
    msg = {
        "timestamp": record.timestamp,
        "human_readable_timestamp": str(human_readable_ts),
        "data": data,
    }
    print(json.dumps(msg))


if __name__ == '__main__':
  main()
