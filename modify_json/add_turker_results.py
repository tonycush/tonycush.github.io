import json
import re

with open('my_files/crunchbase_info_tidy.json') as json_file:
    all_data = json.load(json_file)
with open('my_files/approved_results.json') as turker_json_file:
    turker_data = json.load(turker_json_file)


#find any company numbers that have been turker
comps_turked = []
for turked in turker_data:
    if turked["company_number"] not in comps_turked:
        comps_turked.append(turked["company_number"])

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

print(len(turker_data))
print(len(comps_turked))
for comp in comps_turked:
    this_comps_turked_jobs = []
    for turked in turker_data:
        if turked["company_number"] == comp:
            this_comps_turked_jobs.append(turked)
    
    cb_data_index = find(all_data,"company_number",comp)
    print(cb_data_index)
    all_data[cb_data_index]["turked_answers"] = json.dumps(this_comps_turked_jobs)
    all_data[cb_data_index]["turked_answers"] = json.loads(all_data[cb_data_index]["turked_answers"])
    print(type(all_data[cb_data_index]["turked_answers"]))
    print(type(all_data[cb_data_index]["sections"]))
    print("\n** "+comp+" : "+all_data[cb_data_index]["name"]+" ***")
with open('crunchbase_info_tidy_sample1.json','w') as outfile:
    json.dump(all_data,outfile)