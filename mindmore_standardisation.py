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
        self.df['CERAD_predicted'] = 31.7942156995638 + (-0.0875905541536407 * self.df['age']) +\
            (self.df['eduInv'] * -75.9733008123953)
        self.df['CERAD_learning_z'] = (self.df['CERAD_LEARNING'] \
            - self.df['CERAD_predicted']) / 3.24313630994147
        self.df.drop('CERAD_predicted', axis=1, inplace=True)
            
        return self.df
    
    def CERAD_recall(self):
        
        self.df['CERAD_recall_predicted'] = 12.7904955190877 + (self.df['age']*-0.0501897879003986) +\
            (self.df['eduInv'] * -33.7554737721963) + (-0.810824961274903 * self.df['sex'])
            
        self.df['CERAD_recall_z'] = (self.df['CERAD_DELAYED'] \
            - self.df['CERAD_recall_predicted']) / 1.89431914995295
        
        self.df.drop('CERAD_recall_predicted', axis=1, inplace=True)
    
    def CORSI_FWD(self):
        
        self.df['CORSI_FWD_predicted'] = 5.82930531887294 + (self.df['age']*0.016789664249949) + \
            (self.df['age2']*-0.000465225653294214) + (self.df['edu']*0.0435293550465566) + \
                (self.df['sex']*0.272833659477026)
                
        self.df['CORSI_FWD_z'] = (self.df['CORSI_FWD_SPAN'] - \
            self.df['CORSI_FWD_predicted']) / 1.01018250326044
            
        self.df.drop('CORSI_FWD_predicted', axis=1, inplace=True)
        
        df = self.df
        return df
    
    def FAS(self):
        
        self.df['FAS_predicted'] = 31.9386200030632 + (self.df['edu']*0.92077653545719)
                
        self.df['FAS_z'] = (self.df['FAS_INDEX'] - \
            self.df['FAS_predicted']) / 13.5770025270257
            
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
                SDMT_PREDICTED = 56.0462056475881 + (-0.0615085632106278 * row['age']) + \
                    (-0.00492377037979746 * row['age2']) + (0.553681784665026 * row['edu'])
                SD = 6.88771206095076
                
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
                Stroop_PREDICTED = 18.2684200875865 + (-0.116902227050743 * row['age'])
                SD = 2.76981099623645
                
                return (row['STROOP_INDEX'] - Stroop_PREDICTED) / SD


            

        self.df['Stroop_index_z'] = self.df.apply(lambda row: Stroop_standardizer(row), axis=1)
        df = self.df
        return df
    
                

        