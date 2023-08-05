# Copyright (c) 2020
# Author: xguo

import datetime
import json
import logging
import pandas

from qflow import TopicRecordReader

from absl import app, flags

flags.DEFINE_string('oe', None, 'order event file.')


def get_sign(side):
  if 'BUY' in side:
    return +1
  elif 'SELL' in side:
    return -1
  else:
    raise ValueError()


class BaseProcessor(object):
  def __init__(self):
    self._output = []
    self._timestamp = 0

  @property
  def timestamp(self):
    return self._timestamp

  def set_timestamp(self, timestamp):
    assert timestamp >= self._timestamp
    self._timestamp = timestamp

  def is_acceptable(self, data):
    """override this"""
    return True

  def is_empty(self):
    return not bool(self._output)

  def process(self, data):
    self._timestamp = data.get('timestamp') or data['record_timestamp']
    if not self.is_acceptable(data):
      return

    self.process_impl(data)

  def as_dataframe(self):
    return pandas.DataFrame(self._output)

  def to_pickle(self, filename):
    if self.is_empty():
      return
    self.as_dataframe().to_pickle(filename)

  def process_impl(self, data):
    pass


class FillProcessor(BaseProcessor):
  def __init__(self):
    super().__init__()
    self._known_fill_id = set()

  def is_acceptable(self, data):
    if data['data']['type'] != 'ORDER_EVENT':
      return False

    oe = data['data'].get('oe') or data['data']['event']
    if oe['type'] != "ORDER_FILLED":
      return False

    fill_id = oe['fill_id']
    if fill_id in self._known_fill_id:
      logging.info('Duplicated fill id!')
      return False

    return True

  def process_impl(self, data):
    oe = data['data'].get('oe') or data['data']['event']
    fill_id = oe['fill_id']
    self._known_fill_id.add(fill_id)
    info = {
        'symbol': oe['symbol'],
        'fill_price': oe['fill_price'],
        'side': oe['order_side'],
        'fill_qty': oe['fill_qty'] * get_sign(oe['order_side']),
        'timestamp': self.timestamp }
    self._output.append(info)


class BalanceProcessor(BaseProcessor):
  def is_acceptable(self, data):
    if data['data']['type'] != 'BALANCE':
      return False

    balance_info = data['data']['balance']
    if 'each_balance' not in balance_info:
      return False

    return True

  def process_impl(self, data):
    balance_info = data['data']['balance']
    for data in balance_info['each_balance']:
      info = {
          'symbol': data['currency'],
          'timestamp': self.timestamp,
          'net_position': data['total'] }
      self._output.append(info)


class PositionProcessor(BaseProcessor):
  def is_acceptable(self, data):
    if data['data']['type'] != 'POSITION':
      return False

    if 'each_position' not in position_info:
      return False

    return True

  def process_impl(self, data):
    position_info = data['data']['position']
    for data in position_info['each_position']:
      info = {
          'symbol': data['symbol'],
          'timestamp': self.timestamp,
          'net_position': data['net_position'] }
      self._output.append(info)


class BookProcessor(BaseProcessor):
  def is_acceptable(self, data):
    if data['data']['type'] != 'book':
      return False

    return True

  def process_impl(self, data):
    book = data['data']['data']
    asks = book['asks']
    bids = book['bids']
    symbol = data['data']['product']
    info = {
        'symbol': symbol,
        # level 0
        'ask0_price': asks[0][0],
        'ask0_qty': asks[0][1],
        'bid0_price': bids[0][0],
        'bid0_qty': bids[0][1],
        # level 1
        'ask1_price': asks[1][0],
        'ask1_qty': asks[1][1],
        'bid1_price': bids[1][0],
        'bid1_qty': bids[1][1],
    }
    self._output.append(info)


def get_iterator(filename):
  if 'json' in filename:
    with open(filename) as infile:
      data = json.load(infile)
      return data
  else:
    reader = TopicRecordReader(filename)
    return reader


def main_func(_):
  fill = FillProcessor()
  book = BookProcessor()
  pos = PositionProcessor()
  bal = BalanceProcessor()
  for each in get_iterator(flags.FLAGS.oe):
    fill.process(each)
    book.process(each)
    pos.process(each)
    bal.process(each)

  fill.to_pickle('fill.gz')
  book.to_pickle('book.gz')
  pos.to_pickle('pos.gz')
  bal.to_pickle('bal.gz')


def main():
  app.run(main_func)


if __name__ == "__main__":
  app.run(main_func)
