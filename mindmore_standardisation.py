# -*- coding: utf-8 -*-
"""
Mindmore standardization script for:
    1. CERAD Learning
    2. CERAD recall
    3. STROOP
    4. FAS
    5. SDMT


"""

import pandas as pd

class mindmore_standardiser:
    
    def __init__(self, df):
        self.df = df
        
        self.df['eduInv'] = 1/self.df['edu']
        self.df['age2'] = self.df['age']**2
        self.df['ageEdu'] = self.df['age']*self.df['edu']
        self.df['sex'].replace({'man':1, 'woman':0}, inplace=True)


    def CERAD_learning(self):
        self.df['CERAD_predicted'] = 31.794 + (-0.088 * self.df['age']) +\
            (self.df['eduInv'] * -75.973)
        self.df['CERAD_learning_z'] = (self.df['CERAD_LEARNING'] \
            - self.df['CERAD_predicted']) / 3.243
        self.df.drop('CERAD_predicted', axis=1, inplace=True)
            
        return self.df
    
    def CERAD_recall(self):
        
        self.df['CERAD_recall_predicted'] = 12.790 + (self.df['age']*-0.05) +\
            (self.df['eduInv'] * -33.755) + (-0.811 * self.df['sex'])
            
        self.df['CERAD_recall_z'] = (self.df['CERAD_DELAYED'] \
            - self.df['CERAD_recall_predicted']) / 1.894
        
        self.df.drop('CERAD_recall_predicted', axis=1, inplace=True)
    
    def CORSI_FWD(self):
        
        self.df['CORSI_FWD_predicted'] = 5.829 + (self.df['age']*0.017) + \
            (self.df['age2']*-0.0005) + (self.df['edu']*0.044) + \
                (self.df['sex']*0.273)
                
        self.df['CORSI_FWD_z'] = (self.df['CORSI_FWD_SPAN'] - \
            self.df['CORSI_FWD_predicted']) / 1.010
            
        self.df.drop('CORSI_FWD_predicted', axis=1, inplace=True)
        
        df = self.df
        return df
    
    def FAS(self):
        
        self.df['FAS_predicted'] = 31.939 + (self.df['edu']*0.921)
                
        self.df['FAS_z'] = (self.df['FAS_INDEX'] - \
            self.df['FAS_predicted']) / 13.577
            
        self.df.drop('FAS_predicted', axis=1, inplace=True)
        
        df = self.df
        return df

        