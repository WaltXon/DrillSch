# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 16:22:15 2014

@author: waltn
"""

import rigschedule as rs
import samplewells as sw
import pandas as pd

eur_cutoff = 5.0
acloss_cuttoff = 45.0


wells = pd.DataFrame.from_records(sw.getWells())
sch = pd.DataFrame.from_records(rs.rigSchedule())

print sch

def setPrefs(wells, schedule):
    for exp in wells.expdate:
        for spud in schedule.spud:
            if exp < spud:
                wells.pref.append(spud)

setPrefs(wells, sch)

def stableMatching(wells, schedule):
    #if     
    #while 'empty' in [status for status in schedule.well]:
    pass