from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
import os
import pandas
import numpy

earnings = 5361876000
EPS = 0.21
sharesoutstanding = 25090311730

#symbols = ['1810.hk']
ts = TimeSeries(key='6HBVTBNERFR7WLAJ',output_format='pandas')
data, meta_data = ts.get_daily_adjusted(symbol = '1810.hk',outputsize ='compact')
#clean NA data
data = data[data['1. open']!= 0.0]
#load P/E
data['P/E'] = data['5. adjusted close']/EPS

#load money volumn
#hkd money volumn
data['HKD volume'] = data['6. volume']*data['5. adjusted close']
#usd money volumn
cc = ForeignExchange(key='6HBVTBNERFR7WLAJ')
usd_hkd_data, _ = cc.get_currency_exchange_rate(from_currency = 'HKD', to_currency = 'USD')
usd_hkd = usd_hkd_data['5. Exchange Rate']
data['USD volume'] = data['HKD volume']*float(usd_hkd)

#rmb money volume
rmb_hkd_data, _ = cc.get_currency_exchange_rate(from_currency = 'HKD', to_currency = 'RMB')
rmb_hkd = usd_hkd_data['5. Exchange Rate']
data['RMB volume'] = data['HKD volume']*float(rmb_hkd)

#Market Cap(USD)
data['Market Cap(USD)'] = data['5. adjusted close']*sharesoutstanding*usd_hkd


#Save as CSV
data.to_csv('C:/Users/Acudogon/Documents/M&A/01810.csv')



