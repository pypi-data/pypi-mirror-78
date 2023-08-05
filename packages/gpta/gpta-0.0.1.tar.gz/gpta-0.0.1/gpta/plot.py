# Copyright (c) 2020 Presto Labs Pte. Ltd.
# Author: xguo

import json
import pandas as pd
import matplotlib.pyplot as plt

book_df = pd.read_pickle('book.gz')
symbol_list = list(set(book_df.symbol))
print(json.dumps(symbol_list, indent=2))

ada = book_df[book_df.symbol == 'ADA-USDT.Binance.ADAUSDT']
ada.ask0_price.plot()
ada.bid0_price.plot()
plt.show()
