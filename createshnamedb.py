# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 09:31:52 2014

@author: waltn
"""
import string
import cPickle as pickle
#from bs4 import BeautifulSoup
#
#f = open('C:\Users\WaltN\Desktop\GitHub\DrillSch\Superhero Database.htm', 'r')
#soup = BeautifulSoup(f)
#
#print(soup.get_text())

with open('C:\Users\WaltN\Desktop\GitHub\DrillSch\sh.txt', 'r') as f:
    text = f.read()

word = []
heros = []
for char in text: 
    if char in string.digits:
        if len(word) > 0:
          heros.append(''.join(word).strip())
          word = []
       
    else:
        word.append(char)
        
        
print heros
pickle.dump(heros, open('C:\Users\WaltN\Desktop\GitHub\DrillSch\sh.p', 'wb'))