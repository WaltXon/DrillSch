# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:41:50 2014

@author: waltn
"""

import datetime
import pandas as pd



def rigSchedule(start_date='2014-10-14', cterm=12, drldays = 22): 
    dpm = 365.0/12.0
    periods = int((cterm*dpm) / drldays)
    sdate = datetime.datetime.strptime(start_date,'%Y-%m-%d')  
    dates = {}
    d = sdate
    dates[d] = 'empty'
    for x in range(0,periods):
        d =  d + datetime.timedelta(days=drldays)
        dates[d] = 'empty'
    print dates
    return dates