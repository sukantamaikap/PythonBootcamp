import pandas as pd
import quandl
import math
from datetime import timedelta
import numpy as np
from sklearn import preprocessing, cross_validation
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


def generateData():
    #Add your Quandl API KEY here
    quandl.ApiConfig.api_key = 'Your key here'
    df = quandl.get('WIKI/TSLA')
    print("raw data from Quandl")
    print(df.head())
    print(df.shape)
    df.to_csv('TSLA.csv')


def predict_and_plot():
    df = pd.read_csv('TSLA.csv')
    print('data read from file : ', df.head(), df.shape)
    df['Date'] = df['Date'].astype('datetime64[ns]')
    df.set_index('Date', inplace='True')
    # define the features
    df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100
    df['PCT_Change'] = ((df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open']) * 100

    #filter out the required columns
    df = df[['Adj. Close', 'HL_PCT', 'PCT_Change', "Adj. Volume"]]

    # define the label
    forecast_column = 'Adj. Close'
    df.fillna(-9999, inplace=True)

    # define the forecast length
    forecast_out = int(math.ceil(0.01 * len(df)))
    print("forecast lengthh : " + str(forecast_out))

    # define the label
    df['label'] = df[forecast_column].shift(-forecast_out)
    print('label chosen ...')
    print('shape of the data after adding label : ', str(df.shape))
    print(df.head())
    print(df.tail())

    #define features i.e remove label from the data frame
    X = np.array(df.drop(['label'], 1))
    X = preprocessing.scale(X)
    #forecast for last "forecast_out" days only, as they do not have a corresponding predictions
    X_predict_on = X[- forecast_out:]
    #remove the "forecast out" count from the end to ensure count parity between feature and label
    X = X[:-forecast_out]

    # define label
    y = df['label']
    y.dropna(inplace=True)
    y = np.array(y)

    print('Check data consistency, X : ,', len(X),  ' and Y : ', len(y))

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
    clf = LinearRegression()
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    forecast_set = clf.predict(X_predict_on)
    print(forecast_set, accuracy, forecast_out)

    last_date = df.iloc[-1].name
    modified_date = last_date + timedelta(days=1)
    date = pd.date_range(last_date, periods=forecast_out, freq='D')
    df1 = pd.DataFrame(forecast_set, columns=['Forecast'], index=date)
    df = df.append(df1)

    print(df.head())
    print(df.tail())

    df['Adj. Close'].plot()
    df['Forecast'].plot()
    plt.legend(loc=1)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

generateData()
predict_and_plot()