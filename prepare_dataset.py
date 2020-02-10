import json
import csv
import os

# create csv file for inference
with open("annotations.json") as f:
	data = json.load(f)

csv_out = open(os.path.join("/onepanel/output/", "classes.csv"), "w", newline='')

csv_writer = csv.writer(csv_out)
csv_writer.writerow(['labels','id'])

for lbl in data['categories']:
	csv_writer.writerow([lbl['name'], lbl['id']])
