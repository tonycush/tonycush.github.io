import pandas as pd
from pandas import DataFrame
import json
import numpy as np
"""
INDUSTRIES
FEATURES TO FIND : 
    STRINGS     : 
    INTS        : 
    DATES       : YEAR END
    ARRAYS      : INVESTORS, INVESTMENTS, FUNDING, ACCOUNT TYPES
    FUNCTIONS   : GROWTH

FEATURES FOUND : 
    STRINGS     : STATUS, COMPANY TYPE , NAMES, IPO STATUS, ACCOUNTS OVERDUE
    INTS        : OFFICERS, RESIGNATIONS
    DATES       : INCORPORATED, DISSOLVED, FOUNDED
    ARRAYS      : PREV_NAMES,SICs,INDUSTRIES, FOUNDERS
    FUNCTIONS   :

"""
print("\n** ** ** ** ** ** ** ** ** ** ** **")

# reading in the updated company file
with open('my_files/crunchbase_info_tidy.json') as json_file:
    data = json.load(json_file)

df = pd.json_normalize(data)

#print(df.info())
FIELDS = ["index","name","company_number","company_house_name","company_house_overview.previous_company_names","company_house_overview.Company type","company_house_overview.Company status","company_house_overview.Incorporated on","company_house_people.num_officers","company_house_people.num_resignation","company_house_overview.SIC","company_house_overview.Accounts overdue"]
#,"company_house_overview.Dissolved on"
#

df_features = df[FIELDS]
df_features.rename(columns = {
    "company_house_overview.previous_company_names":"ch_prev_names",
    "company_house_overview.Company type":"ch_type",
    "company_house_overview.Company status":"ch_status",
    "company_house_overview.Incorporated on":"ch_incorporation_date",
    #"company_house_overview.Dissolved on":"ch_dissolve_date",
    "company_house_people.num_officers":"ch_tot_officers",
    "company_house_people.num_resignation":"ch_tot_resignations",
    "company_house_overview.SIC":"ch_sic",
    "company_house_overview.Accounts overdue":"ch_overdue",
    #"":"",
    },inplace = True)
#print(df_features)
#print(df_features.info())

#LOAD THE SUBSET OF DATA INTO DATAFRAME
#subsets required from crunchbase data['Overview','Investors'{table},'Funding Rounds'{table}] ]
overview_df = pd.DataFrame()
for company in data:
    #print("\n****   "+ company['name'] + "   *******\n")
    cb_sections = company['sections']
    for cb_section in cb_sections:
        #print(cb_section['name'])
        if cb_section['name'] == "Overview":          
            #print(cb_section['data'])
            temp_df = pd.json_normalize(cb_section['data'])
            temp_df = pd.DataFrame(np.diag(temp_df),index=[temp_df.columns][0]).transpose()
            temp_df['index'] = company['index']
            overview_df = pd.concat([overview_df,temp_df])
        """
        elif cb_section['name'] in ["Funding Rounds","Investors"]:
            print((cb_section['name']))
            #print((cb_section['table'][0]))
            temp_columns = cb_section['table'][0]['columnNames']
            df_temp_table = pd.DataFrame()
            temp_rows = cb_section['table'][0]['rows']
            for temp_row in temp_rows:
                df_temp_table= df_temp_table.append(temp_row)
            df_temp_table.reset_index(drop=True, inplace=True)
            for old_col in df_temp_table.columns:
                new_col = temp_columns[old_col]
                df_temp_table.rename(columns={old_col:new_col},  inplace=True)
            print(df_temp_table)        
        """
    #print("-----------------")

print("\n^^^^ ^^ ^^^^ ^^ ^^^^ ^^ ^^^^\n")

overview_df = overview_df.reset_index(drop=True)
SUBFIELDS = ["Also Known As ","Company Type ","Industries ","Founded Date ","Founders ","IPO Status ","index"]
df_subfeatures = overview_df[SUBFIELDS]
#print(df_subfeatures.info())

df_features = pd.merge(df_features,df_subfeatures, how='outer',left_on='index', right_on='index')
#print(df_features.info())
#print(df_features.head())

#Get a list of column names, check if there is a value, insert result beside column
feature_columns = df_features.columns
for (col_index,feature) in enumerate(feature_columns):
    placing = (col_index*2)+1
    new_col = "present_"+feature
    df_features.insert(placing,new_col,df_features[feature].notnull())

#print(df_features.info())
#print(df_features.head())
df_features.to_excel(r'my_files/features.xlsx',index = False)


#df_merged.to_excel(r'my_files/building_feats_subs.xlsx')
