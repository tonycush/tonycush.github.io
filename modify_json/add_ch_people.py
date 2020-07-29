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
for x in data[0:3]:
    businesses.append(x["company_number"])

order = 1
for business in businesses:
    business_ixbrl = []
    time.sleep(1)
    print("\n\t***\n")
    filehistory = "https://beta.companieshouse.gov.uk/company/" + business + "/officers"
    
    webpage = requests.get(filehistory, "html.parser")
    soup = BeautifulSoup(webpage.content, features="lxml")

    company_name = soup.find(attrs={"class": "heading-xlarge"})
    company_name = company_name.get_text()
    company_number = soup.find(attrs={"id": "company-number"})
    company_number = company_number.strong.get_text()
    
    print(str(order) + " : " + company_name)

    company_appointments = soup.find(attrs = {"id":"company-appointments"})
    company_appointments = company_appointments.get_text().replace(" ","").replace("\n"," ").strip()
    company_appointments_split = company_appointments.split("/")
    total_officers = int(company_appointments_split[0].split(" ")[0])
    total_resignations = int(company_appointments_split[1].split(" ")[0])

    print("** NOW THE APPOINTMENTS **")
    company_appointments_list = soup.find(attrs = {"class":"appointments-list"})
    
    print(type(company_appointments_list)) 
    appointments = company_appointments_list.children
    print(type(appointments)) 
    #print(appointments.attrs) 
    print(len(list(appointments)))
    for app in appointments:
        print(app)

    order += 1

    

"""
with open('my_files/crunchbase_info_tidy.json','w') as outfile:
    json.dump(data,outfile)
"""