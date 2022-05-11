# -*- coding: utf-8 -*-
"""
Mindmore standardization script for:
    1. CERAD Learning
    2. CERAD recall
    3. STROOP Index
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
        self.df['GENERAL_inputDevice'].replace({'mouse':0, 'trackpad':1}, inplace=True)


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

    def SDMT(self):
        
        def sdmt_standardizer(row):
            """
            Additional function in order to determine what model to standardize
            by
            
            
            """
            if row['GENERAL_inputDevice'] == 1:
                SDMT_PREDICTED = 68.931 + \
                (-4.441 * row['GENERAL_inputDevice']) + \
                (-0.477 * row['age']) + \
                    (1.656 * row['sex'])
                SD = 6.615                                
                
                return (row['SDMT_CORRECT'] - SDMT_PREDICTED) / SD
                           


            if row['GENERAL_inputDevice'] == 0:
                SDMT_PREDICTED = 68.931 + \
                (-4.441 * row['GENERAL_inputDevice']) + \
                (-0.477 * row['age']) + \
                    (1.656 * row['sex'])
                SD = 6.615                                
                
                return (row['SDMT_CORRECT'] - SDMT_PREDICTED) / SD
        
            elif row['GENERAL_inputDevice'] == 'touchscreen':
                SDMT_PREDICTED = 56.046 + (-0.062 * row['age']) + \
                    (-0.005 * row['age2']) + (0.554 * row['edu'])
                SD = 6.888
                
                return (row['SDMT_CORRECT'] - SDMT_PREDICTED) / SD


            

        self.df['SDMT_z'] = self.df.apply(lambda row: sdmt_standardizer(row), axis=1)
        df = self.df
        return df
    
    def Stroop_index(self):

        def Stroop_standardizer(row):
            """
            Additional function in order to determine what model to standardize
            by
            
            
            """
            if row['GENERAL_inputDevice'] == 1:
                Stroop_PREDICTED = 20.994 + \
                (-1.929 * row['GENERAL_inputDevice']) + \
                (-0.147 * row['age'])
                SD = 2.395                                
                
                return (row['STROOP_INDEX'] - Stroop_PREDICTED) / SD
                           
            if row['GENERAL_inputDevice'] == 0:
                Stroop_PREDICTED = 20.994 + \
                (-1.929 * row['GENERAL_inputDevice']) + \
                (-0.147 * row['age'])
                SD = 2.395                                
                
                return (row['STROOP_INDEX'] - Stroop_PREDICTED) / SD
        
            elif row['GENERAL_inputDevice'] == 'touchscreen':
                Stroop_PREDICTED = 18.268 + (-0.117 * row['age'])
                SD = 2.770
                
                return (row['STROOP_INDEX'] - Stroop_PREDICTED) / SD


            

        self.df['Stroop_index_z'] = self.df.apply(lambda row: Stroop_standardizer(row), axis=1)
        df = self.df
        return df
    
                

        