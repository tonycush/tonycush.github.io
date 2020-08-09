import pandas as pd
from pandas import DataFrame
import json
import numpy as np
import re
"""
FEATURES : 
    TO FIND : 
        STRINGS     : 
        INTS        : 
        DATES       : 
        ARRAYS      : INVESTORS, INVESTMENTS, FUNDING, 
        FUNCTIONS   : GROWTH

    FOUND : 
        STRINGS     : STATUS, COMPANY TYPE , NAMES, IPO STATUS, ACCOUNTS OVERDUE, IND SICs
        INTS        : OFFICERS, RESIGNATIONS
        DATES       : INCORPORATED, DISSOLVED, FOUNDED,YEAR END, FILING DATES
        ARRAYS      : PREV_NAMES,INDUSTRIES, ACCOUNT TYPES, ACCOUNTS
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

def add_col_to_df(df,new_cols,prefix):
    for col in new_cols:
        new_col = prefix+col
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
        df_features[new_col] =new_col_series

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

def rename_accs_table_cols(titles):
    new_titles = list(titles[0:2])
    new_titles.append('notes')
    table_width = len(titles)
    if table_width == 4:
        new_titles.append('current_r')
    elif table_width == 7:
        new_titles.extend(['current_l','current_r','previous_l','previous_r'])
    elif table_width ==5:
        last_col = titles[4]
        if last_col[-1:] =='+':
            new_titles.extend(['current_l','current_r'])
        else:            
            new_titles.extend(['current_r','previous_r'])
    return new_titles

def rename_duplicate_headers(headers):
    distinct_headers = set(headers)
    if len(headers) != len(distinct_headers):
        new_headers = []
        for header in headers:
            if header not in new_headers:
                new_headers.append(header)
            else:
                new_header = header+"+"
                new_headers.append(new_header)
        headers = new_headers
    return(headers)

def combine_same_year_cols(df):
    for i in df.columns:
        df[i][df[i].apply(lambda i: True if re.search('^\s*$', str(i)) else False)]=None
    how_many_cols = len(df.columns)
    if how_many_cols== 7:
        cy_r = df['current_r']
        cy_l = df['current_l']
        df['current_r'] = df['current_r'].fillna(df['current_l'])
        df['previous_r'] = df['previous_r'].fillna(df['previous_l'])
        df=df.drop(columns=['current_l','previous_l'])
    elif how_many_cols ==5 and 'current_l'in df.columns:        
        df['current_r'] = df['current_r'].fillna(df['current_l'])
        df=df.drop(columns=['current_l'])
    return df

print("\n** ** ** ** ** ** ** ** ** ** ** **")
# reading in the updated company file
with open('my_files/crunchbase_info_tidy.json') as json_file:
    data = json.load(json_file)

df = pd.json_normalize(data)
FIELDS = ["index","name","ni_company_house_match","company_number","company_house_name","company_house_overview.previous_company_names","company_house_overview.Company type","company_house_overview.Company status","company_house_overview.Incorporated on","company_house_people.num_officers","company_house_people.num_resignation","company_house_overview.SIC","company_house_overview.Accounts overdue","company_house_overview.Dissolved on"]
#,"company_house_overview.Dissolved on"

df_features = df[FIELDS]
df_features.rename(columns = {
    "company_house_overview.previous_company_names":"ch_prev_names",
    "company_house_overview.Company type":"ch_type",
    "company_house_overview.Company status":"ch_status",
    "company_house_overview.Incorporated on":"ch_incorporation_date",
    "company_house_overview.Dissolved on":"ch_dissolve_date",
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
investors_df = pd.DataFrame()
funding_round_df = pd.DataFrame()
filed_accs_df = pd.DataFrame()
investor_list = []
funding_type_list = []
for company in data:
    #print("\n****   "+ company['name'] + "   *******\n")
    cb_sections = company['sections']
    for cb_section in cb_sections:
        if cb_section['name'] == "Overview": 
            overview_df = normalize_section(cb_section['data'],company['index'],overview_df) 
        elif cb_section['name'] == "Funding Rounds":            
            funding_df = normalize_section(cb_section['fields'],company['index'],funding_df)
        elif cb_section['name']=="Investors":  
            investment_df = normalize_section(cb_section['fields'],company['index'],investment_df)    

              
            investor_table = section_sub_table(cb_section['table'])
            inv_list = list(set(list(investor_table['Investor Name'])))
            inv_list = ['invr_'+inv for inv in inv_list]    
            inv_flag = [1 for inv in inv_list]    
            temp_investor_df = pd.DataFrame(data=inv_flag)
            temp_investor_df = temp_investor_df.transpose()
            temp_investor_df.columns=inv_list
            temp_investor_df['index'] = company['index']
            investors_df = pd.concat([investors_df,temp_investor_df])

            temp_funding_round_list = list(investor_table['Funding Round'])
            funding_round_list= []
            for funding in temp_funding_round_list:
                fund_round = funding.split(" - ")[0].strip()
                if fund_round not in funding_round_list:
                    funding_round_list.append(fund_round)
            funding_round_list = ['fr_'+fr for fr in funding_round_list]    
            funding_round_flag = [1 for fr in funding_round_list]   
            temp_funding_round_df = pd.DataFrame(data=funding_round_flag)
            temp_funding_round_df = temp_funding_round_df.transpose()
            temp_funding_round_df.columns=funding_round_list
            temp_funding_round_df['index'] = company['index']
            funding_round_df = pd.concat([funding_round_df,temp_funding_round_df])
            
    ###setting up the filed accounts df
    if 'filing_history' in company:
        all_filing_history = pd.json_normalize(company['filing_history'])
        accs_filed = all_filing_history[(all_filing_history.doc_code=="AA")]    
        accs_filed = accs_filed.drop(columns = 'doc_code')
        accs_filed = accs_filed.iloc[::-1].reset_index(drop=True)
        
        ixbrl_df = pd.json_normalize(company['ixbrl_info'])
        if not(ixbrl_df.empty):        
            accs_filed = pd.merge(accs_filed,ixbrl_df,how='outer',left_on='date_filed',right_on='accs_date_filed')  
            if 'accs_table.data' in accs_filed:
                accs_filed = accs_filed[['date_filed','filing_desc','made_up_to','accs_table.data']]
            else:
                accs_filed = accs_filed[['date_filed','filing_desc','made_up_to','accs_table']]
                
            #accs_filed.rename(columns = {'accs_table.data':'table_data'},inplace=True)
        accs_filed = accs_filed.transpose()
        accs_filed = accs_filed.unstack().to_frame().sort_index(level=1).T
        accs_filed[(0,'acc_index')] = company['index']
        filed_accs_df = pd.concat([filed_accs_df,accs_filed])

new_cols=[]
for col in filed_accs_df.columns:
    new_name = "y"+str(col[0])+"_"+col[1]
    new_cols.append(new_name)
filed_accs_df.columns = new_cols

section_df = pd.merge(overview_df,funding_df, how='outer',left_on='index', right_on='index')
section_df = pd.merge(section_df,investment_df, how='outer',left_on='index', right_on='index')

print("\n^^^^ ^^ ^^^^ ^^ ^^^^ ^^ ^^^^\n")

overview_df = section_df.reset_index(drop=True)
SUBFIELDS = ["Also Known As ","Company Type ","Industries ","Founded Date ","Founders ","IPO Status ", "Number of Funding Rounds ","Total Funding Amount ","Number of Investors ","index"]
df_subfeatures = overview_df[SUBFIELDS]

df_features = pd.merge(df_features,df_subfeatures, how='outer',left_on='index', right_on='index')
df_features = pd.merge(df_features,investors_df, how='outer',left_on='index', right_on='index')
df_features = pd.merge(df_features,funding_round_df, how='outer',left_on='index', right_on='index')
df_features = pd.merge(df_features,filed_accs_df, how='outer',left_on='index', right_on='y0_acc_index')

##FIND ALL COLUMNS IN DF THAT HAVE 'accs_table.data' IN THEIR NAME
acc_table_cols =[]
for col in df_features.columns:
    if re.search("accs_table.data",col):
        acc_table_cols.append(col)


#FOR EACH OF THOSE COLUMNS RETRIEVE THE ACCOUNTS TABLE DATA
all_company_accs_df = pd.DataFrame()
for company in data:
    comp_index = company['index']
    comp_name = company['name']
    this_comp_index = data.index(company)
    print(" ><><>< "+str(comp_index) +" ><><><><   "+comp_name+"   ><><><><")
    this_company_accs_df  = pd.DataFrame(data=[comp_index],columns=['comp_index'])  
    for acc_col in acc_table_cols:
        #print(">>>>>>>>>>>>>>>>>>>>>>>>")
        this_year = acc_col.split("_")[0]
        acc_col_list = list(df_features[acc_col])
        ##JUST RETURN THE VALUE IN THE SERIES
        acc_table = (acc_col_list[this_comp_index])
        if isinstance(acc_table,list):
            acc_layout = pd.json_normalize(acc_table)
            current_titles = acc_layout.columns
            acc_layout.columns = rename_accs_table_cols(current_titles) 
            acc_layout = combine_same_year_cols(acc_layout)
            acc_layout = acc_layout.drop(columns=['index','notes']).dropna(axis=0).reset_index(drop=True)
            acc_layout['Title'] = acc_layout['Title'].str.upper()

            ##LETS TRANSPOSE & UNSTACK
            acc_headers = list(acc_layout['Title'])
            acc_headers = [this_year+"_"+header for header in acc_headers]
            #CHECK FOR DUPLIACTE HEADERS
            acc_headers = rename_duplicate_headers(acc_headers)
            acc_values = (acc_layout['current_r'])
            acc_table_df = acc_values.to_frame().T
            
            acc_table_df.columns = acc_headers
            acc_table_df['comp_index'] = company['index']
            this_company_accs_df = pd.merge(this_company_accs_df,acc_table_df, how='outer',left_on='comp_index', right_on='comp_index')
        #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        
    #print(this_company_accs_df)
    #print(all_company_accs_df.info())
    all_company_accs_df = pd.concat([all_company_accs_df,this_company_accs_df])
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#reorder all accs_table columns
all_company_accs_df = all_company_accs_df.reindex(sorted(all_company_accs_df.columns), axis=1)
##print(all_company_accs_df.info())
df_features = pd.merge(df_features,all_company_accs_df,how='outer',left_on='index', right_on='comp_index')
#Get a list of column names, check if there is a value, insert result beside column
feature_columns = df_features.columns
for (col_index,feature) in enumerate(feature_columns):
    placing = (col_index*2)+1
    new_col = "present_"+feature
    df_features.insert(placing,new_col,df_features[feature].notnull())

#create sorted list of all SICs
#create a list of all values - then add those values as column names
#adding a prefix to make the df columns easier to search
to_seperate = [('ch_sic','sic_'),('Industries ','ind_')]
for sep in to_seperate:
    col = sep[0]
    prefix = sep[1]
    new_col_list = retrieve_series_values(df_features[col])
    add_col_to_df(df_features[col],new_col_list,prefix)
    df_features = df_features.drop(columns=[col])


##cols to drop
drop_cols = ['present_index','present_comp_index','present_name','present_ni_company_house_match','present_company_house_name','present_ch_sic']
for drop_col in drop_cols:
    df_features=df_features.drop(columns=[drop_col])

df_features.to_excel(r'my_files/features.xlsx',index = False)

