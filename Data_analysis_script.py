"""
This script was created in order to prepare file for data analysis for cross sectional
study of cognition in patients with stress related mental disorders compared to
Mindmore normative data. 

In order for it to work we need data from three different sources:
    1. Test data from Mindmore
    2. Tracking of who did PRE and POST tests
    3. Demographic information from BASS for standardization
    
    Furthermore we need normative models from MM paper as well as updated norms
    for SDMT and Stroop. Currently in seperate script (mindmore_standardisation.py)


"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns
from test_occasion_calculator import what_test_occassion
from mindmore_standardisation import mindmore_standardiser


# Let's start of by importing the test data from Mindmore and getting the columns we need

test_data = pd.read_csv('ICBTTAU data 10-5-22.csv')

columns = ['BATTERY', 'CLICKRT', 'CTMT', 'CPT', 'RT', 'RAVLT', 'CORSI_BWD',
           'PASAT', 'TMT', 'BNT', 'TOKEN', 'TOH', 'CUBE','CLOCK',
           'CERAD_RECOGNITION']

for x in columns: 
    test_data = test_data.loc[:,~test_data.columns.str.startswith(x)]
    
#Capitalizing the pseudonyms
test_data['GENERAL_pseudonym'] = test_data['GENERAL_pseudonym'].str.upper()

#Getting only tests that were completed
test_data = test_data[test_data['GENERAL_completedAtTime'].notnull()]

#Getting the occasion for test
test_data = what_test_occassion(test_data)

#Finally standardizing the pseudonym column
test_data.rename(columns={'GENERAL_pseudonym':'code'}, inplace=True)

#For this analysis we're only interested in the PRE data.
test_data = test_data[test_data['test_or_retest'] == 't1']

test_data_columns = test_data.columns
###############################################################################


# Now let's do the same for BASS data
bass_data = pd.read_csv('20220507.csv', encoding='UTF-8', delimiter=',')

# For standardization and analysis we need edu, YOB, sex, and diagnosis
bass_columns = bass_data.columns

bass_data = bass_data[['Participant Id', 'ICBTvsTAU-DemV_1a_SCREEN',
                       'ICBTvsTAU-DemV_1b_SCREEN', 'ICBTvsTAU-DemV_3_SCREEN',
                       'KLIN_5d_SCREEN', 'SMBQ_sum18_Förmätn', 'PSS10_sum_Förmätn',
                       'ICBTvsTAU MADRS_sum_Förmätn']]

bass_data.rename(columns={'ICBTvsTAU-DemV_1a_SCREEN':'YOB', 'ICBTvsTAU-DemV_1b_SCREEN':'sex',
                          'ICBTvsTAU-DemV_3_SCREEN':'edu','KLIN_5d_SCREEN':'diagnosis',
                        'Participant Id':'code', 'SMBQ_sum18_Förmätn':'SMBQ', 
                        'PSS10_sum_Förmätn':'PSS10', 'ICBTvsTAU MADRS_sum_Förmätn':'MADRS'
                          }, inplace=True)

#Calculating EDU
bass_data = bass_data.replace({'FG1':8, 'FG2':9,'G1':11,'G2':12,
                               'EG1':14,'EG2':17,'FB':21})

#Changing variables for sex
bass_data['sex'] = bass_data['sex'].str.replace('K','woman')
bass_data['sex'] = bass_data['sex'].str.replace('M','man')

bass_data['age'] = 2022 - bass_data['YOB']

#By looking at this data we can see that we have 285 included participants in the
# study

###############################################################################

#Finally we'll have a look at the tracking data. 

status_data = pd.read_csv('Study cohort tracking.csv')

status_data = status_data[['registreringskod', 'Status_1']]
status_data.rename(columns={'registreringskod':'code'}, inplace=True)

#For this analysis we're only interested in the PRE data.
status_data = status_data[status_data['Status_1'] == 'Genomfört']

###############################################################################

# Let us now merge these three files together into one

merged_datafile = bass_data.merge(test_data, on='code',
                how='left').merge(status_data, on='code', how='inner')

columns_merged_datafile = merged_datafile.columns


x = mindmore_standardiser(merged_datafile)
merged_datafile = x.CERAD_learning()
merged_datafile = x.CERAD_recall()
merged_datafile = x.CORSI_FWD()
merged_datafile = x.FAS()
merged_datafile = x.SDMT()
merged_datafile = x.Stroop_index()

tables2 = np.round(pd.pivot_table(bass_data,values=['age', 'edu', 'PSS10',
                                            'SMBQ', 'MADRS' ], index=['diagnosis', 'sex'],
                                  margins=True, margins_name='Total', aggfunc=['count', np.mean, np.std,np.min, np.max]), 2)
tables2 = tables2.sort_index(axis=1, level=1, ascending=False).swaplevel(i=0, j=1, axis=1)
tables2 = tables2.round(2)
cols = tables2.columns.tolist()

#Make into string to create range row
tables2 = tables2.astype(str)

#Creating a range column for min and max values

tables2['edu', 'range'] = tables2['edu', 'amin'] + "-" + tables2['edu', 'amax']
tables2['age', 'range'] = tables2['age', 'amin'] + "-" + tables2['age', 'amax']
tables2['SMBQ', 'range'] = tables2['SMBQ', 'amin'] + "-" + tables2['SMBQ', 'amax']
tables2['PSS10', 'range'] = tables2['PSS10', 'amin'] + "-" + tables2['PSS10', 'amax']
tables2['MADRS', 'range'] = tables2['MADRS', 'amin'] + "-" + tables2['MADRS', 'amax']

#Getting the rows we're interested in, in the correct order

tables2 = tables2[[('age', 'count'),('age', 'mean'),('age', 'std'),('age', 'range'),
('edu', 'mean'),('edu', 'std'),('edu', 'range'),
('SMBQ', 'mean'),('SMBQ', 'std'),('SMBQ', 'range'),
('PSS10', 'mean'),('PSS10', 'std'),('PSS10', 'range'),
('MADRS', 'mean'),('MADRS', 'std'),('MADRS', 'range')]]

tables2 = tables2.transpose()

#Experimenting with some styling

tables2.style
tables2.style.set_precision(2)
tables2.style.background_gradient()

print(tables2)

# import seaborn as sns
plt.style.use('seaborn')

"ECDF function"
def ecdf(data):
    x = np.sort(data)
    y = np.arange(1, len(x)+1) / len(x)
    return(x, y)

def EDA(data):
    "This function plots standardised data using ECDF together with quantiles and CDF"
    
    standardised = data.filter(regex='z$')       
    # standardised = standardised.apply(lambda x: x.str.replace(',', '.'))
    standardised = standardised.apply(pd.to_numeric)
    
    # ex_ut = ""
    # ex_ut = ex_ut.filter(regex='z$')       
    # ex_ut = ex_ut.apply(lambda x: x.str.replace(',', '.'))
    # ex_ut = ex_ut.apply(pd.to_numeric)
    
    def ecdf(data):
        x = np.sort(data)
        y = np.arange(1, len(x)+1) / len(x)
        return(x, y)
     
    for columns in standardised:
        
        "Drop NA"
        a = standardised[columns].dropna()
        
        """
        Code to drop outliers +- 3 SD", not used
        
        """
        # greater_than = standardised[columns] > -3
        # less_than = standardised[columns] < 3
        # a = a[greater_than & less_than]
        
        # b = ex_ut[columns].dropna()
        # b_greater_than = ex_ut[columns] > -3
        # b_less_than = ex_ut[columns] < 3
        # b = b[b_greater_than & b_less_than]
                
        "Plot ECDF"
        x, y = ecdf(a)
        plt.plot(x, y, marker='.', linestyle='none', label='Empirical CDF')
        
        # ut_x, ut_y = ecdf(b)
        # plt.plot(ut_x, ut_y, marker='.', linestyle='none', label='Ex-ut')
        
        "Plot theoretical CDF"
        t_mean = np.mean(a)
        t_std = np.std(a)
        t_samples = np.random.normal(t_mean, t_std, size=10000)
        x_theor, y_theor = ecdf(t_samples)
        plt.plot(x_theor, y_theor, label='Theoretical CDF')
        
        "Plot quantiles"
        percentiles = np.array([25, 50, 75])
        percs = [0.25, 0.5, 0.75]
        perc_val = np.percentile(a, percentiles)
        print("percentiles=", perc_val)
        plt.plot(perc_val, percs, marker='o', linestyle='none', color='red')

        
        "Display labels, set margins, ticks, show plot"
        plt.xlabel('Z scores')
        plt.ylabel('ECDF')
        plt.title(str(columns))
        plt.margins(0.02)
        plt.xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        plt.legend()
        plt.show()
        
EDA(merged_datafile)

standardised = merged_datafile
standardised = standardised.filter(regex='z$')
standardised.apply(pd.to_numeric)
standardised = standardised.join(merged_datafile['diagnosis'])

# standardised = standardised.drop(['StroopInhibition_z',
#        'StroopWord_time_z', 'StroopWCorr_z', 'StroopColourWord_time_z',
#        'StroopWCcorr_z'], axis=1)

for columns in standardised:
    
    try: 
        sns.violinplot(x='diagnosis', y=columns, data=standardised)
        plt.show()
    except:
        continue


###############################################################################


# For adjustment disorder creating a table with t-tests for parametric measures
# and Wilcoxon signed rank for non-parametric measures

# standardised = standardised[standardised['diagnosis'] == 'AS']
# standardised = standardised.filter(regex='z$')
# standardised.apply(pd.to_numeric)

# t_test = []
# for columns in standardised:
#         a = standardised[columns].dropna()
#         t_test.append(stats.ttest_1samp(a, 0, alternative='less'))

# col = standardised.columns.tolist()
# t_test = pd.DataFrame(t_test, index = col)

# t_test.round(4)

# t_test = t_test.rename(columns = {'statistic': 't_test_statistic'})

# wilcoxon = []

# t_test = t_test.reset_index()

# combined = t_test
# adcombined = combined.set_index('index').sort_index()
# adcombined = adcombined.reset_index()

# adcombined['diagnosis'] = 'AD'

# # For exhaustion disorder 

# standardised = merged_datafile

# standardised = standardised[standardised['diagnosis'] == 'UT']
# standardised = standardised.filter(regex='z$')
# standardised.apply(pd.to_numeric)

# t_test = []
# for columns in standardised:
#         a = standardised[columns].dropna()
#         t_test.append(stats.ttest_1samp(a, 0, alternative='less'))

# col = standardised.columns.tolist()
# t_test = pd.DataFrame(t_test, index = col)

# t_test.round(4)

# t_test = t_test.rename(columns = {'statistic': 't_test_statistic'})

# wilcoxon = []

# t_test = t_test.reset_index()

# combined = t_test
# utcombined = combined.set_index('index').sort_index()

# utcombined = utcombined.reset_index()
# utcombined['diagnosis'] = 'UT'

# #Combining AD and UT creating a unified table for both diagnosis

# combiner = utcombined.merge(adcombined, how='outer')
# combiner = combiner.pivot_table(index='index', columns='diagnosis')
# combiner = combiner.swaplevel(axis=1).sort_index(axis=1)

# #Retrieving descriptive statistics for the measures for each diagnosis
# standardised = merged_datafile
# mean_sd = standardised.pivot_table(values=['CERAD_learning_z','CERAD_recall_z','CORSI_FWD_z',
#                                     'FAS_z'], columns='diagnosis',aggfunc = ['count',np.mean, np.std])

# mean_sd = mean_sd.swaplevel(axis=1).sort_index(axis=1)
# mean_sd = mean_sd.rename(columns={"AS": "AD"})

# #Merging all data together

# all_data = pd.merge(mean_sd, combiner, left_index=True,right_index=True)
# all_data = all_data.reset_index()
# all_data = all_data.sort_index(axis=1)
# all_data = all_data.rename(columns={'': 'TEST'})
# all_data = all_data.set_index('index','TEST')
# all_data = all_data.stack().round(4)

# orderlist = [  
#               (('CERAD_learning_z',), 'count'), (('CERAD_learning_z',), 'mean'), (('CERAD_learning_z',), 'std'),
#  (('CERAD_learning_z',), 't_test_statistic'),  (('CERAD_learning_z',), 'pvalue'),
#     (('CERAD_recall_z',), 'count'), (('CERAD_recall_z',), 'mean'),
#  (('CERAD_recall_z',), 'std'), 
#  (('CERAD_recall_z',), 't_test_statistic'), 
#      (('CERAD_recall_z',), 'pvalue'),           

#  (('CORSI_FWD_z',), 'count'), (('CORSI_FWD_z',), 'mean'),
#  (('CORSI_FWD_z',), 'std'),
#  (('CORSI_FWD_z',), 't_test_statistic'),
#     (('CORSI_FWD_z',), 'pvalue'),
#              (('FAS_z',), 'count'),
#  (('FAS_z',), 'mean'), (('FAS_z',), 'std'),
#  (('FAS_z',), 't_test_statistic'), (('FAS_z',), 'pvalue')
# ]

# all_data = all_data.reindex(orderlist)

# all_data.style

# def even_number_background(cell_value):

#     highlight = 'background-color: red;'
#     default = ''

    
#     if type(cell_value) in [float, int]:
#         if cell_value < 0.05:
#             return highlight
#     return default

# all_data = all_data.style.applymap(even_number_background, subset=pd.IndexSlice[pd.IndexSlice[:,'pvalue'], :])



# print(all_data.index.values)

# all_data

# merged_datafile.head().to_csv('for_wobbie_100522.csv')

# merged_datafile.to_csv('ludwig-victoria100522.csv', encoding='UTF-8-sig')
