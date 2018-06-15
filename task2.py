#Task 2


# pip install csv and requests before executing this file

import csv
import json
import copy
import requests
import itertools


url = 'https://data.cityofnewyork.us/api/views/25th-nujf/rows.json'
print "Making request to fetch JSON file"
response = requests.get(url)

print "Loading JSON data"
baby_names_data = json.loads(response.text) # result 1

column_names = [key["name"] for key in baby_names_data["meta"]["view"]["columns"]]

data = baby_names_data["data"]

select_columns = ["Child's First Name", "Gender", "Ethnicity", "Year of Birth", "Rank", "Count"]

def tabulize_data(data, columns, select_columns=None):
    table = []
    for entry in data:
        rec = {}
        for index, key in enumerate(columns):
            # if (key in select_columns): rec[key] = entry[index]
            rec[key] = entry[index]
        table.append(rec.copy())
    return table

# second result
print "Tabularizing the given data"
result1 = tabulize_data(data, column_names, select_columns)


# third result
print "Reducing data to selected columns"
filtered_data = [dict((k, v) for k, v in rec.iteritems() if k in select_columns) for rec in result1]

selected_years = map(str, list(range(2012, 2014 + 1)))

print "Filtering data by Year"
filter_by_year = [rec for rec in filtered_data if rec['Year of Birth'] in selected_years]

# fourth result
print "Grouping the data by Child's First Name and Ethnicity"
grouped_data = itertools.groupby(filter_by_year, key=lambda d: (d["Child's First Name"], d["Ethnicity"]))

# Group by Child's First Name and Ethnicity
# Sum of Count for each such combination
print "Computing the sum of counts for each combination"
grouped_data_count = []
for key, val in grouped_data:
    rec = {"Child's First Name": key[0], "Ethnicity": key[1]}
    rec["Count"] = sum([int(each["Count"]) for each in val])
    grouped_data_count.append(rec.copy())

print "Writing to json file"
# Writing to JSON file
with open("result.json", "w") as json_file:
    json.dump(grouped_data_count, json_file)

print "Writing to csv file"
# Write to CSV file
with open("result.csv", "w") as csv_file:
    header = grouped_data_count[0].keys()
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(header)
    for each_entry in grouped_data_count:
        csv_writer.writerow(each_entry.values())
