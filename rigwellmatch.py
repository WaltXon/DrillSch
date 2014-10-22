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

def checkExp(wellid, posid):
    if welldf.get_value(wellid, 'expdate') > schdf.get_value(posid, 'spud'):
        return 'GOOD'
    else: return 'BAD'

def setPrefs(w, sch):
    for sid in sch.index: 
        for wid in w.index:
            #print wid
            if checkExp(wid, sid) == 'GOOD':
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
        
def getEmpty(sch):
    return [p for p in sch.index if sch.get_value(p, 'well') == 'empty']

def setOOB(wells):
    wellsOutOfBounds =  [w for w in wells.index if wells.get_value(w, 'pref') == []]
    for oob in wellsOutOfBounds: 
        wells.set_value(oob, 'scheduled', 'OOB')
    return wellsOutOfBounds
    
def getSchd(wells):
    return [w for w in wells.index if wells.get_value(w, 'scheduled') == 'yes']
def getOOB(wells):
    return [w for w in wells.index if wells.get_value(w, 'scheduled') == 'OOB']
def getNotSchd(wells):
    return [w for w in wells.index if wells.get_value(w, 'scheduled') == 'no']
        
def greedyMatching(wells, sch):
    
    wellsOutOfBounds = getOOB(wells)
    wellsToSchedule = getNotSchd(wells)
    wellsScheduled = getSchd(wells) or []
    
    for pos in getEmpty(sch):
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
            sch.set_value(pos, 'well', wells.get_value(candidate.index[0], 'name'))
            sch.set_value(pos, 'well_id', candidate.index[0])
            wellsScheduled.append(candidate.index[0])
            wellsToSchedule.remove(candidate.index[0])      
                
    report(wells)
    return(wells, wellsScheduled, wellsOutOfBounds, wellsToSchedule)
    
def refineMatch(wells, sch):
    wellsToSchedule = [w for w in wells.index if wells.get_value(w, 'scheduled') == 'no']
    res = welldf.iloc[wellsToSchedule].sort(columns='rank', axis=0, ascending=True) #TRUE OR FALSE
    print res
    for wid in res.index:
        print('')
        print('wid = {0}'.format(wid))
        prefs = res.get_value(wid, 'pref')
        for pos in prefs:
            print('pos = {0}'.format(pos))
            swapee = sch.get_value(pos, 'well_id')
            print('swapee = {0}'.format(swapee))
            for empt in getEmpty(sch):
                print('empt = {0}'.format(empt))
                if checkExp(swapee, empt) == 'GOOD':
                    sch.set_value(empt, 'well', sch.get_value(swapee, 'well'))
                    sch.set_value(empt, 'well_id', swapee)
                    sch.set_value(pos, 'well', sch.get_value(wid, 'well'))
                    sch.set_value(pos, 'well_id', wid)
                    wells.set_value(wid, 'sch_id', pos)
                    wells.set_value(wid, 'scheduled', 'yes')
                    wells.set_value(swapee, 'sch_id', empt)
                    print("well {0} moved to position {1}".format(swapee, empt))
                    print("well {0} moved to position {1}".format(wid, pos))
                    break
                else:
                    continue#print("well {0} cannot be moved to position {1}".format(wid, pos))
        
    report(wells)
    
def report(df):
    wellsSch= getSchd(df)
    wellsOOB= getOOB(df)
    wellsNotSch= getNotSchd(df)
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
    
setOOB(welldf)
setPrefs(welldf, schdf)
rankWells(welldf)

gm = greedyMatching(welldf, schdf)
if len(checkEmpty(schdf)) > 0:
    
    print "additional scheduling needed..."
    refineMatch(welldf, schdf)
    

#run a greedy matching
#check to see if there are empty positions on the schedule
#if so, check to see if the unscheduled wells will fit in the empty slot
#if not, check to see if wells can be shifted to accomidate interting non scheduled wells.




