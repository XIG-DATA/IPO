import xlrd,re

import datetime 

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def read_ukipo():
	import xlrd
	workbook = xlrd.open_workbook('UK-IPO.xlsx')
	worksheet = workbook.sheet_by_name('New Issues and IPOs')
	print(dir(worksheet))
	print(worksheet._dimncols, worksheet._dimnrows)

	sh = workbook.sheet_by_index(2)
	
	print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
	result = []
	for i in range(1, sh.nrows):
	    tmp = sh.row(i)

	    #text = [ str( re.sub(r'[^\x00-\x7F]','', x.value)).split(':')[-1] for x in tmp]
	    text = []
	    for j,x in enumerate(tmp):
	    	if j==1:
	    		clean_x = xlrd.xldate.xldate_as_datetime(x.value, workbook.datemode)
	    	else:
		    	if type(x.value) ==  unicode:
		    		clean_x =strip_non_ascii(x.value)
		    	else :
		    		clean_x = str(x)
	    	text.append(clean_x)

	    result.append(text)

	data = [ (str(x[1].year), str(x[1].month), str(x[1].day), x[4], x[6]) for x in result ]
	fp = open('uk_ipo_reference.txt','wb')
	fname = open('uk_ipo_name.txt', 'wb')
	for item in data:
		if item[3] == 'IPO' and item[0] > '1999' and item[0] < '2017': 
			fp.write(' '.join(item) + '\n')
			fname.write(item[-1] + '\n')
	fp.close()
	fname.close()


if __name__ == '__main__':
	read_ukipo()