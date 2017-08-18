# PROBLEM 1: STOCK SCREENER
from pandas_datareader import data
from datetime import datetime
import numpy as np
from matplotlib.dates import strpdate2num
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time

tickers = {'GOGL', 'AAPL'} #, 'TSLA', 'YHOO'}


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
            date_p = np.flipud(date_p)
            close_p = np.flipud(close_p)
            print('file : {} normalization completed'.format(stock_file))
            plt.plot(date_p, close_p, label=stock)
    except Exception as ex:
        print('Failed to load file {}'.format(ex))

    plt.xlabel('date')
    plt.ylabel('price')
    plt.title('STOCK COMPARATOR')
    plt.legend()
    plt.show()


generate_date()
graph_data()
