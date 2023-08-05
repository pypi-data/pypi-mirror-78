# Copyright (c) 2020 Presto Labs Pte. Ltd.
# Author: xguo

import sys
import json
import pandas as pd
import matplotlib.pyplot as plt

"""
book_df = pd.read_pickle('book.gz')
symbol_list = list(set(book_df.symbol))
print(json.dumps(symbol_list, indent=2))

ada = book_df[book_df.symbol == 'ADA-USDT.Binance.ADAUSDT']
ada.ask0_price.plot()
ada.bid0_price.plot()
plt.show()
"""

fill_df = pd.read_pickle(sys.argv[1])
print(fill_df.columns)
symbol_list = list(set(fill_df.symbol))
print(json.dumps(symbol_list, indent=2))
link = fill_df[fill_df.symbol == 'ICX-KRW']

df = link[link.fill_qty > 0]
plt.plot(df.timestamp, df.fill_price, marker='.')

df = link[link.fill_qty < 0]
plt.plot(df.timestamp, df.fill_price, marker='.')

plt.legend(['buy', 'sell'])
plt.show()
