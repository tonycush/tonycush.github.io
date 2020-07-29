import requests
import pandas as pd
from bs4 import BeautifulSoup
import copy
import json

class HTMLTableParser:
    
    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        bs_div = soup.find(attrs={"id": ["balancesheet", "p_balance_sheet"]})
        return [(bs_div['id'],self.parse_html_table(table))\
                for table in bs_div.find_all("table")]  

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            # Determine the number of rows in the table
            td_tags = row.find_all('td')

            #issue with <tr> title rows - need to add cells to pad out table
            for w in td_tags:
                if len(td_tags) <len(column_names) :
                    if "class" in w.attrs:
                        if 'title' in w.attrs['class']:
                            current_cols = (w.attrs['colspan'])
                            cells_to_add =  len(column_names) - (int(current_cols))
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


        # Safeguard on Column Titles        
        if len(column_names) > 0 and len(column_names) != n_columns:
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
with open('my_files/crunchbase_info_tidy.json') as json_file:
    data = json.load(json_file)

    for x in data[:3]:
        print("£££££" + x['name'])
        for ix in x['ixbrl_info']:
            print(ix['ixbrl_acc_link'])        
        
        

"""        
url = "https://beta.companieshouse.gov.uk/company/NI618621/filing-history/MzI2NDA4NTc0NmFkaXF6a2N4/document?format=xhtml&download=1"
hp = HTMLTableParser()
table = hp.parse_url(url)[0][1] # Grabbing the table from the tuple
table_headers = (table.columns)


for header in table_headers:
    table[header] = table[header].replace('[\n,]','',regex = True)

print(table)

"""