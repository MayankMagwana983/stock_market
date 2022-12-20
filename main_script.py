import pandas as pd
import threading
# from time_scheduler import every
from create_option_chain import option_chain
import time
import os


option_chain_df = pd.DataFrame()
data_path = 'D:/Trading_Business/Option_Chain_Trading/data/'


timeout = 600.0 # Sixty seconds


# option_chain_df = option_chain("NIFTY", "OPTIDX")


# check date folder
current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))



if os. path. exists(data_path + 'daily_data/' + current_date) == False:
        os.makedirs(data_path + 'daily_data/' + current_date)

nexttime = time.time()
while True:
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    current_time_only = time.strftime('%H_%M_%S', time.localtime(time.time()))
    option_chain_i = option_chain("NIFTY", "OPTIDX")
    option_chain_i['time'] = current_time
    option_chain_i.to_csv(data_path + 'daily_data/' + current_date + '/' + current_time_only + '.csv' )
    option_chain_df = pd.concat([option_chain_i,option_chain_df])
    option_chain_df.to_csv(data_path + 'daily_data/' + current_date + '/option_chain'  + '.csv' )

       # take t sec
    nexttime += timeout
    sleeptime = nexttime - time.time()
    if sleeptime > 0:
        time.sleep(sleeptime)
        

