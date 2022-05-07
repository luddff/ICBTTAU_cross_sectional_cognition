# -*- coding: utf-8 -*-
"""
Created on Sat May  7 12:39:52 2022

@author: Luddff
"""

def what_test_occassion(df):
    
    """
    This function calculates a new column of test_or_retest based on duplicate
    pseudonyms and testoccasions
    
    
    
    """
    
    
    test_or_retest = []
    x1 = ""
    x2 = ""
    x3 = ""
    x4 = ""
    
    for row in df['GENERAL_pseudonym']:
        if row == x1:
            
            if row == x2:
                test_or_retest.append('More than two test occassions')
            else: 
                test_or_retest.append('t2')
                x2 = str(row)
        else: 
            test_or_retest.append('t1')
            x1 = str(row)
    
    df['test_or_retest'] = test_or_retest
    
    return df