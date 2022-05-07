
"""
This script is designed to prepare data for analysis. Originally created for
Click TMT and input device norms

Files required:
    
    For authentication and retrieving questionnaire data:
        
    1. Google authenticator
    
    For analysis:
        
    1. Form answers (CTMT- Google Sheets)
    2. Research export (Resultportal export CSV)
    3. New tests export (From resultportal - Aggregera resultat)
    4. Manual extraction with testOccasion, date, input method, and comments 
        from test application (Lars does this currently 23/02/2022)
    5. Form answers from RT sheets (2020-2021)
    6. Form answers for NS sheets
    7. Form answers

To do:
    
    1. Merge ctmt into one function
    2. Create a list of columns and start deleting unneccessary ones
    3. 

"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import sys

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('western-diorama-333212-26384475db08.json', scope)
client = gspread.authorize(creds)

research_export = pd.read_csv('Data files/research.csv', delimiter = ",", low_memory=False)

def click_tmt_form_import():
    """
    This function gets the formanswers to CTMT

    Returns all formanswers for CTMT
    

    """
    
    
    #Questionnaire data for Click-TMT
    
    ## Find workbook by name and open the correct sheet
    ## use creds to create a client to interact with the Google Drive API
    
    sheet = client.open("Participant count (Click-TMT and input device norms)")
    worksheet = sheet.worksheet("Remote research questionnaire")
    
    ## Extract and print all of the values
    list_of_hashes = worksheet.get_all_values()
    df = pd.DataFrame(list_of_hashes)
    
    ## Creating the first df with all the questionnaire answers
    formanswers = df.rename(columns=df.iloc[0]).drop(df.index[0])
    
    #Get all that have been at least reviewed
    formanswers = formanswers[formanswers['Include_CTMT'].str.contains('Yes|No|Exclude|Review')    ]

    
    formanswers = formanswers[formanswers['Deltagarkod'].str.contains('INP|SINP|SKO')    ]
    
    # duplicated = formanswers[formanswers.duplicated(subset=['code'], keep=False)]
    
    # if(len(duplicated) > 0):
    #     print("Please check duplicate entries in the Click-TMT questionnaire sheets")
    #     sys.exit()
        
    formanswers['HADS_A'] = formanswers['HADS_A'].astype(int)
    formanswers['HADS_D'] = formanswers['HADS_D'].astype(int)
    formanswers['KEDS'] = formanswers['KEDS'].astype(int)

    formanswers.loc[formanswers.HADS_A > 10, 'Include_CTMT'] = 'Exclude'
    formanswers.loc[formanswers.HADS_A > 10, 'reason_for_exclusion'] = \
        formanswers.loc[formanswers.HADS_A > 10, 'reason_for_exclusion'] + ', High HADS_A score'

    formanswers.loc[formanswers.HADS_D > 10, 'Include_CTMT'] = 'Exclude'
    formanswers.loc[formanswers.HADS_D > 10, 'reason_for_exclusion'] = \
        formanswers.loc[formanswers.HADS_D > 10, 'reason_for_exclusion'] + ', High HADS_D score'
    
    formanswers.loc[formanswers.KEDS > 18, 'Include_CTMT'] = 'Exclude'
    formanswers.loc[formanswers.KEDS > 18, 'reason_for_exclusion'] = \
        formanswers.loc[formanswers.KEDS > 18, 'reason_for_exclusion'] + ', High KEDS score'

    ## If we only want the rows with participants who've been included and done test
    # formanswers = formanswers[formanswers['DoneTest'] == 'Yes']    
    
    ## Dropping some unneccessary columns
    x = formanswers.columns.get_loc('Jag känner mig spänd och nervös (Å)')
    y = formanswers.columns.get_loc('Irritation och ilska')
    
    formanswers.drop(list(formanswers)[x:y+1], axis=1, inplace=True)
    formanswers.drop(['TestReminder', 'test_retest_offer', 'Test_reminder_2',
                      'Result_combined', 'SentResult', 'Belöningskod',
                      'Ifall ja, vilken typ',
                      'Jämfört med tidigare (några månader) upplever du försämrat minne eller koncentrationsförmåga?',
                      'Har ni upplevt några personlighetsförändringar de senaste 6 månaderna?',
                      'Har du blivit diagnosticerad med en psykisk sjukdom eller syndrom? Ja/Nej, Ifall ja vilken?',
                      'Tar du någon medicin regelbundet som kan påverka din hjärnfunktion?',
                      'Har du behandling för hjärt och/eller kärlsjukdom? ',
                      'Har du haft hjärnblödning eller blodpropp i hjärnan? Ifall ja, var vänligen beskriv tidpunkt och om du behandlas nuvarande',
                      'Har du någon neurologisk sjukdom som Parkinson, MS, epilepsi eller migrän?',
                      'Har du någon hormonell sjukdom?',
                      'Har du diabetes? Ifall ja, är den behandlad?',
                      'Har du någonsin fått en allvarlig hjärnskakning? Ifall ja, när? Krävdes en sjukhusvistelse?',
                      'Har du blivit diagnosticerad med ett neuropsykiatriskt tillstånd?',
                      'Har du blivit diagnosticerad med inlärningssvårigheter?',
                      'Har du ett tidigare eller pågående alkohol/substansmissbruk?',
                      'ResentTest', 'Exclusion_mail', 'In_office_email',
                      'Jag har fått skriftlig information om studien och har haft'+
                      ' möjlighet att ställa frågor. Jag får behålla den skriftliga'+
                      ' informationen som jag fått på mailen.'], axis=1, inplace=True)
    
    ## Renaming columns to fit with the old RT file
    formanswers = formanswers.rename(columns={'Födelsedatum':'YOB','Ålder': 'age', 'Kön': 'sex',
                         'Utbildningsnivå, hur många år har du studerat?': 'education',
                         'Vad är din språknivå på svenska?':'language',
                         'Deltagarkod': 'code', 'Kommer du att använda mus eller touchpad?':
                             'Mouse_touchpad', 'Bor du i en stad, by eller landsbygd?':
                                 'city_village_remote', 'SPMSQ_vb': 'SPMSQ',
     'Kommer du att använda en inbyggd skärm eller en externt inkopplad datorskärm?':
         'External_Display',
'Kommer du att använda inbyggd mikrofon och högtalare, headset, eller högtalare'+
' och extern mikrofon?':'Headset',         
         'Timestamp': 'form_date', 
         'Kommer du att använda en stationär dator eller en laptop för att utföra testet?':
             'Desktop_Laptop_surface', 'Include_CTMT':'include', 'Note':'note',
             'Var vänlig skatta din vana med att använda ovannämnda inmatningsmetod':
                 'Input_method_comfortability', 'Conditions':'condition'
                                 
                            
                                 })
        
    
    ## Formatting columns to fit with old file
    
    formanswers['sex'] = formanswers['sex'].str.replace('Kvinna','woman')
    formanswers['sex'] = formanswers['sex'].str.replace('Man','man')
    formanswers['YOB'] = formanswers['YOB'].str[-4:]
    formanswers['sex'] = formanswers['sex'].str.replace('Kvinna','woman')
    formanswers['sex'] = formanswers['sex'].str.replace('Man','man')
    
    formanswers['Mouse_touchpad'] = formanswers['Mouse_touchpad'].str.replace(
        'Mus','Mouse')
    formanswers['Mouse_touchpad'] = formanswers['Mouse_touchpad'].str.replace('Touchskärm'
                                                                        ,'Touchscreen')
    
    formanswers = formanswers.reindex(columns=['code', 'YOB', 'age', 'sex', 'education',
                                               'include', 'reason_for_exclusion',
           'DoneTest', 'Done_retest','Controlled_environment', 'language',
           'Ifall ditt modersmål inte är svenska, vad är det?',
           'Ifall ditt modersmål inte är svenska, hur många år sedan började du lära dig svenska?',
           'Yrke (frivillig fråga)',
           'Har du deltagit i en Mindmore studie tidigare eller har tidigare erfarenhet av kognitiva tester?',
           'Ifall ja, var vänligen beskriv din tidigare erfarenhet',
           'Var vänlig skatta din vana vid att använda er dator (1-10)',
           'Desktop_Laptop_surface', 'Mouse_touchpad', 'External_Display',
           'Vilken skärmstorlek kommer du använda?', 'Input_method_comfortability',
           'Headset', 'Är du färgblind?', 'HADS_A', 'HADS_D', 'KEDS', 'SPMSQ',
           'Kommer du utföra testningen på vårt kontor eller hemifrån?',
           'Övriga frågor eller kommentarer', 'city_village_remote', 'condition',
           'note', 'SentTest',
           'Battery_RT_or_CPT', 'Sent_Retest', 'form_date'])
    
    
    return formanswers

ctmt_formanswers = click_tmt_form_import()

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

# formanswers.to_csv('Data files/Created files/formanswers.csv', encoding='utf-8', sep=';')

def rt_form_import():
    #Loading testapp data from RT
    ## Find workbook by name and open the correct sheet
    sheet = client.open("Participant count (RT '20)")
    worksheet = sheet.worksheet("details")
    
    ## Extract and print all of the values
    list_of_hashes = worksheet.get_all_values()
    df = pd.DataFrame(list_of_hashes)
    
    ## Creating the first df with all the questionnaire answers
    RT_data = df.rename(columns=df.iloc[0]).drop(df.index[0])
    
    
    # This file was used previously but it only contains included participants
    ## RT_data = pd.read_csv('Data files/data_RT_standardised_excluded_20210504.csv',
    #                       delimiter = ";")
    
    
    RT_data['HADS_A'] = pd.to_numeric(RT_data['HADS_A'], errors='coerce')
    RT_data['HADS_D'] = pd.to_numeric(RT_data['HADS_D'], errors='coerce')
    RT_data['KEDS'] = pd.to_numeric(RT_data['KEDS'], errors='coerce')
            
    RT_data["reason_for_exclusion"] = ""

    
    RT_data.loc[RT_data.HADS_A > 10, 'include_RT'] = 'Exclude'
    RT_data.loc[RT_data.HADS_A > 10, 'reason_for_exclusion'] = \
        RT_data.loc[RT_data.HADS_A > 10, 'reason_for_exclusion'] + ', High HADS_A score'

    RT_data.loc[RT_data.HADS_D > 10, 'include_RT'] = 'Exclude'
    RT_data.loc[RT_data.HADS_D > 10, 'reason_for_exclusion'] = \
        RT_data.loc[RT_data.HADS_D > 10, 'reason_for_exclusion'] + ', High HADS_D score'
    
    RT_data.loc[RT_data.KEDS > 18, 'include_RT'] = 'Exclude'
    RT_data.loc[RT_data.KEDS > 18, 'reason_for_exclusion'] = \
        RT_data.loc[RT_data.KEDS > 18, 'reason_for_exclusion'] + ', High KEDS score'
    
    #If we only want included participants
    ##RT_data = RT_data[RT_data['include_RT'] == 'yes']
    
    
    RT_data['include_RT'] = RT_data['include_RT'].str.title()
    RT_data = RT_data[RT_data['include_RT'].str.contains('Yes|No|Maybe|Exclude')]
    
    RT_data['sex'] = RT_data['sex'].str.replace('Woman','woman')
    RT_data['sex'] = RT_data['sex'].str.replace('Man','man')
    
    RT_data.drop(columns = ['Sent_email', 'ConsentQuestionnaire_reminder',
                            'ConsentForm', 'TestReminder',
                            'Personnummer', 'Result_combined', 'SentResult',
                            'ResentTest', 'Test_version',
                            'Code_Screener'], inplace=True)
    
    RT_data = RT_data.rename(columns={'include_RT': 'include'})

    
    return RT_data

RT_form_data = rt_form_import()

#Merging CTMT and RT participant sheets

RT_CTMT_merge = pd.concat([ctmt_formanswers, RT_form_data])


#Merging all of our participant sheet docs
RT_CTMT_merge.to_csv('Data files/Created files/ingvar_wobbie_090322_formanswers.csv', 
                     sep=';', encoding='utf-8-sig', index=False)


def click_tmt_results():
    
    """
    This function gets the results from the researchexport and returns test results
    for these participants who've done the test
    
    """
    
    #Creating researchexport
    res_data = research_export
    
    ## Subset data that contains correct prefix
    res_data = res_data[res_data['Patient Code'].str.contains('INP|SKO')==True]
    
    ## Removing 'Tests'
    res_data = res_data[~res_data['Patient Code'].str.contains("TEST")]
    
    ## We're going to merge files on testOccassion when available. This file however
    ## will be merged on 'Date column'. It needs to be prepared
    
    res_data['Date'] = res_data.Date.str[:24]
    
    ##Renaming columns 
    res_data = res_data.rename(columns={'Patient Code': 'code'})
    
    
    return res_data

res_data = click_tmt_results()

#Merging the above two results
merged1 = res_data.merge(RT_CTMT_merge, on='code', how='outer')

#Creating CSV for Lars to extract comments and TestOcassion for merging

# res_data.to_csv('Analysis prep/Data files/Created files/to_lars.csv')

def VS_NS_import(): #Include only 'yes' and 'no'
    
    """
    This function gets the questionnaire data for the normative and RS study
    
    
    """
    #Creating file for VS, NS
    
    ##Importing questionnaires
    
    ## use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('western-diorama-333212-26384475db08.json', scope)
    client = gspread.authorize(creds)
    
    ## Find workbook by name and open the correct sheet
    sheet = client.open("Copy of Participant count (NS '19) 2022 new exclusion criteria")
    worksheet = sheet.worksheet("details")
    
    ## Extract and print all of the values
    list_of_hashes = worksheet.get_all_values()
    df = pd.DataFrame(list_of_hashes)
    
    ## Creating the first df with all the questionnaire answers
    ns_formanswers = df.rename(columns=df.iloc[0]).drop(df.index[0])
    
    
    ## Calculating and excluding based of MADRS
    ns_formanswers['MADRS-S'] = pd.to_numeric(ns_formanswers['MADRS-S'], errors='coerce')
    ns_formanswers.rename(columns={"MADRS-S": "MADRS_S"}, inplace=True)
    
    ns_formanswers.loc[ns_formanswers.MADRS_S > 19, 'include'] = 'No'
    
    ## If we only want the rows with participants who've been included
    # ns_formanswers = ns_formanswers[ns_formanswers['Include'] == 'yes']
    
    ns_formanswers = ns_formanswers[ns_formanswers['include'].str.contains('yes|no|exclude|Review')    ]

    
    ns_formanswers = ns_formanswers.loc[ns_formanswers['code']
                                        .str.startswith(('VS', 'NS'))==True]
    
    ##Dropping unneccesary rows
    ns_formanswers.drop(columns=['Date', 'Results sent'], inplace=True)
    
    #Let's now get the data from the ns file
    
    ns_data = pd.read_csv('Data files/research.csv', delimiter = ",", low_memory=False)
    
    ns_data = ns_data.loc[ns_data['Patient Code'].str.startswith(('vs', 'ns'))==True]
    
    ns_data.rename(columns={'Patient Code': 'code'}, inplace=True)
    ns_data['code'] = ns_data['code'].str.upper()
    
    ns_merge = ns_data.merge(ns_formanswers, on='code', how='outer')
    
    return ns_merge, ns_formanswers

ns_merge = VS_NS_import()

def rs_import():
    
    ## Find workbook by name and open the correct sheet
    sheet = client.open("Copy of Participant count (RS '20) 2022 new exclusion criteria")
    worksheet = sheet.worksheet("details")
    
    ## Extract and print all of the values
    list_of_hashes = worksheet.get_all_values()
    df = pd.DataFrame(list_of_hashes)
    
    ## Creating the first df with all the questionnaire answers
    rs_formanswers = df.rename(columns=df.iloc[0]).drop(df.index[0])
    
    # Code below will reformat questionnaire answers and exclude participants
    # based on high scores
    
    rs_q_columns = [col for col in rs_formanswers.columns if 'HADS' in col]
    rs_q_columns = rs_q_columns + [col for col in rs_formanswers.columns if 'KEDS' in col]
    
    ## Excluding participants who've scored above
    
    for x in rs_q_columns:
        rs_formanswers[x] = pd.to_numeric(rs_formanswers[x], errors='coerce')
    
    #Renaming columns to make legible
    rs_formanswers.rename(columns = {'HADS-D_T1': 'HADS_D_T1', 'HADS-A_T1': 'HADS_A_T1',
                                      'HADS-D_T2': 'HADS_D_T2', 'HADS-A_T2':'HADS_A_T2'}, inplace=True)
    
    
    rs_formanswers.loc[rs_formanswers.KEDS_T1 > 18, 'include_NS'] = 'no'
    rs_formanswers.loc[rs_formanswers.KEDS_T2 > 18, 'include_NS'] = 'no'
    rs_formanswers.loc[rs_formanswers.HADS_D_T1 > 18, 'include_NS'] = 'no'
    rs_formanswers.loc[rs_formanswers.HADS_D_T2 > 18, 'include_NS'] = 'no'
    rs_formanswers.loc[rs_formanswers.HADS_A_T1 > 18, 'include_NS'] = 'no'
    rs_formanswers.loc[rs_formanswers.HADS_A_T2 > 18, 'include_NS'] = 'no'
    
    #If we only want included participants
    ## rs_formanswers = rs_formanswers[rs_formanswers['include_NS'] == 'yes']

    #Import RS data from the test application
    
    rs_data = research_export
    rs_data = rs_data.loc[rs_data['Patient Code'].str.startswith(('rs'))==True]
    
    rs_data.rename(columns={'Patient Code': 'code'}, inplace=True)
    rs_data['code'] = rs_data['code'].str.upper()
    
    rs_merge = rs_data.merge(rs_formanswers, on='code', how='outer')
    
    return rs_merge, rs_formanswers

rs_merge = rs_import()[0]
    
def rt_import():
    """
    
    This function will retrieve test application data for RT
    and return this as a df


    """
    
    

    
    RT_testdata = pd.read_csv('Data files/research.csv', delimiter = ",", low_memory=False)

    RT_testdata = RT_testdata.loc[RT_testdata['Patient Code'].str.startswith(('rt', 'RT'))==True]
    RT_testdata = RT_testdata[~RT_testdata['Patient Code'].str.contains("test|TEST|emily")]

    RT_testdata.rename(columns={'Patient Code': 'code'}, inplace=True)
    RT_testdata['code'] = RT_testdata['code'].str.upper()
        
    return RT_testdata

RT_testdata = rt_import()

def form_combiner():
    # Importing form answer questions for our three studies

    form_answers_CTMT = click_tmt_form_import()
    form_answers_RS = rs_import()[1]
    form_anwers_VSNS = VS_NS_import()[1]
    RT_form_data = rt_form_import()
    # Combining them and removing empty rows
    form_answers_combined = form_answers_CTMT.append([form_answers_RS,
                                                      form_anwers_VSNS, RT_form_data])
    form_answers_combined = form_answers_combined[form_answers_combined['code'].str.len() > 0]
    form_answers_combined['include'] = form_answers_combined['include'].str.lower()
    
    return form_answers_combined

#Loading new test export
new_tests = pd.read_csv('Data files/new_tests.csv', delimiter = ";")

#Removing 'TEST' occassions
new_tests = new_tests[~new_tests['pseudonym'].str.contains("TEST|test")]


#Comments from the testapplication

## This file was corrupt at download. CSV had many columns and some rows were duplicated
## Data was prepared beforehand by:
    ### 1. Creating a seperate column to the left
    ### 2. Combining the following columns using & symbol
    ### 3. Copy pasting result as 'values'
    ### 4. Deleting remaining columns
    ### 5. Read data as CSV

comments_input = pd.read_csv('Data files/comments_inp_method_20220124.csv', delimiter = ';')

## Preparing 'Date' column to be able to combine since all files do not contain
## test occassion
comments_input['Date'] = comments_input.Date.str[:24]

## Extracting input method from longer substring for analysis
comments_input["input_method"] = comments_input["device_info"] \
    .str.extract("(mouse|trackpad|touchscreen)")[0]

# Now we have X different files. However they are all in different sizes as
# we can see. We have to be careful so no test results are lost.

# print("Formanswers contains "+str(len(formanswers.index))+" observations.")
# print("Research export contains "+str(len(res_data.index))+" observations.")
# print("New tests contains "+str(len(new_tests.index))+" observations.")
# print("Comments and input method contains "+str(len(comments_input.index))+" observations.")
# print("Old RT contains "+str(len(RT_data.index))+" observations.")


#We'll merge the CTMT file with the comments extraction

merged2 = merged1.merge(comments_input, on='Date', how='left')

## Dropping some unneccessary columns

merged2.drop(['pseudonym', 'Comment', 'App_rating'], axis=1, inplace=True)

# Merging with the new tests export

merged3 = merged2.merge(new_tests, left_on = 'Test occasion',
                        right_on = 'testOccasionId', how='left')

#Finally merging with the old tests
# merged4 = merged3.append(RT_data)
# merged4 = merged4.append(rs_merge)
# merged4 = merged4.append(ns_merge)


#Some participants did the test more than once. We need to classify which testoccasion
#the participant did. The function below will do just that

# merged4.sort_values(by=['code', 'testOccasionId'], inplace=True)



# merged5 = what_test_occassion(merged4)

# Finally let's do some cleaning of the big file

# list_of_columns = merged5.columns


# merged5.drop(columns = ['pseudonym', 'Result_combined', 'Personnummer', 'TestReminder', 'ConsentForm',
#                         'SentResult', 'Sent_email'], inplace=True)

# merged5['code'].replace("", float("NaN"), inplace=True)

# merged5.dropna(subset = ["code"], inplace=True)
#Let's export this file 
# 
# merged5.to_csv('Data files/Created files/long_format_export.csv')

# to_wobbie = what_test_occassion(merged3)

# to_wobbie.to_csv('Data files/Created files/to_wobbie.csv', sep=";")

# wide_format.to_csv('Data files/Created files/wide_format_export.csv')



