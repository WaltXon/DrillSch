# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 10:41:50 2014

@author: waltn
"""

import datetime
import pandas as pd



def createRigSchedule(start_date='2014-10-14', contractLenMonths=12, spudToSpudDays = 22): 
    stime = datetime.datetime.strptime(start_date,'%Y-%m-%d')  
    etime = stime + du.relativedelta.relativedelta(months = contractLenMonths)
    diff = du.relativedelta.relativedelta(stime, etime)
    totaldays = abs(diff.years*365 + diff.months*30 + diff.days)
    periods = totaldays/spudToSpudDays     
    rng = pd.date_range(start_date, periods, freq='D')    
    print stime, etime, totaldays, periods
    return rng  
    
drldays = 22.0
cterm = 12.0
dpm = 365.0/12.0
start_date='2014-10-14'
periods = (cterm*dpm) / drldays

dr1 = pd.date_range(start_date)