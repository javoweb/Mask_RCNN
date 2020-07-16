# Prepares Dataset for the corresponding job with Trained Model and Classes File

import json
import csv
import os
import glob

# create csv file for inference
def generate_csv(dataset_dir):
    sub_directories = next(os.walk(dataset_dir))[1]
    csv_out = open(os.path.join("./", "classes.csv"), "w", newline='')

    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(['labels','id'])
    labels = []
    for sub_dir in sub_directories:
        with open(os.path.join(dataset_dir, sub_dir, "annotations/instances_default.json", )) as f:
            data = json.load(f)

       

        for lbl in data['categories']:
            if lbl['name'] not in labels:
                csv_writer.writerow([lbl['name'], lbl['id']])
                labels.append(lbl['name'])


if __name__ == '__main__':
    import sys
    from pprint import pprint

    generate_csv(sys.argv[1])