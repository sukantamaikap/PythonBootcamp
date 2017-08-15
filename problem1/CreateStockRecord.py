# PROBLEM 1: STOCK SCREENER
from pandas_datareader import data
from datetime import datetime
import numpy as np
from matplotlib.dates import strpdate2num
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time

tickers = {'MOBL', 'AAPL', 'TSLA', 'YHOO', 'SAP'}


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
    print("inside graph_data")
    source = 'google'
    create_stock_records(tickers, source)
    return


def bytespdate2num(fmt, encoding='ascii'):
    print('format found {}'.format(fmt))
    str_converter = strpdate2num(fmt)
    print("end")

    def bytes_converter(b):
        print('byte converter')
        s = b.decode(encoding)
        print('byte converter end')
        return str_converter(s)

    return bytes_converter


def graph_data():
    try:
        stock_file = 'problem1/' + 'MOBL' + '.csv'
        print('Plotting for file : {}'.format(stock_file))
        converter = {0: bytespdate2num('%Y-%m-%d')}
        date_p, open_p, high_p, low_p, close_p, volume_p = np.loadtxt(stock_file, delimiter=',', unpack=True,
                                                                      converters=converter, skiprows=1)
        print('file : {} normalization completed'.format(stock_file))
        fig = plt.figure()
        axis_1 = plt.subplot(1, 1, 1)
        axis_1 = plt.plot(date_p, open_p)
        axis_1 = plt.plot(date_p, close_p)
        axis_1 = plt.plot(date_p, high_p)
        axis_1 = plt.plot(date_p, low_p)
        axis_1 = plt.plot(date_p, volume_p)
        plt.show()
    except Exception as ex:
        print('Failed to load file {}'.format(ex))


generate_date()
graph_data()
