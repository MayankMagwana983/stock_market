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

import support_resistance_fractal as srf


client_id = 'WM7F3LIJD3-100'
secret_key = '0CJNP13AWG'
redirect_uri = 'http://127.0.0.1:5000/login'



session=accessToken.SessionModel(client_id=client_id,
secret_key=secret_key,redirect_uri=redirect_uri, 
response_type='code', grant_type='authorization_code')


response = session.generate_authcode() 
response


auth_code = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2NzA4NTIxNDMsImV4cCI6MTY3MDg4MjE0MywibmJmIjoxNjcwODUxNTQzLCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYTTAyNjQzIiwibm9uY2UiOiIiLCJhcHBfaWQiOiJXTTdGM0xJSkQzIiwidXVpZCI6IjJhMDAxNTc0Y2I0NzRkNDQ5YjdmZjkyOWYwNGQyZGU4IiwiaXBBZGRyIjoiMC4wLjAuMCIsInNjb3BlIjoiIn0.3MexKlD47GitjKk57q5WPi6NHA-BA7UShnhHG1vJry0'

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


nexttime = time.time()


range_from = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
range_to = datetime.datetime.now().strftime('%Y-%m-%d')
range_from = '2022-12-01'
range_to = '2022-12-12'
candle_resolution = 3
symbol = "NSE:NIFTY50-INDEX"
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





while True:
    historical_data = pd.DataFrame(data_fetch(range_from,range_to)['candles'],columns=['Date','Open','High','Low','Close','Vol'])
    historical_data['Date'] = pd.to_datetime(historical_data['Date'],unit='s') + datetime.timedelta(hours = 5.5)
    historical_data.set_index('Date',inplace = True)
    #Calculate signal data
    historical_data['SMA 30'] = ta.sma(historical_data['Close'],30)
    historical_data['SMA 60'] = ta.sma(historical_data['Close'],60)
    #generate signal
    historical_data['enter_signal'] = np.nan
    historical_data['exit_signal'] = np.nan
    position = False
    
    for i in range(len(historical_data)):
        if ((historical_data['SMA 30'][i] > historical_data['SMA 60'][i]) & (position == False)): # This needs some checking
                historical_data['enter_signal'][i] = 1
                position = True
        elif ((historical_data['SMA 30'][i] <= historical_data['SMA 60'][i]) & (position == True)):
                historical_data['exit_signal'][i] = 1
                position = False

    
def support_resistance(df):
    is_support = [srf.is_support(df,i+2) for i in range(len(df)-4)]
    is_support.insert(0,None)
    is_support.insert(1,None)
    is_support.append(None)
    is_support.append(None)
    df["is_support"] = is_support
    df.loc[df["is_support"] == True, "is_support_price"] = df["Low"]
    
    is_resistance = [srf.is_resistance(df,i+2) for i in range(len(df)-4)]
    is_resistance.insert(0,None)
    is_resistance.insert(1,None)
    is_resistance.append(None)
    is_resistance.append(None)
    df["is_resistance"] = is_resistance
    df.loc[df["is_resistance"] == True, "is_resistance_price"] = df["High"]
    
    return df



def main():
    









