import os

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