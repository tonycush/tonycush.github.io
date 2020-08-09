import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import lxml
import json
import time
import re

def tidy_cell(cell):
    cell = cell.text.strip()
    if "   " in cell:
        cell = re.sub(('\s\s+'),' ',cell)
        cell = cell.replace('\n',' ')
    cell = cell.replace('\\','-')
    return cell

# reading in the updated crunchbase file to get company numbers
with open('my_files/crunchbase_info_tidy.json') as json_file:
    data = json.load(json_file)

businesses = []
for x in data:
    businesses.append(x["company_number"])

order = 1
for business in businesses:
    business_filing = []
    time.sleep(1)
    print("\n\t***\n")
    filehistory = "https://beta.companieshouse.gov.uk/company/" + business + "/filing-history"
    
    webpage = requests.get(filehistory, "html.parser")
    soup = BeautifulSoup(webpage.content, features="lxml")

    company_name = soup.find(attrs={"class": "heading-xlarge"})
    company_name = company_name.get_text()
    company_number = soup.find(attrs={"id": "company-number"})
    company_number = company_number.strong.get_text()

    print(str(order) + " : " + company_name)
    order += 1

    how_many_pages = soup.find(attrs={"class": "pager"})
    if how_many_pages != None:
        pages = -1
        for tag in how_many_pages:
            if tag.name == "li":
                pages += 1
    else:
        pages = 1

    for i in range(1, (pages + 1)):
        filehistory = (
            "https://beta.companieshouse.gov.uk/company/"
            + business
            + "/filing-history?page="
            + str(i)
        )
        webpage = requests.get(filehistory, "html.parser")
        soup = BeautifulSoup(webpage.content, features="lxml")
        ch_table = soup.find(attrs={"id": "fhTable"})
        any_rows = ch_table.find_all("tr")
        for row_i in any_rows:
            any_cells = (row_i.find_all("td"))   
            if len(any_cells)>0:     
                filing_date = tidy_cell(any_cells[0])
                filing_type = tidy_cell(any_cells[1])
                filing_desc = tidy_cell(any_cells[2])
                made_to = ""
                if "made up to" in filing_desc:
                    temp_cell = filing_desc.split(" made up to ")
                    filing_desc = temp_cell[0]
                    made_to = temp_cell[1]
                filing_details = '{"date_filed":"'+filing_date+'","doc_code":"'+filing_type+'","filing_desc":"'+filing_desc+'","made_up_to":"'+made_to+'"}'
                #print(filing_details[100:])
                business_filing.append(json.loads(filing_details))
    
    bus_index = (businesses.index(business))
    if data[bus_index]['company_number'] ==business:
        data[bus_index]['filing_history'] = business_filing

with open('my_files/crunchbase_info_tidy.json','w') as outfile:
    json.dump(data,outfile)
