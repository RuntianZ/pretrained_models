from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from six.moves import urllib
import tempfile


def download(url, localpath):
  """Download (and unzip) a file from the MNIST dataset if not already done."""
  if not os.path.isdir(os.path.dirname(os.path.abspath(localpath))):
    os.makedirs(os.path.dirname(os.path.abspath(localpath)))
  print('Downloading %s to %s' % (url, localpath))
  urllib.request.urlretrieve(url, localpath)


def merge_file(fromfile, tofile):
  if not os.path.isdir(os.path.dirname(os.path.abspath(tofile))):
    os.makedirs(os.path.dirname(os.path.abspath(tofile)))
  partnum = 1
  with open(tofile, 'wb') as fout:
    while True:
      fname = '{}.part{}'.format(fromfile, partnum)
      if not os.path.exists(fname):
        break
      with open(fname, 'rb') as fin:
        chunk = fin.read()
        fout.write(chunk)
      partnum += 1
    partnum -= 1
  return partnum


def download_and_merge(url, localpath, part_num):
  tmp = tempfile.TemporaryDirectory()
  if part_num == 0:
    download(url, localpath)
  else:
    for i in range(part_num):
      file_url = '{}.part{}'.format(url, i + 1)
      local_pth = '{}/tmp.part{}'.format(tmp.name, i + 1)
      download(file_url, local_pth)
    merge_file('{}/tmp'.format(tmp.name), localpath)


def split(fromfile, tofile, chunksize=20000000):
  todir = os.path.dirname(os.path.abspath(tofile))
  if not os.path.isdir(todir):
    os.makedirs(todir)
  partnum = 0
  with open(fromfile, 'rb') as fin:
    while True:
      chunk = fin.read(chunksize)
      if not chunk:
        break
      partnum += 1
      fname = '{}.part{}'.format(tofile, partnum)
      with open(fname, 'wb') as fout:
        fout.write(chunk)
  return partnum
