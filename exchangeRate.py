import os
import urllib2
import numpy as np
from BeautifulSoup import BeautifulSoup as bs
from pandas import DataFrame as df

def get_usdToRmb():
	url = "https://www.federalreserve.gov/releases/h10/hist/dat00_ch.htm"
	rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].findAll('tr')
	date, rate = [],[]
	for each_row in rows[::-1]:
		date.append(str(each_row.findAll('th')[0].text))
		if each_row.findAll('td')[0].text == 'ND':
			rate.append(np.nan)
		else:
			rate.append(float(each_row.findAll('td')[0].text))
	return date, rate

def get_usdToHkd():
	url = "https://www.federalreserve.gov/releases/h10/hist/dat00_hk.htm"
	rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].findAll('tr')
	rate = []
	for each_row in rows[::-1]:
		if each_row.findAll('td')[0].text == 'ND':
			rate.append(np.nan)
		else:
			rate.append(float(each_row.findAll('td')[0].text))
	return rate

if __name__ == "__main__":
	rates = df()
	date, rate = get_usdToRmb()
	rates['Date'] = date
	rates.set_index('Date')
	rates['USD->RMB'] = rate
	rates['USD->HKD'] = get_usdToHkd()

	rates['HKD->RMB'] = rates['USD->HKD'] / rates['USD->RMB']
	rates = rates.round({'HKD->RMB': 4})

	print rates
	# path = os.getcwd().replace('\\','/')+'/rates.csv'
	# rates.to_csv(path, index=False)