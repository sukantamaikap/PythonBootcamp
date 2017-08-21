# PROBLEM 1: STOCK SCREENER
# Plot multiple stocks in the same graph
from pandas_datareader import data
from datetime import datetime
import numpy as np
from matplotlib.dates import strpdate2num
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

tickers = {'AAPL', 'TSLA', 'YHOO', 'MOBL'}

def create_stock_record(ticker, source):
    start_date = datetime(2014, 6, 12)
    end_date = datetime.today()
    mobl = data.DataReader(ticker, source, start_date, end_date)
    file_name = 'problem1/' + ticker + '.csv'
    mobl.to_csv(file_name)
    print('record created for ticker : {} with file name {}'.format(ticker, file_name))
    return


def create_stock_records(tickers, source):
    print("inside create_stock_records")
    for ticker in tickers:
        print('creating data for ticker : {} '.format(ticker))
        create_stock_record(ticker, source)
    return


def generate_date():
    source = 'google'
    create_stock_records(tickers, source)
    return


def bytespdate2num(fmt, encoding='ascii'):
    print('format found {}'.format(fmt))
    str_converter = strpdate2num(fmt)

    def bytes_converter(b):
        s = b.decode(encoding)
        return str_converter(s)

    return bytes_converter


def graph_data():
    try:
        for stock in tickers:
            stock_file = 'problem1/' + stock + '.csv'
            print('Plotting for file : {}'.format(stock_file))
            converter = {0: bytespdate2num('%Y-%m-%d')}
            date_p, open_p, high_p, low_p, close_p, volume_p = np.loadtxt(stock_file, delimiter=',', unpack=True,
                                                                          converters=converter, skiprows=1)
            print('file : {} normalization completed'.format(stock_file))

            plt.plot_date(date_p, close_p, '-', label=stock)
    except Exception as ex:
        print('Failed to load file {}'.format(ex))

    plt.xlabel('date')
    plt.ylabel('price')
    plt.title('STOCK COMPARATOR')
    plt.legend()
    plt.show()


generate_date()
graph_data()
