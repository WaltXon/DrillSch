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


wells = sw.getWells()
sch = pd.DataFrame.from_records(rs.rigSchedule())

print sch



