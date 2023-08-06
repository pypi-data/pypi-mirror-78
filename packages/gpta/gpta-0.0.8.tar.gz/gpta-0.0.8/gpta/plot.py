# Copyright (c)
# Author: xguo

import json
import logging
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

from absl import flags, app


flags.DEFINE_string('symbol', None, 'symbol')


class Analyser(object):
  def __init__(self):
    self._data = {
        'book': None,
        'fill': None,
        'order': None,
        'balance': None,
        'pnl_balance': None,
        'position': None,
    }
    self._symbol_list = None
    self._logger = logging.getLogger('Analyser')
    self.load_files()

  def load_files(self):
    for key in list(self._data.keys()):
      fn = '%s.gz' % key
      if not os.path.isfile(fn):
        self._logger.info('%s not found!' % fn)
        continue
      df = pd.read_pickle(fn)
      self._data[key] = df

    for key, df in self._data.items():
      if df is None:
        continue

      try:
        symbol_list = list(set(df.symbol))
        json_str = json.dumps(symbol_list, indent=2)
        self._logger.info("%s:\n%s", key, json_str)
      except AttributeError:
        continue

      if key == 'book':
        self._symbol_list = symbol_list

  @property
  def symbol_list(self):
    return self._symbol_list

  def plot_fill(self, symbol):
    simple_symbol = symbol.split('.')[0]

    fill_df = self._data['fill']
    book_df = self._data['book']
    order_df = self._data['order']

    book_df = book_df[book_df.symbol == symbol]

    fill_df = fill_df[fill_df.symbol == simple_symbol]
    buy_df = fill_df[fill_df.fill_qty > 0]
    sell_df = fill_df[fill_df.fill_qty < 0]

    order_df = order_df[order_df.symbol == simple_symbol]

    plt.figure()
    ax0 = plt.subplot(211)
    plt.title(symbol)
    # book
    ax0.plot(book_df.timestamp, book_df.ask0_price, color='lightpink', marker='.', alpha=0.3)
    ax0.plot(book_df.timestamp, book_df.bid0_price, color='palegreen', marker='.', alpha=0.3)

    # avg buy/sell price
    avg_sell_price = (sell_df.fill_price * sell_df.fill_qty.abs()).cumsum() / sell_df.fill_qty.abs().cumsum()
    avg_buy_price = (buy_df.fill_price * buy_df.fill_qty.abs()).cumsum() / buy_df.fill_qty.abs().cumsum()
    ax0.plot(sell_df.timestamp, avg_sell_price, alpha=0.4, color='lightpink')
    ax0.plot(buy_df.timestamp, avg_buy_price, alpha=0.4, color='palegreen')

    # order
    sell_order_df = order_df[order_df.order_qty < 0]
    buy_order_df = order_df[order_df.order_qty > 0]
    ax0.plot(sell_order_df.timestamp, sell_order_df.order_price, color='brown', marker='.', alpha=0.4)
    ax0.plot(buy_order_df.timestamp, buy_order_df.order_price, color='black', marker='.', alpha=0.4)

    # fill buy/sell price
    ax0.plot(sell_df.timestamp, sell_df.fill_price, color='red', marker='v')
    ax0.plot(buy_df.timestamp, buy_df.fill_price, color='blue', marker='^')

    # pnl
    ax1 = ax0.twinx()
    pnl = -(fill_df.fill_price * fill_df.fill_qty).cumsum() + fill_df.fill_qty.cumsum() * fill_df.fill_price
    ax1.plot(fill_df.timestamp, pnl)

    ax2 = plt.subplot(212, sharex=ax0)
    ax2.plot(fill_df.timestamp, fill_df.fill_qty.cumsum())

    plt.show()

  def plot(self):
    pnl_balance = self._data['pnl_balance']
    plt.plot(pnl_balance.timestamp, pnl_balance.total)
    plt.show()


def main_func(_):
  analyser = Analyser()
  if not flags.FLAGS.symbol:
    return

  analyser.plot_fill(flags.FLAGS.symbol)


def main():
  app.run(main_func)


if __name__ == '__main__':
  main()
