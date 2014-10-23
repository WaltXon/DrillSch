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
    #print('wellsOutOfBounds = {0}'.format(wellsOutOfBounds))    
    for oob in wellsOutOfBounds: 
        wells.set_value(oob, 'scheduled', 'OOB')
    return wellsOutOfBounds
    
def getSchd(wells):
    return [w for w in wells.index if wells.get_value(w, 'scheduled') == 'yes']
def getOOB(wells):
    return [w for w in wells.index if wells.get_value(w, 'scheduled') == 'OOB']
def getNotSchd(wells):
    return [w for w in wells.index if wells.get_value(w, 'scheduled') == 'no']
def swap(swapee, empt, swap_well, swappos):
    #move the swap well to the empty slot
    schdf['well'][empt] = welldf['name'][swapee]
    schdf['well_id'][empt] = swapee
    #move the new well into the now open spot formerly occupied by the swap well
    schdf['well'][swappos] = welldf['name'][swap_well]
    schdf['well_id'][swappos] = swap_well
    #update the welldf table to show the new positions
    welldf['sch_id'][swap_well] = swappos
    welldf['scheduled'][swap_well] = 'yes' 
    welldf['sch_id'][swapee] = empt
    print("swap well {0} ({1}) moved from position {2} to empty position {3}".format(welldf['name'][swapee], swapee, swappos, empt))    
    print("new well {0} ({1}) moved to position {2}".format(welldf['name'][swap_well], swap_well, swappos))
    
    
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
    

def refineMatchInner(wells, sch, prefs, wid):
    for pos in prefs:
        print('pos = {0}'.format(pos))
        #get the id of the well in the first pref spot
        swapee = sch['well_id'][pos]
        print('swapee = {0}'.format(swapee))
        #get a list of the empty spots
        for empt in getEmpty(sch):
            print('empt = {0}'.format(empt))
            #check to see if the well currently occuping the swap spot could legaly be moved to
            #an empty spot
            if checkExp(swapee, empt) == 'GOOD':
                #swap the existing well into the empty spot and the new well into the swap spot                    
                swap(swapee, empt, wid, pos)
                return

def refineMatchOuter(wells, sch):
    wellsToSchedule = [w for w in wells.index if wells.get_value(w, 'scheduled') == 'no']
    res = welldf.iloc[wellsToSchedule].sort(columns='rank', axis=0, ascending=False) #TRUE OR FALSE
    print('')
    print('--------')    
    print wells
    print('--------')    
    print sch    
    print('--------')
    print res
    print('--------')
    #step through the list of wells that are not scheduled
    for wid in res.index:
        print('---')
        print('wid = {0}'.format(wid))
        print('---')
        #get a list of thier possible rig spots
        prefs = res.get_value(wid, 'pref')
        #start from the last position and move forward
        prefs.reverse()
        #step through possible preferred rig spots
        refineMatchInner(wells, sch, prefs, wid)


    
    report(wells)

def finalMatch(wells, sch):
    pass


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
    

setPrefs(welldf, schdf)
rankWells(welldf)
setOOB(welldf)

greedyMatching(welldf, schdf)
if len(getEmpty(schdf)) > 0:
    print('')
    print "additional scheduling needed..."
    refineMatchOuter(welldf, schdf)
welldf['pref'].astype(str)
scht = schdf[['well_id','spud']]
merged = pd.merge(welldf, scht, left_index=True, right_on='well_id', how='left' ) #, axis=1, join='inner', join_axes=[welldf.index, schridx.index])
#merged.to_excel(r'C:\Users\WaltN\Desktop\GitHub\DrillSch\result.xlsx')
mgsort =  merged.sort(columns='spud', ascending=True)
print mgsort
#run a greedy matching
#check to see if there are empty positions on the schedule
#if so, check to see if the unscheduled wells will fit in the empty slot
#if not, check to see if wells can be shifted to accomidate interting non scheduled wells.




