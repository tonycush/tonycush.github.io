import requests
import pandas as pd
from bs4 import BeautifulSoup
import copy
import json
import time

class HTMLTableParser:
    
    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        bs_div = soup.find(attrs={"id": ["balancesheet", "p_balance_sheet"]})
        any_tags = str(type(bs_div))
        if 'NoneType' in any_tags:
            return False            
        else:
            return [(bs_div['id'],self.parse_html_table(table))\
                    for table in bs_div.find_all("table")]

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            #problem with some accs having different tags in their rows
            in_row_tags = row.findChildren(recursive = False)
            if len(in_row_tags)> 1:
                dif_tags_check = []
                for x in in_row_tags:
                    dif_tags_check.append(x.name)
                if (len(set(dif_tags_check))) >1:  
                    #Will need to rename the first tag (usually given th tag)
                    if 'th' in dif_tags_check and 'td' in dif_tags_check:
                        update = row.find('th')
                        update.name = 'td'

            # Determine the number of rows in the table
            td_tags = row.find_all('td')

            #issue with <tr> title rows - need to add cells to pad out table
            for w in td_tags:
                if len(td_tags) <len(column_names) :
                    if "class" in w.attrs:
                        if 'blank-line'or 'title' in w.attrs['class']:
                            if 'title'in w.attrs['class']:
                                current_cols = int(w.attrs['colspan'])
                            else:
                                current_cols = 1
                            cells_to_add =  len(column_names) - current_cols
                            new_cell = copy.copy(w)
                            del new_cell.attrs
                            new_cell.contents = ""
                            for i in range(cells_to_add):
                                td_tags.append(new_cell)
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
                    
            # Handle column names if we find them
            th_tags = row.find_all('th')
            ## Issues with multi row column heads - need to insert cells to pad out table            
            for x in th_tags:
                if "colspan" in x.attrs:
                    how_many_cols = int(x.attrs['colspan'])
                    del x.attrs['colspan']           
                    temp = copy.copy(x)
                    for i in range(how_many_cols-1):
                        th_tags.insert(th_tags.index(x),temp)                        
            
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    ##changing names
                    if th.get_text() not in column_names:
                        column_names.append(th.get_text())
                    else:
                        new_name = th.get_text()+"+"
                        column_names.append(new_name)                
                if column_names[0] == '':
                    column_names[0] = "Title"

        # Safeguard on Column Titles        
        if len(column_names) > 0 and len(column_names) != n_columns:
            print(len(column_names))
            raise Exception("Column titles do not match the number of columns")
        
        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                            index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        
        return df

# reading in the updated crunchbase file to get company numbers
unparsable = []
order = 1
accs_parsed = 0
accs_not_parsed = 0
no_ixbrl_acc = 0
with open('my_files/crunchbase_info_tidy.json') as json_file:
    data = json.load(json_file)

    for x in data:
        print("\n*** CB. " +str(order)+" " + x['name']+" ***  CH."+ x['company_house_name']+" *** \n")
        #print(x)
        if 'ixbrl_info' in x:        
            for this_link in x['ixbrl_info']:                
                time.sleep(3)
                print("\n" + this_link['accs_type'] + " --- "+this_link['accs_made_up_to']+" *** \n")
                #print(this_link['ixbrl_acc_link'])
                url = this_link['ixbrl_acc_link']
                hp = HTMLTableParser()

                parsed_url = hp.parse_url(url)
                if parsed_url == False:
                    print("!!! UNPARSABLE TABLE !!! For now...")
                    unparsable.append(url)
                    this_link['accs_table'] = "Not parsed"
                    accs_not_parsed +=1
                else:
                    table= parsed_url[0][1]  # Grabbing the table from the tuple         
                    table_headers = (table.columns)
                    for header in table_headers:
                        table[header] = table[header].replace('[\n,]','',regex = True)
                    print(table)
                    jtable = table.to_json(orient='table')
                    this_link['accs_table'] = json.loads(jtable)
                    accs_parsed += 1           
            #print(type(this_link['accs_table']))    
        else:
            print("!!!! NO iXBRL Details !!!!")
            no_ixbrl_acc +=1
        order +=1   

print("The End!!")
print ("Total iXBRL accounts parsed   : "+str(accs_parsed))
print ("Total iXBRL accounts unparsed : "+str(accs_not_parsed))
print ("No iXBRL accounts available   : "+str(no_ixbrl_acc))


unparsableLinkFile = open("my_files/unparse_ixbrl_links.csv", "w")

for info in unparsable:
    for link in info:
        unparsableLinkFile.write(link)
    unparsableLinkFile.write("\n")
unparsableLinkFile.close()

with open('my_files/crunchbase_info_tidy.json','w') as outfile:
    json.dump(data,outfile)
