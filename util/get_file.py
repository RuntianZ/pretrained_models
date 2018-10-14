from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from six.moves import urllib
import tensorflow as tf


def download(directory, filename, source_url):
  """Download (and unzip) a file from the MNIST dataset if not already done."""
  filepath = os.path.join(directory, filename)
  if tf.gfile.Exists(filepath):
    return filepath
  if not tf.gfile.Exists(directory):
    tf.gfile.MakeDirs(directory)
  url = source_url + filename
  print('Downloading %s to %s' % (url, filepath))
  urllib.request.urlretrieve(url, filepath)
  return filepath


def merge_file(fromdir, todir, filename):
  if not os.path.exists(todir):
    os.mkdir(todir)
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