# Copyright (c) 2020
# Author: xguo

import collections
import functools
import json
import logging
import pandas as pd
import pdb
import sys

from absl import app, flags
from qflow import TopicRecordReader
from datatool import OhlcCalculator

import matplotlib.pyplot as plt
FLAGS = flags.FLAGS


class ShitcoinLogParser(object):
  def __init__(self, filename):
    self._reader = TopicRecordReader(filename)
    self._data = None
    self._book_dict = collections.defaultdict(list)
    self._fill_dict = collections.defaultdict(list)
    self._order_dict = collections.defaultdict(list)
    self._product_list = set()

    self._ohlc_dict = {}
    for interval in [5, 10, 20, 40]:
      self._ohlc_dict[interval] = collections.defaultdict(functools.partial(OhlcCalculator, interval))

    self._current_ts = None
    self._current_product = None

  def parse_content(self):
    for record in self._reader.read_records():
      info = json.loads(record.data.tobytes())
      ts = record.timestamp
      info_type = info.get('type')

      if 'order' in info:
        product = info['order']['product']
      else:
        product = info.get('product') or info.get('symbol')

      if product is None:
        logging.info('info %s', info)
        continue

      self._product_list.add(product)
      self._current_ts = ts
      self._current_product = product

      if info_type == 'book':
        book = self.parse_book(info['data'])
        self._book_dict[product].append(book)
        for ohlc in self._ohlc_dict.values():
          ohlc[product].update(ts, book['mid'])
      elif info_type == 'fill':
        self._fill_dict[product].append(self.parse_fill(info))
      elif info_type == 'order':
        self._order_dict[product].append(self.parse_order(info))
      else:
        pdb.set_trace()

  def parse_book(self, info):
    result = {
        'ts': self._current_ts,
        'product': self._current_product,
        'ask0': info['asks'][0][0],
        'bid0': info['bids'][0][0],
        'mid': info['mid'],
    }
    return result

  def parse_fill(self, info):
    order_side_map = {1: 'BUY', 2: 'SELL'}
    if 'order' in info:
      order_side = order_side_map[info['order']['order_side']]

    result = {
        'ts': self._current_ts,
        'product': self._current_product,
        'fill_price': info['fill_price'],
        'fill_qty': info['fill_qty'],
        'order_side': order_side,
    }
    return result

  def parse_order(self, info):
    result = {
        'ts': self._current_ts,
        'product': self._current_product,
        'buy_price': info['mm']['pass_buy_price'],
        'sell_price': info['mm']['pass_sell_price'],
        #'raw_mid': info['raw_mid_price'],
    }
    return result

  def plot(self):
    product_pairs = collections.defaultdict(dict)
    for prod in self._product_list:
      base = prod.split('.')[0].split('-')[0]
      is_korean = 'KRW' in prod
      if is_korean:
        product_pairs[base]['trade'] = prod
      else:
        product_pairs[base]['ref'] = prod

    logging.info("base product: %s", product_pairs)
    for pp in product_pairs.values():
      trade_prod = pp['trade']
      logging.info("trade product: %s", trade_prod)

      df = pd.DataFrame(self._book_dict[trade_prod])
      df.ts = pd.DatetimeIndex(df.ts)
      plt.plot(df.ts, df.ask0, ':')
      plt.plot(df.ts, df.bid0, ':')
      plt.plot(df.ts, df.mid, ':')

      df = pd.DataFrame(self._order_dict[trade_prod])
      df.ts = pd.DatetimeIndex(df.ts)
      plt.plot(df.ts, df.buy_price)
      plt.plot(df.ts, df.sell_price)

      fills = self._fill_dict[trade_prod]
      if fills:
        df = pd.DataFrame(fills)
        df.ts = pd.DatetimeIndex(df.ts)
        df_buy = df[df.order_side == 'BUY']
        df_sell = df[df.order_side == 'SELL']
        plt.plot(df_buy.ts, df_buy.fill_price, 'o')
        plt.plot(df_sell.ts, df_sell.fill_price, 'o')
        plt.legend(['ask0', 'bid0', 'mid', 'est', 'buy', 'sell', 'fill_buy', 'fill_sell'])
      else:
        plt.legend(['ask0', 'bid0', 'mid', 'est', 'buy', 'sell'])

      plt.title(trade_prod)
      plt.show()

    """
    for pp in product_pairs.values():
      trade_prod = pp['trade']
      ref_prod = pp['ref']
      lengend = []
      for ii, ohlc_dict in self._ohlc_dict.items():
        ohlc = ohlc_dict[trade_prod]
        df = pd.DataFrame([info._asdict() for info in ohlc.data])
        df.timestamp = pd.DatetimeIndex(df.timestamp)
        fn = "%s.%ds.gz" % (trade_prod, ii)
        df.to_pickle(fn)
        #plt.plot(df.timestamp, df.rtn)

        ohlc = ohlc_dict[ref_prod]
        df = pd.DataFrame([info._asdict() for info in ohlc.data])
        df.timestamp = pd.DatetimeIndex(df.timestamp)
        fn = "%s.%ds.gz" % (ref_prod, ii)
        df.to_pickle(fn)
        #plt.plot(df.timestamp, df.rtn)
        #lengend.append("%s_%s" % (trade_prod, ii))
        #lengend.append("%s_%s" % (ref_prod, ii))

    """
      #plt.legend(lengend)
      #plt.title(trade_prod)
      #plt.show()


def main(_):
  filename = sys.argv[1]
  parser = ShitcoinLogParser(filename)
  parser.parse_content()
  parser.plot()


if __name__ == '__main__':
  app.run(main)
