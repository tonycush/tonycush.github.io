import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import lxml
import json
import time

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

    company_officers = []
    company_appointments_list = soup.find(attrs = {"class":"appointments-list"})    
    appointments = company_appointments_list.findAll('div', recursive = False)
    for appointment in appointments:
        officer_details = appointment.findChildren(recursive = False)
        officer_info = '{'
        for o_detail in officer_details:
            if o_detail.has_attr("class"):
                if 'heading-medium' in o_detail.attrs['class']:
                    o_key = "Officer"
                    o_value = (o_detail.text.strip()) 
                    #print(o_value)
                    if "'" in o_value:
                        o_value = o_value.replace("'","\'")
                    o_linkage = o_detail.find("a").get("href")
                    o_link_value = "https://beta.companieshouse.gov.uk"+o_linkage

                    officer_info+= '"'+o_key+'":"'+o_value+'","Officer link":"'+o_link_value+'",' 
                else:
                    dls = o_detail.findAll('dl')
                    for dl in dls:
                        dtease = dl.findAll('dt')
                        for dt in dtease:
                            o_key = dt.text
                            if "Role" in o_key[:4]:
                                role_status = o_key[4:].strip()
                                o_key = 'Status":"'+role_status+'","'+o_key[:4]
                            o_value = dt.nextSibling.nextSibling.text.strip()
                            officer_info+= '"'+o_key+'":"'+o_value+'",'  

            else:
                dts = o_detail.findAll('dt')
                for dt in dts:
                    o_key = dt.text
                    o_value = dt.nextSibling.nextSibling.text.strip()
                    #print(o_value)
                    o_value = o_value.replace("'","\'")
                    if '"' in o_value:
                        o_value = o_value.replace('"','')
                        print(o_value)
                    officer_info+= '"'+o_key+'":"'+o_value+'",'  
            
        officer_info = officer_info[:-1]+"}"
        #print(officer_info[150:170])
        company_officers.append(json.loads(officer_info))

    company_house_people_string = '{"num_officers":"'+str(total_officers)+'","num_resignation":"'+str(total_resignations)+'","officers":""}'  
    ch_people_json = json.loads(company_house_people_string)
    bus_index = (businesses.index(business))
    if data[bus_index]['company_number'] ==business:
        data[bus_index]['company_house_people']= ch_people_json
        data[bus_index]['company_house_people']['officers'] = company_officers
    
    order += 1   


with open('my_files/crunchbase_info_tidy.json','w') as outfile:
    json.dump(data,outfile)
