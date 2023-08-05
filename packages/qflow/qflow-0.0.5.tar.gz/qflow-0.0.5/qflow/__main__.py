import datetime
import glob
import json
import os
import sys

from absl import (flags, app)

from .topic_record import TopicRecordReader, TopicRecordWriter
from .util import get_timestamp


flags.DEFINE_boolean('merge', False, 'merge files')
flags.DEFINE_string('record', None, 'record file')


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


def dump_file(record_file):
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


def merge_files(file_list):
  writer = RecordWriter("new_%s" % os.path.basename(file_list[0]))
  for fn in file_list:
    reader = TopicRecordReader(fn)
    for record in reader.read_records():
      writer.write(record.data.tobytes(), record.timestamp)


def main_func(_):
  record_file = flags.FLAGS.record
  if os.path.isfile(record_file):
    dump_file(record_file)
  elif flags.FLAGS.merge:
    file_list = sorted(glob.glob("%s/*.gz" % record_file))
    merge_files(file_list)
  else:
    print('Wrong flags!!!')



def main():
  app.run(main_func)


if __name__ == '__main__':
  main()
