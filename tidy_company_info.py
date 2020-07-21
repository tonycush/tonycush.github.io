import json
import re

with open('crunchbase_info_sample.json') as json_file:
    data = json.load(json_file)

for company in data:
    print("**** ****")
    print(company['name'])
    for company_section in company['sections']:
        #reformat section names
        orig_name = company_section['name']
        updated_name =(orig_name.replace("<!---->","")).strip()
        company_section['name'] = updated_name
        if len(company_section['data'])>0 :            
            #split industries & founders into arrays
            for i in company_section['data']:
                if "Industries " in i:
                    i["Industries "] = i["Industries "].split(',')
                
                if "Founders " in i:
                    i["Founders "] = i["Founders "].split(',')                    
       
        #update info in section tables
        if len(company_section['table'])>0:   
            #reformat column names         
            new_headers = []
            for col_head in company_section['table'][0]['columnNames']:
                new_headers.append(col_head.strip())
            company_section['table'][0]['columnNames'] = new_headers

            #Check for dates within tables, and reformat string
            a_date = re.search(".*Date.*",str(company_section['table'][0]['columnNames']))
            if a_date:
                #original dates in format MMM DD, YYYY 
                #not helpful for splitting string into an array
                for i in company_section['table'][0]['rows']:
                    i_res = re.search("\w{3} \d+, \d{4}",i[0])
                    temp_date = i_res.group()
                    new_date = temp_date.replace(",","")
                    new_i= re.sub("\w{3} \d+, \d{4}",new_date,i[0])
                    i[0] = new_i
                    #print(i)
            
            #split out each row in the table into an array
            #some rows have multiple entries under 'partners' & 'Lead Investors'
            # these details are to be placed in an array
            print()
            print("SORT OUT EACH ROW")
            print(company_section['table'][0]['columnNames'])
            table_len = len(company_section['table'][0]['columnNames'])

            split_index = (table_len-1)            
            table_name = company_section['name']
            print("This "+table_name+" table has : "+str(table_len) +" columns")
            
            print(table_name)
            for i in company_section['table'][0]['rows']:
                j = i[0].split(',')

                if len(j)< table_len:                    
                    j.insert(2," —")
                
                k = j[split_index:]
                start = j[:split_index]
                start.append(k)
                #print(j)
                #print(start)
                i[0] = start
                #print("This row has : "+str(len(j)) +" columns")

            
            print("Did that work")
            for i in company_section['table'][0]['rows']:
                i = i[0]
                print(len(i))
                print(i)

            
with open('crunchbase_info_sample2.json','w') as outfile:
    json.dump(data,outfile)
    
                