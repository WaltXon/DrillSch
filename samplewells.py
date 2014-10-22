# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 09:20:46 2014

@author: waltn
"""

import random
import datetime
import cPickle as pickle


names = pickle.load( open( 'C:\Users\WaltN\Desktop\GitHub\DrillSch\sh.p', "rb" ) )

def getName():
    n = random.choice(names)
    if n.find('  ') > -1:
        a = n.split('  ')
        b = a[random.randint(0,len(a)-1)]
    else:
        b = n
    if b == '' or b is None:
        b = getName()
    return '{0}-{1}'.format(b, random.randint(1,7))

def getEUR(low=5.0, high=20.0):
    f = 10.0
    return random.randrange(low*f, high*f, 0.5*f)/f
    ##Consider using np.random.normal() for a more accurate distribtion

def getExpDate(start, end, time_format='%Y-%m-%d'):
    sd = datetime.datetime.strptime(start, time_format)  
    ed = datetime.datetime.strptime(end, time_format)  
    year = random.choice(range(sd.year,ed.year))
    month = random.choice(range(1, 12))
    day = random.choice(range(1, 28))
    expdate = datetime.datetime(year, month, day)
    return expdate
    
def getAcres(low=0.0, high=400.0):
    return random.randrange(low, high, 5.0)
    
def getWells(n=20, sdate = '2014-01-01', edate='2017-02-20'):
    wells = []
    for i in range(n):
        wells.append({"name": getName(), "eur": getEUR(), "expdate": getExpDate(sdate, edate), 
        "acloss": getAcres(), 'pref': [], 'scheduled': 'no', 'rank': 0.0, 'sch_id': -1})
    return wells


  


