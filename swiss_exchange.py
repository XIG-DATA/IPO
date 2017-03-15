import os, requests
from bs4 import BeautifulSoup
import xlwt
import multiprocessing, sys, os  , time 
import pandas as pd , pickle

def craw_ipo(year):
	url = 'http://www.six-swiss-exchange.com/shares/companies/ipo/' + str(year) + '/overview_en.htm'
	response = requests.get(url)#, headers = headers)
	soup = BeautifulSoup(response.text,'lxml')
	tmp = []
	for i,ex in enumerate(soup.findAll('td')):
		if len(ex.text.strip()) > 0 and len(ex.text) < 40:
			tmp.append(ex.text)

	start = 0
	for i, x in enumerate(tmp):
		if len(x.split('.')) == 3:
			start = i
			break 
	end = tmp.index('Description')
	result = tmp[start:end]
	return result 


def write():
	result = []
	for i in range(2006, 2017):
		result.extend(craw_ipo(i))
	return result

def old():
	result = write()
	book = xlwt.Workbook()
	sh = book.add_sheet("Sheet")
	n = 0
	for i in range(int(len(result)/7)):
		t = result[7* i : 7 * i + 7 ]
		sh.write(n, 0, t[0])
		sh.write(n, 1, t[1])
		sh.write(n, 2, t[2])
		sh.write(n, 3, t[3])
		sh.write(n, 4, t[4])
		sh.write(n, 5, t[5])
		sh.write(n, 6, t[6])
		n = n + 1 
	book.save('ipo.xlsx')


def test(number):
	result = {}
	#inp = 'https://beta.companieshouse.gov.uk/company/10110294'
	base = 'https://beta.companieshouse.gov.uk/company/10' + number
	try : 
		r = requests.get(base)
		soup = BeautifulSoup(r.text, 'lxml')
		candidates = soup.findAll('dd')[-1]
		result['date'] = candidates.text 
		result['company'] = soup.title.text
	except : 
		print(number + ' not found')

	return result 

company_numbers = []
for i in range(0,999999):		
	ele = str(i)
	len_ele = len(ele)
	if len_ele < 6 : 
		tmp = ''.join(['0']* (6-len_ele)) +str(i)	
	else:
		tmp = ele 

	company_numbers.append(tmp)

print()
print('--- Parsing')

num_tasks = len(company_numbers)

p = multiprocessing.Pool()
results = p.imap(test, company_numbers)
while (True):
    completed = results._index
    print("\r--- Completed {:,} out of {:,}".format(completed, num_tasks))
    sys.stdout.flush()
    time.sleep(1)
    if (completed == num_tasks): break
p.close()
p.join()
df_full = pd.DataFrame(list(results))

print()
with open('10_test.pkl', 'wb') as fp:
    pickle.dump(df_full, fp)
