from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import csv
import pandas as pd

def get_data():
    api_key = "RDYJ6OGZ5PJCWW44"
    ts = TimeSeries(key= api_key, output_format='pandas')
    ti = TechIndicators(key = api_key, output_format = 'pandas')

    stock = 'AAPL'

    # get data, returns a tuple
    # data is pandas dataframe, meta_data is a dict
    data, meta_data = ts.get_daily(symbol= stock, outputsize = 'compact')
    # stock_MACD, stock_meta_MACD are both dict
    macd, meta_macd = ti.get_macd(symbol = stock, interval = 'daily', series_type = 'open')


    data.to_csv('AAPL_data.csv', sep='\t')
    with open('AAPL_meta_data.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=list(meta_data.keys()))
        writer.writeheader()
        writer.writerow(meta_data)
    with open('AAPL_macd_meta_data.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=list(meta_macd.keys()))
        writer.writeheader()
        writer.writerow(meta_macd)

    #Visualization
    figure(num=None, figsize = (30,12), dpi=80, facecolor='w', edgecolor='k')
    data['4. close'].plot()
    title_data = 'Daily Times Series for '+ stock + ' stock'
    plt.title(title_data)
    plt.tight_layout()
    plt.grid()
    plt.show()

    macd.plot()
    title_macd = 'MACD indicator for '+ stock + ' stock'
    plt.title(title_macd)
    plt.tight_layout()
    plt.grid()
    plt.show()


get_data()
