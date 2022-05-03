# -*- coding: utf-8 -*-
"""
Created on Tue May  3 14:30:38 2022

@author: FRF8
"""

import pandas as pd

# Let's start of by importing the test data from Mindmore

test_data = pd.read_csv('ICBTTAU data 3-5-22.csv')

columns = ['BATTERY', 'CLICKRT', 'CTMT', 'CPT', 'RT', 'RAVLT', 'CORSI_BWD',
           'PASAT', 'TMT', 'BNT', 'TOKEN', 'TOH', 'CUBE','CLOCK',
           'CERAD_RECOGNITION']

for x in columns: 
    test_data = test_data.loc[:,~test_data.columns.str.startswith(x)]

# Now let's do the same for 
bass_data = pd.read_csv('20220503.csv', encoding='unicode_escape', delimiter=';')
