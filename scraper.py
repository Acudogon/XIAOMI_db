import exchangeRate as er
import os
import urllib2
import numpy as np
from BeautifulSoup import BeautifulSoup as bs
from pandas import DataFrame as df

from Tkinter import *
import tkSimpleDialog

def process_date(d):
	mon,day,yr = d.replace(',','').split()
	yr = yr[-2:]
	return day+'-'+mon+'-'+yr

def process_num(s, unit):
	if unit == 'B':
		num = float(s)
		num *= 1000
		s = str(int(num))
		if len(s) > 3:
			s = s[-3:] + ',' + s[-3:]
		if len(s) > 7:
			s = s[-7:] + ',' + s[-7:]
	elif unit == 'K':
		s = s[:-5] + str(int(s[-5]) + 1) if int(s[-3]) > 4 else s[:-4]
	return s

def get_historical_data(name, number_of_days):
	url = "https://finance.yahoo.com/quote/" + name + "/history/"

	rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')
	info = {'Date':[], 'Open':[], 'High':[], 'Low':[], 'Close':[]}
	for each_row in rows:
		if len(info['Date']) >= number_of_days:
			break
		divs = each_row.findAll('td')
		info['Date'].append(str(divs[0].span.text))
		info['Open'].append(str(divs[1].span.text))
		info['High'].append(str(divs[2].span.text))
		info['Low'].append(str(divs[3].span.text))
		info['Close'].append(str(divs[4].span.text))
	for key in info:
		result[key] = info[key]
	result.set_index('Date')

def get_stats(name):
	url = "https://finance.yahoo.com/quote/" + name + "/key-statistics?p=" + name
	rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')
	tmp = [np.nan for i in xrange(len(result))]
	for each_row in rows:
		divs = each_row.findAll('td')
		tmp[0] = np.nan
		if divs[0].span.text  == 'Market Cap (intraday)':			
			tmp[0] = process_num(divs[1].text[:-1],'B') if divs[1].text != 'N/A' else np.nan
			result['Market Cap'] = tmp
		elif divs[0].span.text  == 'Enterprise Value':
			tmp[0] = process_num(divs[1].text[:-1],'B') if divs[1].text != 'N/A' else np.nan
			result['EV'] = tmp
		elif divs[0].span.text  == 'Trailing P/E':
			tmp[0] = str(divs[1].text) if divs[1].text != 'N/A' else np.nan
			result['Trailing P/E'] = tmp
		elif divs[0].span.text  == 'Forward P/E':
			tmp[0] = str(divs[1].text) if divs[1].text != 'N/A' else np.nan
			result['Forward P/E'] = tmp
		elif divs[0].span.text  == 'Price/Sales':
			tmp[0] = str(divs[1].text) if divs[1].text != 'N/A' else np.nan
			result['P/S'] = tmp
		elif divs[0].span.text  == 'Price/Book':
			tmp[0] = str(divs[1].text) if divs[1].text != 'N/A' else np.nan
			result['P/B'] = tmp
		elif divs[0].span.text  == 'Enterprise Value/Revenue':
			tmp[0] = str(divs[1].text) if divs[1].text != 'N/A' else np.nan
			result['EV/Rev'] = tmp
		elif divs[0].span.text  == 'Enterprise Value/EBITDA':
			tmp[0] = str(divs[1].text) if divs[1].text != 'N/A' else np.nan
			result['EV/EBITDA'] = tmp
		else:
			# print divs[0].span.text
			continue
	return

def get_rev(name):
	url = 'https://finance.yahoo.com/quote/1810.HK/financials?p=' + name
	rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')
	counter = 0
	idx = 0
	line = []
	while counter < 3:
		divs = rows[idx].findAll('td')
		if divs[0].span.text == 'Revenue':
			line.append([str(divs[1].text)[6:]])
			line.append([str(divs[2].text)[6:]])
			line.append([str(divs[3].text)[6:]])
			counter += 1
		elif divs[0].span.text == 'Total Revenue':
			line[0].append(process_num(str(divs[1].text),'K'))
			line[1].append(process_num(str(divs[2].text),'K'))
			line[2].append(process_num(str(divs[3].text),'K'))
			counter += 1
		elif divs[0].span.text == 'Net Income' and len(divs) > 1:
			line[0].append(process_num(str(divs[1].text),'K'))
			line[1].append(process_num(str(divs[2].text),'K'))
			line[2].append(process_num(str(divs[3].text),'K'))
			counter += 1
		idx += 1
	tmp = [np.nan for i in xrange(len(result))]
	for e in line:
		tmp[0] = e[1]
		result[e[0]+'Rev'] = tmp
		tmp[0] = e[2]
		result[e[0]+'NetIncome'] = tmp


app = Tk()
app.withdraw()
ticker = tkSimpleDialog.askstring("Ticker","Ticker->")

result = df()
get_historical_data(ticker, 5)
get_stats(ticker)
get_rev(ticker)

date,tmp = er.get_usdToRmb()
diff = 0
while date[diff] != process_date(result['Date'][0]):
	if diff > 10:
		break
	print date[diff], process_date(result['Date'][0])
	diff += 1

result['USD->RMB'] = tmp[diff:diff+5]
result['USD->HKD'] = er.get_usdToHkd()[diff:diff+5]

result['HKD->RMB'] = result['USD->HKD'] / result['USD->RMB']
result = result.round({'HKD->RMB': 4})

print result
# path = os.getcwd().replace('\\','/')+'/1810hk.csv'
# xiaomi.to_csv(path, index=False)