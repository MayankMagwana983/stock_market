# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 23:22:58 2022

@author: Mayank Chhibber
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 22:35:45 2022

@author: Mayank Chhibber
"""

from fyers_api import fyersModel
from fyers_api import accessToken
from fyers_api.Websocket import ws
import time
import datetime
import talib
import pandas as pd
import time
import numpy as np
import pandas_ta as ta
import os
import support_resistance_fractal
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import matplotlib.dates as mpdates


client_id = 'WM7F3LIJD3-100'
secret_key = '0CJNP13AWG'
redirect_uri = 'http://127.0.0.1:5000/login'



session=accessToken.SessionModel(client_id=client_id,
secret_key=secret_key,redirect_uri=redirect_uri, 
response_type='code', grant_type='authorization_code')


response = session.generate_authcode() 
response


auth_code = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2NzE0NzU2NDksImV4cCI6MTY3MTUwNTY0OSwibmJmIjoxNjcxNDc1MDQ5LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYTTAyNjQzIiwib21zIjpudWxsLCJub25jZSI6IiIsImFwcF9pZCI6IldNN0YzTElKRDMiLCJ1dWlkIjoiNWM3ZTBiYzcwYTY3NDI1N2FmMzYzNWUxNGJkY2E0MjkiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.f0zOVgjzIpfwLoVan-H56IWatZvPLzIHUYHElTmiw40'

session.set_token(auth_code)
response = session.generate_token()

access_token = response["access_token"]
access_token



fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)


fyers.get_profile()
fyers.funds()
fyers.holdings()


data_path = 'D:/Trading_Business/Option_Chain_Trading/data/'
current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
timeout = 2




def data_fetch(range_from_value,range_to_value):
    data = {"symbol":symbol,"resolution":candle_resolution,"date_format":"1","range_from":range_from_value,"range_to":range_to_value,"cont_flag":"1"}
    hist_data = fyers.history(data)
    return hist_data




range_from = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
range_to = datetime.datetime.now().strftime('%Y-%m-%d')
range_from = '2022-12-18'
range_to = '2022-12-20'
candle_resolution = 1
symbol = "NSE:NIFTY50-INDEX"
range_from_sr = '2022-12-01' 
range_tp_sr =  '2022-12-20'
candle resolution_sr = 10
# time_period_required = 31

# time_period_mfi = 10
  
# historical_data = pd.DataFrame(data_fetch(range_from,range_to)['candles'],columns=['time','open','high','low','close','vol'])
# historical_data['time'] = pd.to_datetime(historical_data['time'],unit='s') + datetime.timedelta(hours = 5.5)
# # historical_data = historical_data.iloc[:time_period_required,0:7]
# # historical_data_offset =  historical_data.shift(1).add_suffix("_1")
# # historical_data = historical_data.merge(historical_data_offset,how = 'left',left_index = True,right_index = True)
# historical_data.set_index('time',inplace = True)
# # historical_data.to_csv(data_path + 'daily_data/' + current_date + '/index_data'  + '.csv' )
#        # take t sec
# # nexttime += timeout
# # sleeptime = nexttime - time.time()


timeout = 270.0 # Sixty seconds

current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))


trading_dataframe = pd.DataFrame(columns = ['Enter_Time','Exit_Time','Enter_Price','Exit_Price'])

nexttime = time.time()
position = False

trade_number = 0
while True:
    historical_data = pd.DataFrame(data_fetch(range_from,range_to)['candles'],columns=['Date','Open','High','Low','Close','Vol'])
    historical_data['Date'] = pd.to_datetime(historical_data['Date'],unit='s') + datetime.timedelta(hours = 5.5)
    # historical_data.set_index('Date',inplace = True)
    
    #Calculate support-resistance levels
    # a list to store resistance and support levels

    support_resistance_df =   historical_data = pd.DataFrame(data_fetch(range_from,range_to)['candles'],columns=['Date','Open','High','Low','Close','Vol'])
    support_resistance_df['Date'] = pd.to_datetime(support_resistance_df['Date'],unit='s') + datetime.timedelta(hours = 5.5)
    levels = []
    for i in range(2, historical_data.shape[0] - 2):  
      if support_resistance_fractal.is_support(historical_data, i):    
        low = historical_data['Low'][i]    
        if support_resistance_fractal.is_far_from_level(low, levels, historical_data):      
          levels.append((i, low))  
      elif support_resistance_fractal.is_resistance(historical_data, i):    
        high = historical_data['High'][i]    
        if support_resistance_fractal.is_far_from_level(high, levels, historical_data):      
          levels.append((i, high))
    
    
    
    
    
    #Calculate signal data
    historical_data['SMA_30'] = ta.sma(historical_data['Close'],5)
    historical_data['SMA_60'] = ta.sma(historical_data['Close'],10)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #generate signal
    if ((historical_data.tail(1)['SMA_30'].values[0] > historical_data.tail(1)['SMA_60'].values[0])  &  
        (historical_data.tail(2)['SMA_30'].values[0] <= historical_data.tail(2)['SMA_60'].values[0]) &
        (position == False)):
        trade_number += 1 
        trading_dataframe.loc[trade_number,'Enter_Time'] = current_time
        trading_dataframe.loc[trade_number,'Enter_Price'] = historical_data.tail(1)['Close'].values[0]
        # trading_dataframe.loc[trade_number,'Enter_Exit'] = 'Enter'
        position = True
        print('trade taken')
    elif ((historical_data.tail(1)['SMA_30'].values[0] <= historical_data.tail(1)['SMA_60'].values[0])  & 
        (position == True)):
       trading_dataframe.loc[trade_number,'Exit_Time'] = current_time
       trading_dataframe.loc[trade_number,'Exit_Price'] = historical_data.tail(1)['Close'].values[0]
       position = False
       print('trade exited')
        # take t sec
    nexttime += timeout
    sleeptime = nexttime - time.time()
    if sleeptime > 0:
        time.sleep(sleeptime)
    trading_dataframe.to_csv('trading_dataframe')
    print('Next Loop')
    
df = historical_data.copy()
df['Date'] = df['Date'].map(mpdates.date2num)
    




    