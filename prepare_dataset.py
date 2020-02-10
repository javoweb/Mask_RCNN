import json
import csv
import os


# create csv file for inference
def generate_csv(input_file):
	with open(input_file) as f:
		data = json.load(f)

	csv_out = open(os.path.join("/onepanel/output/", "classes.csv"), "w", newline='')

	csv_writer = csv.writer(csv_out)
	csv_writer.writerow(['labels','id'])

	for lbl in data['categories']:
		csv_writer.writerow([lbl['name'], lbl['id']])


if __name__ == '__main__':
	import sys
	generate_csv(sys.argv[1])
