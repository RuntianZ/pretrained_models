from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from six.moves import urllib


def download(directory, filename, source_url):
  filepath = os.path.join(directory, filename)
  if os.path.isfile(filepath):
    return filepath
  if not os.path.isdir(directory):
    os.makedirs(directory)
  url = source_url.format(filename)
  print('Downloading %s to %s' % (url, filepath))
  urllib.request.urlretrieve(url, filepath)
  return filepath


def merge(fromdir, todir, filename):
  if not os.path.exists(todir):
    os.makedirs(todir)
  else:
    for fname in os.listdir(todir):
      os.remove(os.path.join(todir, fname))

  tofile = os.path.join(todir, filename)
  partnum = 1
  with open(tofile, 'wb') as fout:

    while True:
      fname = os.path.join(fromdir, ('{}.part{}'.format(filename, partnum)))
      if not os.path.exists(fname):
        break

      with open(fname, 'rb') as fin:
        chunk = fin.read()
        fout.write(chunk)
      partnum += 1
    partnum -= 1

  return partnum


def split(fromdir, todir, filename, chunksize=20000000):
  if not os.path.exists(todir):
    os.mkdir(todir)
  else:
    for fname in os.listdir(todir):
      os.remove(os.path.join(todir, fname))

  fromfile = os.path.join(fromdir, filename)
  partnum = 0
  with open(fromfile, 'rb') as fin:
    while True:
      chunk = fin.read(chunksize)
      if not chunk:
        break

      partnum += 1
      fname = os.path.join(todir, ('{}.part{}'.format(filename, partnum)))
      with open(fname, 'wb') as fout:
        fout.write(chunk)

  return partnum
