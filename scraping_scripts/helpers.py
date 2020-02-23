# Imports
import requests
import pandas as pd
from bs4 import BeautifulSoup

def parse_statistics_table(url, table_caption):
	'''
	Find a table of statistics and create pandas DataFrame

	Parameters
	----------
	url: string 
		The URL that shows the table 
	table_caption: string
		The text in the table caption

	Returns
	-------
	df: pd.DataFrame
		DataFrame version of table from url with particular caption
	'''
	page_soup = BeautifulSoup(requests.get(url).text,
                                features="html.parser")

	# Find main table
	for caption in page_soup.find_all('caption'):
	    if caption.get_text() == table_caption:
	        table = caption.find_parent(
	            'table', {'class': 'engineTable'})


	# Isolate the column names <thead>
	table_thead = table.find('thead').find_all('tr')[0]
	columns = [x.get_text() for x in table_thead.find_all('th')]

	# Find and store each row
	rows = []

	for innings in [row for row in table.find('tbody').find_all('tr')]:
	    rows.append([stat.get_text() for stat in innings.find_all('td')])

	# Create pandas data frame and save to csv
	df = pd.DataFrame(rows, columns=columns).apply(pd.to_numeric, errors='ignore')

	return(df)
	