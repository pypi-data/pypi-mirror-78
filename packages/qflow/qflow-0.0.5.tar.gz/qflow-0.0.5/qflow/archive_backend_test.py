import os
import shutil
import tempfile
import unittest

import boto3
from moto import mock_s3

from . import archive_backend as backend


class LocalArchiveBackendTest(unittest.TestCase):
  def setUp(self):
    self._tmpdir = tempfile.mkdtemp(prefix='test_')

  def tearDown(self):
    shutil.rmtree(self._tmpdir)

  def test_iter_file_dir(self):
    files = []
    dirs = []
    for idx in range(0, 100):
      filepath = os.path.join(self._tmpdir, 'f-%d' % idx)
      with open(filepath, 'w') as f:
        pass
      files.append(filepath)

      dirpath = os.path.join(self._tmpdir, 'd-%d' % idx)
      os.mkdir(dirpath)
      dirs.append(dirpath)

    local = backend.LocalArchiveBackend()
    res_f = sorted([f for f in local.iter_file(self._tmpdir)])
    self.assertEqual(sorted(files), res_f)

    res_d = sorted([d for d in local.iter_dir(self._tmpdir)])
    self.assertEqual(sorted(dirs), res_d)


class S3ArchiveBackendTest(unittest.TestCase):
  def test_decompose_s3path(self):
    bucket, key = backend.S3ArchiveBackend._decompose_s3path(
        's3://test-bucket/a/b/c/d/e')
    self.assertEqual('test-bucket', bucket)
    self.assertEqual('a/b/c/d/e', key)

    bucket, key = backend.S3ArchiveBackend._decompose_s3path(
        's3://bucket-only')
    self.assertEqual('bucket-only', bucket)
    self.assertEqual('', key)

    with self.assertRaises(ValueError):
      backend.S3ArchiveBackend._decompose_s3path('a/b/c')

  @mock_s3
  def test_iter_file(self):
    # Prepare data
    test_client = boto3.client('s3')
    test_client.create_bucket(Bucket='test-bucket')
    keys = []
    for idx in range(0, 2100):  # Truncated two times.
      key = 'data/f-%d' % idx
      test_client.put_object(Bucket='test-bucket', Key=key, Body=b'body')
      keys.append('s3://test-bucket/%s' % key)

    # Test
    s3 = backend.S3ArchiveBackend()
    res = sorted([k for k in s3.iter_file('s3://test-bucket/data')])
    self.assertEqual(sorted(keys), res)

  @mock_s3
  def test_iter_dir(self):
    # Prepare data
    test_client = boto3.client('s3')
    test_client.create_bucket(Bucket='test-bucket')
    keys = []
    for idx in range(0, 2100):  # Maybe truncated.
      key = 'data/d-%d/f' % idx
      test_client.put_object(Bucket='test-bucket', Key=key, Body=b'body')
      keys.append('s3://test-bucket/%s/' % os.path.dirname(key))

    # Test
    s3 = backend.S3ArchiveBackend()
    res = sorted([k for k in s3.iter_dir('s3://test-bucket/data')])
    self.assertEqual(sorted(keys), res)

  @mock_s3
  def test_open(self):
    # Prepare data
    test_client = boto3.client('s3')
    test_client.create_bucket(Bucket='test-bucket')
    key = 'data/f'
    test_client.put_object(Bucket='test-bucket', Key=key, Body=b'body')

    # Test
    s3 = backend.S3ArchiveBackend()
    with  s3.open('s3://test-bucket/data/f', 'rb') as f:
      self.assertEqual(b'body', f.read())

    # No key
    with self.assertRaises(FileNotFoundError):
      s3.open('s3://test-bucket/1234', 'rb')

    # No bucket
    with self.assertRaises(FileNotFoundError):
      s3.open('s3://invalid-bucket/1234', 'rb')

if __name__ == "__main__":
  unittest.main()
