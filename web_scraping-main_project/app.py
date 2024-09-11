from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr-2024')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', {'class': 'history-rates-data'})
rows = table.find_all('tr', {'class': ''})
row_length = len(rows)

exchange_rates = []

temp = {} #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here for row in rows:
# Extract the date and exchange rate if available
    date_element = rows.find('a', class_='')
    rate_element = rows.find('span', class_='')

    if date_element and rate_element:
        # Store data in the temporary variable
        temp['Date'] = date_element.text.strip()
        temp['Exchange Rate'] = rate_element.text.strip().replace('1 USD =', '').strip()

# Append the temp dictionary to the final list
exchange_rates.append(temp)
	
temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(exchange_rates)

#insert data wrangling here
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data = data.sort_values(by='Date')
data.reset_index(drop=True, inplace=True)
data['Exchange Rate'] = data['Exchange Rate'].str.replace('IDR', '').str.strip()
data['Exchange Rate'] = pd.to_numeric(data['Exchange Rate'], errors='coerce').astype('float64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["Exchange Rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)