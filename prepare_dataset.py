# Prepares Dataset for the corresponding job with Trained Model and Classes File

import json
import csv
import os
import glob
mport boto3
from botocore.exceptions import ClientError



# create csv file for inference
def generate_csv(input_file):
	with open(input_file) as f:
		data = json.load(f)

	csv_out = open(os.path.join("/mnt/output/", "classes.csv"), "w", newline='')

	csv_writer = csv.writer(csv_out)
	csv_writer.writerow(['labels','id'])

	for lbl in data['categories']:
		csv_writer.writerow([lbl['name'], lbl['id']])


if __name__ == '__main__':
	import sys
	from pprint import pprint

	generate_csv(sys.argv[1])

	from datetime import datetime
	time = datetime.now()
	stamp = time.strftime("%m%d%Y%H%M%S")
	dataset_name = "maskrcnn-model-output-{}".format(stamp)
# 	os.system("onepanel datasets create {}".format(dataset_name))
	
# 	os.chdir("/onepanel/code/{}".format(dataset_name))
# 	os.system("cp /onepanel/output/classes.csv /onepanel/code/{}/".format(dataset_name))
	for i,_,_ in os.walk("/mnt/output/logs"):
		if "cvat" in i:
			model_path = i
	if not model_path.endswith("/"):
		model_path += "/"
	# find last saved model
	latest_model = max(glob.glob(model_path+"mask*"), key=os.path.getctime)
# 	os.system("cp {} /onepanel/code/{}/".format(latest_model,dataset_name))
	if os.getenv("AWS_BUCKET_NAME", None) is None:
		msg = "AWS_BUCKET_NAME environment var does not exist. Please add ENV var with bucket name."
		raise
	aws_s3_path = os.getenv('AWS_S3_PREFIX')+'/'+os.getenv('ONEPANEL_RESOURCE_NAMESPACE')+'/'+os.getenv('ONEPANEL_RESOURCE_UID')+'/models/'
	try:  # models dir exists
		s3_client.head_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=aws_s3_path)
	except ClientError:
		s3_client.put_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=(aws_s3_path))
	try:
		dir_name = aws_s3_path+dataset_name+'/'
		s3_client.put_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=(dir_name))
		response = s3_client.upload_file(latest_model, os.getenv('AWS_BUCKET_NAME'),dir_name+os.path.basename(latest_model))
		response = s3_client.upload_file("/mnt/output/classes.csv", os.getenv('AWS_BUCKET_NAME'), dir_name+"classes.csv")
		print("\n\n")
		print("*******************************************************************************")
		print("Dataset with Trained Model: ", dir_name)
	except ClientError as e:
		print("**** One or more file failed to upload to S3 ***")
		raise
