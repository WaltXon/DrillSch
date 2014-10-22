# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 16:22:15 2014

@author: waltn
"""

import rigschedule as rs
import samplewells as sw
import pandas as pd

welldf = pd.DataFrame.from_records(sw.getWells())
schdf = pd.DataFrame.from_records(rs.rigSchedule())

def setPrefs(w, sch):
    for sid in sch.index: 
        spud_date = sch.get_value(sid, 'spud')
        for wid in w.index:
            #print wid
            if w.get_value(wid, 'expdate') > spud_date:
                #print('{0} < {1}'.format(w.get_value(wid, 'expdate'), spud_date))
                current = w.get_value(wid, 'pref')
                current.append(sid)
                w.set_value(wid, 'pref', current)

def rankWells(w, eur_cutoff = 5.0, acloss_cuttoff = 45.0):
    for wid in w.index:
        eur = w.get_value(wid, 'eur')
        acloss = w.get_value(wid, 'acloss')
        e = eur/eur_cutoff
        a = acloss/acloss_cuttoff
        w.set_value(wid, 'rank', int((e*.80 + a*.2)*100))
        

def stableMatching(wells, schedule):
    wellsToSchedule = [w for w in wells.index if wells.get_value(w, 'pref') != []]
    wellsOutOfBounds =  [w for w in wells.index if wells.get_value(w, 'pref') == []]
    wellsScheduled = []
    
    for oob in wellsOutOfBounds: 
        wells.set_value(oob, 'scheduled', 'OOB')
    
    #while wellsToSchedule: #and sum(eurFromPreviousRun) > sum(eurFromPreviousPreviousRun)
    #make sure imporovements to the EUR total are being made round to round
        #print('wellsToSchedule = {0}'.format(wellsToSchedule))  
        #if len([pp for pp in schedule.index if schedule.get_value(pp, 'well') == 'empty']) == 0:
            #break
    for pos in [p for p in schedule.index if schedule.get_value(p, 'well') == 'empty']:
        #print('pos = {0}'.format(pos))            
        possibles = [w for w in wells.index if pos in wells.get_value(w, 'pref') and wells.get_value(w, 'scheduled') == 'no']
        #print('possibles = {0}'.format(possibles))
        if possibles != []:            
            possdf = wells.iloc[possibles]
            #print possdf
            candidates = possdf.sort(columns='rank', ascending=False, axis=0)
            #print('candidates = {0}'.format(candidates))
            candidate = candidates.iloc[[0]]
            #print('candidate = {0}'.format(candidate))
            #print('candidate.index[0] = {0}'.format(candidate.index[0]))
            wells.set_value(candidate.index[0], 'scheduled', 'yes')
            wells.set_value(candidate.index[0], 'sch_id', pos)
            schedule.set_value(pos, 'well', wells.get_value(candidate.index[0], 'name'))
            wellsScheduled.append(candidate.index[0])
            wellsToSchedule.remove(candidate.index[0])      
                
        #wellsScheduledDF = wells.iloc[wellsScheduled]
        #wellsNotSchedueld = wells.iloc[wellsNotScheduled]
        #wellsOutOfBounds = wells.iloc[wellsOutOfBounds]
    report(wells, wellsScheduled, wellsOutOfBounds, wellsToSchedule)
        #return (wellsScheduledDF, wellsNotScheduledDF, wellsOutOfBoundsDF)
        
def report(df, wellsSch, wellsOOB, wellsNotSch):
    wSch = df.iloc[wellsSch]
    wOOB = df.iloc[wellsOOB]
    wNotSch = df.iloc[wellsNotSch]
    dfsum = df.sum()
    print('')
    print('================REPORT==================')
    print('')
    print("Max Possible Matches = {0}".format(len(wellsSch) + len(wellsNotSch)))    
    print('')
    print("Wells Scheduled = {0}".format(len(wellsSch))) 
    print('')       
    wsSum = wSch.sum(axis=0)
    print("% of EUR = {0}".format(wsSum['eur']/dfsum['eur']))
    print("% of AC LOSS = {0}".format(wsSum['acloss']/dfsum['acloss']))
    print(wsSum)
    print('')
    print("Wells Not Scheduled = {0}".format(len(wellsNotSch)))
    print('')
    wnSum = wNotSch.sum(axis=0)
    print("% of EUR = {0}".format(wnSum['eur']/dfsum['eur']))
    print("% of AC LOSS = {0}".format(wnSum['acloss']/dfsum['acloss']))
    print(wnSum)
    print('')
    print("Wells Out Of Bounds = {0}".format(len(wellsOOB)))
    print('')
    woSum = wOOB.sum(axis=0)
    print("% of EUR = {0}".format(woSum['eur']/dfsum['eur']))
    print("% of AC LOSS = {0}".format(woSum['acloss']/dfsum['acloss']))
    print(woSum)
    print('=========================================')
    
    
setPrefs(welldf, schdf)
rankWells(welldf)

stableMatching(welldf, schdf)




