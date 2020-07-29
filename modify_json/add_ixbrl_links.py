import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import lxml
import json
import time

def check_ixbrl(x):
    if "iXBRL" in x:
        return "Yes"
    else:
        return "No"

# reading in the updated crunchbase file to get company numbers
with open('my_files/crunchbase_info_tidy.json') as json_file:
    data = json.load(json_file)

businesses = []
for x in data:
    businesses.append(x["company_number"])

order = 1
for business in businesses:
    bus_ixbrl = "["
    time.sleep(1)
    print("\n\t***\n")
    filehistory = (
        "https://beta.companieshouse.gov.uk/company/" + business + "/filing-history"
    )

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
        any_links = ch_table.find_all("a")
        for link in any_links:
            if "iXBRL" in link.get_text():
                ixbrl_acc_link = "https://beta.companieshouse.gov.uk" + link.get("href")

                acc_desc = (link.parent.parent.previous_sibling.previous_sibling)
                split_acc_desc = acc_desc.text.strip().split(' made up to ')
                acc_json = "{'accs_type' :'"+split_acc_desc[0] +"', 'accs_made_up_to':'"+split_acc_desc[1] +"','ixbrl_acc_link':'"+ ixbrl_acc_link+"'},"
                bus_ixbrl+=acc_json
    
    if bus_ixbrl[-1] == ',':
        bus_ixbrl= bus_ixbrl[:-1]    
    bus_ixbrl+=']'
    
    bus_index = (businesses.index(business))
    if data[bus_index]['company_number'] ==business:
        data[bus_index]['ixbrl_info'] = bus_ixbrl

with open('my_files/crunchbase_info_tidy.json','w') as outfile:
    json.dump(data,outfile)