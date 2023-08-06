# Copyright (c) 2020
# Author: xguo

import collections
import datetime
import glob
import re
import os


def get_file_date(filename):
  """ smm_record_1598486442102095104.gz """
  result = re.findall('1[0-9]{18}', filename)
  assert(len(result) == 1)
  dt = datetime.datetime.fromtimestamp(int(result[0]) / 1e9)
  return dt.strftime('%Y%m%d')


def main():
  fn_dict = collections.defaultdict(list)
  file_list = glob.glob('*.gz')
  for fn in file_list:
    date = get_file_date(fn)
    fn_dict[date].append(fn)

  for date, files in fn_dict.items():
    os.mkdir(date)
    os.mkdir(os.path.join(date, 'prod'))
    os.mkdir(os.path.join(date, 'sim'))
    for f in files:
      if 'sim' in f:
        os.rename(f, os.path.join(date, 'sim', f))
      else:
        os.rename(f, os.path.join(date, 'prod', f))


if __name__ == "__main__":
  main()
