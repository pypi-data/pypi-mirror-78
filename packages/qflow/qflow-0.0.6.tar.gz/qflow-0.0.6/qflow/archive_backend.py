import io
import logging
import os
import types
from typing import Iterable, Iterator, Optional, Tuple, Union


def get_archive_backend_type(ref_path: str):
  if ref_path and ref_path.startswith('s3://'):
    return 's3'
  else:
    return 'local'


def get_archive_backend(ref_path: str, **kwargs):
  archive_backend_type = get_archive_backend_type(ref_path)
  return _ARCHIVE_BACKEND_MAP[archive_backend_type](**kwargs)


class ArchiveBackendBase(object):
  def close_backend(self):
    pass

  def normpath(self, path: str):
    return path

  def iter_file(self, path: str) -> Union[Iterable, Iterator]:
    raise NotImplemented()

  def iter_dir(self, path: str) -> Union[Iterable, Iterator]:
    raise NotImplemented()

  def open(self, path: str, mode: Optional[str]):
    raise NotImplemented()


class LocalArchiveBackend(ArchiveBackendBase):
  def __init__(self, logger=None, **kwargs):
    if kwargs:
      raise ValueError()

  def iter_file(self, path: str) -> Union[Iterable, Iterator]:
    if not os.path.isdir(path):
      return
    for filename in os.listdir(path):
      filepath = os.path.join(path, filename)
      if os.path.isfile(filepath):
        yield filepath

  def iter_dir(self, path: str) -> Union[Iterable, Iterator]:
    if not os.path.isdir(path):
      return
    for dirname in os.listdir(path):
      dirpath = os.path.join(path, dirname)
      if os.path.isdir(dirpath):
        yield dirpath

  def open(self, path: str, mode: Optional[str]):
    return open(path, mode)

  def normpath(self, path: str):
    return os.path.normpath(os.path.expanduser(path))


class StreamingBodyWrapper(object):
  def __init__(self, fileobj):
    self._fileobj = fileobj

  def __del__(self):
    self.close()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.close()

  def readable(self):
    return True

  def flush(self):
    pass

  @property
  def closed(self):
    return self._fileobj == None

  def close(self, *args, **kwargs):
    if self._fileobj is not None:
      self._fileobj.close(*args, **kwargs)
      self._fileobj = None

  def read(self, *args, **kwargs):
    try:
      return self._fileobj.read(*args, **kwargs)
    except ValueError:
      return None
    except EOFError:
      return None

  def readinto(self, b):
    length = len(b)
    data = self.read(length)
    if data is None:
      return None
    b[:len(data)] = data
    return len(data)


class S3ArchiveBackend(ArchiveBackendBase):
  def __init__(self, s3_client=None, logger=None, **kwargs):
    import boto3
    self._logger = logger or logging.getLogger(__name__)
    self._client = s3_client or boto3.client('s3', **kwargs)

  @staticmethod
  def _decompose_s3path(path: str) -> Tuple[str, str]:
    # Return tuple of bucket and key.
    if not path.startswith('s3://'):
      raise ValueError('Invalid path')
    path = path[5:]  # Remove 's3://'
    first_slash_idx = path.find('/')
    if first_slash_idx == -1:
      return (path, '')
    bucket = path[:first_slash_idx]
    key = path[first_slash_idx+1:]
    return (bucket, key)

  def iter_file(self, path: str) -> Union[Iterable, Iterator]:
    bucket, prefix = self._decompose_s3path(path)
    if not prefix.endswith('/'):
      prefix += '/'

    next_token = None
    while True:
      args = dict(Bucket=bucket, Prefix=prefix, Delimiter='/')
      if next_token:
        args['ContinuationToken'] = next_token
      res = self._client.list_objects_v2(**args)
      contents = res.get('Contents', [])
      for content in contents:
        try:
          key = content['Key']
          yield 's3://%s/%s' % (bucket, key)
        except KeyError:
          self._logger.error('Invalid key is returned: %s' % path)
          continue
      truncated = res.get('IsTruncated', False)
      if not truncated:
        return
      next_token = res.get('NextContinuationToken', None)

  def iter_dir(self, path: str) -> Union[Iterable, Iterator]:
    bucket, prefix = self._decompose_s3path(path)
    if not prefix.endswith('/'):
      prefix += '/'

    known_prefix = set()
    next_token = None
    while True:
      args = dict(Bucket=bucket, Prefix=prefix, Delimiter='/')
      if next_token:
        args['ContinuationToken'] = next_token
      res = self._client.list_objects_v2(**args)
      common_prefixes = res.get('CommonPrefixes', [])
      for common_prefix in common_prefixes:
        try:
          prefix = common_prefix['Prefix']
          if prefix not in known_prefix:
            yield 's3://%s/%s' % (bucket, prefix)
            known_prefix.add(prefix)
        except KeyError:
          self._logger.error('Invalid prefix is returned: %s' % path)
          continue
      truncated = res.get('IsTruncated', False)
      if not truncated:
        return
      next_token = res.get('NextContinuationToken', None)

  def open(self, path: str, mode: Optional[str]):
    from botocore.exceptions import ClientError
    if mode != 'rb':
      raise NotImplemented('Unsupported mode: %s' % mode)
    bucket, key = self._decompose_s3path(path)
    try:
      s3_obj = self._client.get_object(Bucket=bucket, Key=key)
    except ClientError as e:
      if e.response['Error']['Code'] == 'NoSuchKey':
        raise FileNotFoundError()
      elif e.response['Error']['Code'] == 'NoSuchBucket':
        raise FileNotFoundError()
      raise

    return io.BufferedReader(StreamingBodyWrapper(s3_obj.get('Body', None)),
                             128 * 1024)


_ARCHIVE_BACKEND_MAP = {
    'local': LocalArchiveBackend,
    's3': S3ArchiveBackend
}
