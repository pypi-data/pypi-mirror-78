# Copyright (c) 2020 Presto Labs Pte. Ltd.
# Author: xguo

import logging
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt


class Analyser(object):
  def __init__(self):
    self._data = {
        'book': None,
        'fill': None,
        'balance': None,
        'pnl_balance': None,
        'position': None
    }
    self._logger = logging.getLogger('Analyser')
    self.load_files()

  def load_files(self):
    for key in list(self._data.keys()):
      fn = "%s.gz" % key
      try:
        self._data[key] = pd.read_pickle(fn)
      except FileNotFoundError:
        self._logger.info('%s not found!' % fn)

    for key, df in self._data.items():
      if df is None:
        continue

      if not hasattr(df, 'symbol'):
        continue

      symbol_list = list(set(df.symbol))
      json_str = json.dumps(symbol_list, indent=2)
      self._logger.info("%s: %s", key, json_str)

  def plot_fill(self, symbol):
    fill_df = self._data['fill']
    book_df = self._data['book']

    prod_df = fill_df[fill_df.symbol == symbol.split('.')[0]]
    buy_df = prod_df[prod_df.fill_qty > 0]
    sell_df = prod_df[prod_df.fill_qty < 0]

    plt.figure(figsize=(20, 20), dpi=600)
    ax0 = plt.subplot(311)
    ax0.plot(book_df.timestamp, book_df.ask0_price, marker=':')
    ax0.plot(book_df.timestamp, book_df.bid0_price, marker=':')
    ax0.plot(sell_df.timestamp, sell_df.fill_price, marker='.')
    ax0.plot(buy_df.timestamp, buy_df.fill_price, marker='.')

    ax1 = plt.subpllot(312, sharex=ax0)
    ax1.plot(prod.timestamp, prod_df.fill_qty.cumsum())

    ax2= plt.subpllot(312, sharex=ax0)
    ax2.plot(prod.timestamp, prod_df.fill_qty.cumsum())

    (fill_df.fill_price * fill_df.fill_qty).cumsum()
    plt.legend(['ask0', 'bid0', 'sell', 'buy'])
    plt.savefig('%s_pnl.svg' % symbol)

  def plot(self):
    pnl_balance = self._data['pnl_balance']
    plt.plot(pnl_balance.timestamp, pnl_balance.total)
    plt.show()


def main():
  analyser = Analyser()
  analyser.plot()


if __name__ == '__main__':
  main()
