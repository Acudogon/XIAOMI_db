import os
import urllib2
from BeautifulSoup import BeautifulSoup as bs
from pandas import DataFrame as df

def get_historical_data(name, number_of_days):
    url = "https://finance.yahoo.com/quote/" + name + "/history/"

    rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')
    info = {'Date':[], 'Open':[], 'High':[], 'Low':[], 'Close':[]}
    for each_row in rows:
    	if len(info['Date']) >= number_of_days:
    		break
        divs = each_row.findAll('td')
        info['Date'].append(str(divs[0].span.text))
        info['Open'].append(float(divs[1].span.text.replace(',','')))
        info['High'].append(float(divs[2].span.text.replace(',','')))
        info['Low'].append(float(divs[3].span.text.replace(',','')))
        info['Close'].append(float(divs[4].span.text.replace(',','')))
    for key in info:
    	xiaomi[key] = info[key]
    xiaomi.set_index('Date')
    return xiaomi

def get_stats(name):
	url = "https://finance.yahoo.com/quote/" + name + "/key-statistics?p=" + name

	rows = bs(urllib2.urlopen(url).read()).findAll('table')[0].tbody.findAll('tr')
	for each_row in rows:
		divs = each_row.findAll('td')
		if divs[0].span.text  == 'Market Cap (intraday)':
			xiaomi['Market Cap'] = None if divs[1].text == 'N/A' else int(float(divs[1].text.replace('B',''))*1000)
		elif divs[0].span.text  == 'Enterprise Value':
			xiaomi['EV'] = None if divs[1].text == 'N/A' else int(float(divs[1].text.replace('B',''))*1000)
		elif divs[0].span.text  == 'Trailing P/E':
			xiaomi['Trailing P/E'] = None if divs[1].text == 'N/A' else float(divs[1].text)
		elif divs[0].span.text  == 'Forward P/E':
			xiaomi['Forward P/E'] = None if divs[1].text == 'N/A' else float(divs[1].text)
		elif divs[0].span.text  == 'Price/Sales':
			xiaomi['P/S'] = None if divs[1].text == 'N/A' else float(divs[1].text)
		elif divs[0].span.text  == 'Price/Book':
			xiaomi['P/B'] = None if divs[1].text == 'N/A' else float(divs[1].text)
		elif divs[0].span.text  == 'Enterprise Value/Revenue':
			xiaomi['EV/Rev'] = None if divs[1].text == 'N/A' else float(divs[1].text)
		elif divs[0].span.text  == 'Enterprise Value/EBITDA':
			xiaomi['EV/EBITDA'] = None if divs[1].text == 'N/A' else float(divs[1].text)
		else:
			# print divs[0].span.text
			continue
	return

xiaomi = df()
get_historical_data('1810.hk', 5)
get_stats('1810.HK')
print xiaomi
path = os.getcwd().replace('\\','/')+'/1810hk.csv'
xiaomi.to_csv(path)