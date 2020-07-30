import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import lxml
import json
import time
import re

# reading in the updated crunchbase file to get company numbers
with open('my_files/crunchbase_info_tidy.json') as json_file:
    data = json.load(json_file)

businesses = []
for x in data:
    businesses.append(x["company_number"])

order = 1
for business in businesses:
    
    time.sleep(1)
    print("\n\t***\n")
    filehistory = "https://beta.companieshouse.gov.uk/company/" + business
    
    webpage = requests.get(filehistory, "html.parser")
    soup = BeautifulSoup(webpage.content, features="lxml")

    company_name = soup.find(attrs={"class": "heading-xlarge"})
    company_name = company_name.get_text()
    company_number = soup.find(attrs={"id": "company-number"})
    company_number = company_number.strong.get_text()    
    print(str(order) + " : " + company_name)

    ch_overview = soup.find(attrs = {"id":"content-container"})
    reg_address_info = ch_overview.find('dl').findChildren(recursive = False)
    reg_address = reg_address_info[1].text.strip()
    ch_overview_str = '{"registered_address":"'+reg_address+'",'

    # RETREIVING GRID DETAILS
    ch_overview_grids = ch_overview.findAll(attrs = {"class":"grid-row"})
    for overview_grid in ch_overview_grids:
        ch_type_details = overview_grid.findAll('dl')
        for type in ch_type_details:
            type_key = type.find('dt').text
            type_value = type.find('dd').text.strip()
            if '     ' in type_value:
                type_value  = re.sub(('\s\s+'),' ', type_value)
                type_value = type_value.replace('\n',' ')
            ch_overview_str += '"'+type_key+'":"'+type_value+'",'
            
        ch_docs_details = overview_grid.findAll(attrs = {"class":"column-half"})
        for doc in ch_docs_details:
            doc_type = doc.h2.text
            ch_overview_str += '"'+doc_type+'":['
            doc_details = doc.findAll('p')
            for doc_detail in doc_details:
                this_line = doc_detail.text.strip()
                if "   " in this_line:
                    this_line = re.sub(('\s\s+'),' ',this_line)
                    this_line = this_line.replace('\n',' ')
                ch_overview_str+= '"'+this_line+'",'
            if ch_overview_str[-1] == "[":
                ch_overview_str += ']'
            else:
                ch_overview_str= ch_overview_str[:-1] + '],'

    # RETREIVING SIC DETAILS
    sic_list_info = ch_overview.find(attrs = {"id":"sic-title"}).nextSibling.nextSibling
    sic_list_items = []
    sic_list = sic_list_info.findAll('li')
    ch_overview_str += '"SIC":['
    for sic in sic_list:
        sic_split = sic.text.strip().split(" - ")
        sic_code = sic_split[0]
        sic_desc = sic_split[1] 
        ch_overview_str+= '{"'+sic_code+'":"'+sic_desc+'"},'
    if ch_overview_str[-1] == "[":
        ch_overview_str += ']'
    else:
        ch_overview_str= ch_overview_str[:-1] + ']'
    
    # RETREIVING PREV NAME DATA - if applicable
    prev_name_table = ch_overview.find(attrs = {"id":"previousNameTable"})
    if prev_name_table is not None:
        ch_overview_str += ', "previous_company_names" : ['
        pn_rows = (prev_name_table.findAll('tr'))
        for pn_row in pn_rows[1:]:
            pn_details = pn_row.findAll('td')
            prev_name = pn_details[0].text.strip()
            period = pn_details[1].text.split("-")
            period_start = period[0].strip()
            period_end = period[1].strip()
            ch_overview_str += '{"previous_name":"'+prev_name+'","period_start":"'+period_start+'","period_end":"'+period_end+'"},'
    ch_overview_str= ch_overview_str[:-1] + ']'
 
    ch_overview_str += '}'
    #print(ch_overview_str)

    # LOADING NEW DATA
    bus_index = (businesses.index(business))
    if data[bus_index]['company_number'] ==business:
        data[bus_index]['company_house_overview']= json.loads(ch_overview_str)        
    order += 1  

with open('my_files/crunchbase_info_tidy.json','w') as outfile:
    json.dump(data,outfile)

