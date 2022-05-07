"""
This script was created in order to prepare file for data analysis for cross sectional
study of cognition in patients with stress related mental disorders compared to
Mindmore normative data. 

In order for it to work we need data from three different sources:
    1. Test data from Mindmore
    2. Tracking of who did PRE and POST tests
    3. Demographic information from BASS for standardization
    
    Furthermore we need normative models from MM paper as well as updated norms
    for SDMT and Stroop.


"""

import pandas as pd
from test_occasion_calculator import what_test_occassion
from mindmore_standardisation import mindmore_standardiser


# Let's start of by importing the test data from Mindmore and getting the columns we need

test_data = pd.read_csv('ICBTTAU data 3-5-22.csv')

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
                       'KLIN_5d_SCREEN']]

bass_data.rename(columns={'ICBTvsTAU-DemV_1a_SCREEN':'YOB', 'ICBTvsTAU-DemV_1b_SCREEN':'sex',
                          'ICBTvsTAU-DemV_3_SCREEN':'edu','KLIN_5d_SCREEN':'diagnosis',
                        'Participant Id':'code'
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
x.CERAD_learning()
x.CERAD_recall()



# merged_datafile.to_csv('data_070522.csv')




