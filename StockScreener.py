#PROBLEM 1 : STOCK SCREENER

from pandas_datareader import data
from datetime import datetime

ticker = 'MOBL'
source = 'google'
start_date = datetime(2014, 6, 12)
end_date = datetime.today()
mobl = data.DataReader(ticker, source, start_date, end_date)
mobl.to_csv(ticker + '.csv')

