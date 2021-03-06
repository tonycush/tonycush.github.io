import pandas as pd
from pandas import DataFrame
import json
import numpy as np
from tableschema import Table
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

#with open () as filing_history:
#    file_data = 
#LOAD THE SUBSET OF DATA INTO DATAFRAME
#subsets required from crunchbase data['Overview','Investors'{table},'Funding Rounds'{table}] ]
#overview_df = pd.DataFrame()
acc_titles=[]
acc_years=[]
for company in data:
    print("\n^^^ "+company['name']+" ^^^\n")
    #this_index= data.index(company)
    #print(this_index)
    if 'ixbrl_info' in company:
        df = pd.json_normalize(company['ixbrl_info'])
        print(df.info())
        if not df.empty:
            #print("WHAT HAVE WE GOT HERE")
            if 'accs_table.data' in df:
                all_schemas = df['accs_table.schema.fields']
                for schema in all_schemas:
                    if isinstance(schema,list):
                        how_many_cols = len(schema)
                        print(schema)
                        if how_many_cols == 4:
                            schema[3]['name'] = 'current_r'
                        elif how_many_cols == 7:
                            schema[3]['name'] ='current_l'
                            schema[4]['name'] ='current_r'
                            schema[5]['name'] ='previous_l'
                            schema[6]['name'] ='previous_r'
                        elif how_many_cols ==5:
                            last_col = schema[4]['name']
                            if last_col[-1:] =='+':
                                schema[3]['name'] ='current_l'
                                schema[4]['name'] ='current_r'
                            else:
                                schema[3]['name'] ='current_r'
                                schema[4]['name'] ='previous_r'
                        print(schema)
            
                
                print(">>>>>>>>>>>>>>>>\n")
                
                all_accs = df['accs_table.data']
                #print(all_accs)
                print(all_schemas)
                for acc in all_accs:
                    if isinstance(acc, list):
                        for entry in acc:
                            print(entry)
                            title = entry['Title']
                            #title = entry['Title'].upper().strip()
                            if title not in acc_titles:
                                acc_titles.append(title)
                    #print(">>>>>>>>>>>>>>>>\n")
                #print("-----------------\n")

acc_titles.sort()
#print(acc_titles)
#print(str(len(acc_titles))+" : TITLE types??\n\n")

acc_titles.sort()
#print(acc_years)

#acc_titles.clear()
search_titles = []
for title in acc_titles:
    if 'ORD' not in title:
        search_titles.append(title)
#print(search_titles)
#print(str(len(search_titles))+" : TITLE types??\n\n")


#print(section_df.head())
#print(section_df.info())



#Get a list of column names, check if there is a value, insert result beside column
#feature_columns = df_features.columns
#for (col_index,feature) in enumerate(feature_columns):
#    placing = (col_index*2)+1
#    new_col = "present_"+feature
#   df_features.insert(placing,new_col,df_features[feature].notnull())


#print(df_features.info())
#print(df_features.head())
#df_features.to_excel(r'my_files/accs_features.xlsx',index = False)

#df_features.to_excel(r'my_files/accs_building_feats_sample.xlsx')
