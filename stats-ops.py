#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import numpy as np
import time
import math
from datetime import date


# In[31]:


def calc_iv(venc, st, tipo, days):
    days = days/365
    perp = requests.get("https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-PERPETUAL").json()['result']
    mprice = perp['mark_price']
    #criar lista de 2000 a 16000 somando de 125 em 125
    if tipo == 'diaria':
        interval = 500
    if tipo == 'semanal':
        interval = 500
    if tipo == 'trimestral':
        interval = 500
    #trazer o número mais aproximado da lista
    op = requests.get(f"https://www.deribit.com/api/v2/public/ticker?instrument_name=BTC-{venc}-{st}-P").json()['result']
    iv = op['mark_iv']/100
    iv_d = iv*math.sqrt(days)
    range_1dpmax = mprice*(1+(iv_d))
    range_1dpmin = mprice*(1-(iv_d))
    range_2dpmax = mprice*(1+(2*iv_d))
    range_2dpmin = mprice*(1-(2*iv_d))
    range_3dpmax = mprice*(1+(3*iv_d))
    range_3dpmin = mprice*(1-(3*iv_d))
    info = ['IV', 'IV_d', 'BTC-MIN', 'BTC-MAX']
    data = [range_3dpmin, range_2dpmin, range_1dpmin, range_1dpmax, range_2dpmax, range_3dpmax]
    stats = dict(zip(info, data))
    return data


# In[35]:


iv2 = calc_iv('22JUL22', '20000', 'mensal', 10)
a = {'68.2% de chance': [iv2[2], iv2[3]] ,'95.4% de chance': [iv2[1], iv2[4]],'99.6% de chance': [iv2[0], iv2[5]]}
df = pd.DataFrame(a, index = ['Preço Mínimo', 'Preço Máximo']).T
df = df.round(2)
iv2 = [round(num, 2) for num in iv2]
df

