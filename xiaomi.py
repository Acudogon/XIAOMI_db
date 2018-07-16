from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import os
import pandas

earnings = 5361876000
EPS = 0.21
sharesoutstanding = 25090311730.0

# hector	->	6HBVTBNERFR7WLAJ
# herry		->	1DPT9DATB5J89COD
# zhao		->	E1TIY33M6TV277LO
keys = ['6HBVTBNERFR7WLAJ','1DPT9DATB5J89COD','E1TIY33M6TV277LO']
# ticker = 1810.hk
ts = TimeSeries(key=keys[0],output_format='pandas')
data,_ = ts.get_daily_adjusted(symbol='1810.hk', outputsize='compact')
# clean N/A data
data = data[data['1. open'] != 0.0]
# load P/E
data['P/E'] = data['5. adjusted close'] / EPS

# load money volumn
# hkd money volumn
data['HKD volume'] = data['6. volume'] * data['5. adjusted close']
# usd money volumn
hkdUsd = ForeignExchange(key=keys[0])
usd_hkd_data,_ = hkdUsd.get_currency_exchange_rate(from_currency='HKD', to_currency='USD')
usd_hkd = usd_hkd_data['5. Exchange Rate']
data['USD volume'] = data['HKD volume'] * float(usd_hkd)

# rmb money volume
# hkdRmb = ForeignExchange(key=keys[0])
# rmb_hkd_data, _ = hkdRmb.get_currency_exchange_rate(from_currency='HKD', to_currency='RMB')
# rmb_hkd = usd_hkd_data['5. Exchange Rate']
# data['RMB volume'] = data['HKD volume'] * float(rmb_hkd)

# Market Cap(USD)
data['Market Cap(USD)'] = data['5. adjusted close'] * sharesoutstanding * float(usd_hkd)

# Save as CSV
path = os.getcwd().replace('\\','/')+'/01810.csv'
data.to_csv(path)