# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 21:56:22 2022

@author: Mayank Chhibber
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.parse import urlencode

def np_float(x):
    try:
        y = x.lstrip().rstrip().replace(',','')
        return np.float64(y)
    except:
        return np.nan

def option_chain(symbol, instrument, date_="-"):
    base_url = "https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?"
    parameters = {
        "segmentLink": 17,
        "instrument": instrument,
        "symbol": symbol,
        "date": date_
    }
    url = base_url + urlencode(parameters)
    headers = {
        "Host": "www1.nseindia.com",
        "Referer": "https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        }
    r = requests.get(url, headers=headers)
    
    bs = BeautifulSoup(r.text)
    table = bs.find("table", {"id": "octable"})
    # Get all rows
    table_rows = table.find_all('tr')
    
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        if td:
            row = [tr.text for tr in td]
            l.append(row)
    
    arr = []
    for r in l:
        row = [np_float(x) for x in r]
        arr.append(row)
    
    df = pd.DataFrame(arr)
    df.columns = ["CE Chart", "CE OI", "CE Change in OI", "CE Volume", "CE IV", "CE LTP", "CE Net Change", "CE Bid Qty", "CE Bid Price", "CE Ask Price", "CE Ask Quantity",
                 "Strike Price",
                 "PE Bid Qty", "PE Bid Price", "PE Ask Price", "PE Ask Qty", "PE Net Change", "PE LTP", "PE IV", "PE Volume", "PE Change in OI", "PE OI", "PE Chart"]
    print(df)
    return df
