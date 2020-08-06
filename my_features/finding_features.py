import pandas as pd
from pandas import DataFrame
import json
import numpy as np
"""
FEATURES : 
    TO FIND : 
        STRINGS     : 
        INTS        : 
        DATES       : YEAR END
        ARRAYS      : INVESTORS, INVESTMENTS, FUNDING, ACCOUNT TYPES
        FUNCTIONS   : GROWTH

    FOUND : 
        STRINGS     : STATUS, COMPANY TYPE , NAMES, IPO STATUS, ACCOUNTS OVERDUE, IND SICs
        INTS        : OFFICERS, RESIGNATIONS
        DATES       : INCORPORATED, DISSOLVED, FOUNDED
        ARRAYS      : PREV_NAMES,INDUSTRIES, 
        FUNCTIONS   :
"""

def retrieve_series_values(series):
    temp_list = []
    for temp_array in series:        
        if isinstance(temp_array, list):
            for this_value in temp_array:
                if isinstance(this_value, dict):
                    for key in this_value.keys():
                        temp_list.append(key) 
                else:
                    temp_list.append(this_value.strip())
    temp_list = list(set(temp_list))
    temp_list.sort()
    return temp_list

def add_col_to_df(df,new_cols):
    for col in new_cols:
        new_col_series = []
        for df_array in df:
            flag = 0
            if isinstance(df_array, list):
                for df_entry in df_array:
                    if isinstance(df_entry, dict):
                        if col in df_entry.keys(): 
                            flag = 1
                            break
                    else:
                        if df_entry.strip()==col:
                            flag = 1
                            break
            new_col_series.append(flag)
        df_features[col] =new_col_series  
    #df_features= df_features.drop(columns=['ch_sic'])

def normalize_section(s,num,df):
    temp_df = pd.json_normalize(s)
    temp_df = pd.DataFrame(np.diag(temp_df),index=[temp_df.columns][0]).transpose()
    temp_df['index'] = num
    df = pd.concat([df,temp_df])
    return df

def section_sub_table(table):
    df_temp_table = pd.DataFrame()
    temp_rows = table[0]['rows']
    for temp_row in temp_rows:
        df_temp_table= df_temp_table.append(temp_row)
    df_temp_table.reset_index(drop=True, inplace=True)    
    temp_columns = table[0]['columnNames']
    for old_col in df_temp_table.columns:
        new_col = temp_columns[old_col]
        df_temp_table.rename(columns={old_col:new_col},  inplace=True)
    return df_temp_table

print("\n** ** ** ** ** ** ** ** ** ** ** **")
# reading in the updated company file
with open('my_files/crunchbase_info_tidy_sample.json') as json_file:
    data = json.load(json_file)

df = pd.json_normalize(data)
#print(df.info())

FIELDS = ["index","name","company_number","company_house_name","company_house_overview.previous_company_names","company_house_overview.Company type","company_house_overview.Company status","company_house_overview.Incorporated on","company_house_people.num_officers","company_house_people.num_resignation","company_house_overview.SIC","company_house_overview.Accounts overdue"]
#,"company_house_overview.Dissolved on"
#FIELDS = ["index","name","company_house_overview.SIC"]

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

#LOAD THE SUBSET OF DATA INTO DATAFRAME
#subsets required from crunchbase data['Overview','Investors'{table},'Funding Rounds'{table}] ]
overview_df = pd.DataFrame()
funding_df = pd.DataFrame()
investment_df = pd.DataFrame()
investor_list = []
funding_type_list = []
for company in data[0:3]:
    #this_index= data.index(company)
    #print(this_index)
    #company_section_df =pd.DataFrame()
    #print("\n****   "+ company['name'] + "   *******\n")
    cb_sections = company['sections']
    for cb_section in cb_sections:
        #print(cb_section['name'])
        if cb_section['name'] == "Overview": 
            overview_df = normalize_section(cb_section['data'],company['index'],overview_df) 
        elif cb_section['name'] == "Funding Rounds":            
            funding_df = normalize_section(cb_section['fields'],company['index'],funding_df)
        elif cb_section['name']=="Investors":  
            investment_df = normalize_section(cb_section['fields'],company['index'],investment_df)      
            investor_table = section_sub_table(cb_section['table'])
            temp_investor_list = investor_table['Investor Name']
            temp_funding_list = investor_table['Funding Round']
            for investor in temp_investor_list:
                if investor not in investor_list:
                    investor_list.append(investor)
            for funding in temp_funding_list:
                fund_round = funding.split(" - ")[0].strip()
                if fund_round not in funding_type_list:
                    funding_type_list.append(fund_round)

    print("-----------------\n")
investor_list.sort()
print(investor_list)
funding_type_list.sort()
print(funding_type_list)

#print(overview_df.info())
section_df = pd.merge(overview_df,funding_df, how='outer',left_on='index', right_on='index')
section_df = pd.merge(section_df,investment_df, how='outer',left_on='index', right_on='index')
#print(section_df.head())
#print(section_df.info())


print("\n^^^^ ^^ ^^^^ ^^ ^^^^ ^^ ^^^^\n")
overview_df = section_df.reset_index(drop=True)
SUBFIELDS = ["Also Known As ","Company Type ","Industries ","Founded Date ","Founders ","IPO Status ", "Number of Funding Rounds ","Total Funding Amount ","Number of Investors ","index"]
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

#create sorted list of all SICs
##create a list of all values - then add those values as column names

"""
to_seperate = ['ch_sic','Industries ']
for sep in to_seperate:
    new_col_list = retrieve_series_values(df_features[sep])
    add_col_to_df(df_features[sep],new_col_list)
    df_features = df_features.drop(columns=[sep])
"""
#print(df_features.info())
#print(df_features.head())
#df_features.to_excel(r'my_files/features.xlsx',index = False)

df_features.to_excel(r'my_files/building_feats_sample.xlsx')
