import boto3
import os
from botocore import UNSIGNED
from botocore.config import Config
import csv
import geojson 

s3 = boto3.client(
    's3',
    config=Config(signature_version=UNSIGNED)
)

#Up to date state district information
#https://data.openstates.org/people/current/ga.csv

all_features = []

bucket="gm-zdm"
response = s3.list_objects_v2(Bucket=bucket,Prefix='gj/pol/ga')

for obj in response.get('Contents', []):
    key = obj['Key']
    local_path = os.path.join('.', key)

    # create directories if needed
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    try:
        s3.download_file(bucket, key, local_path)
        
        with open(local_path, 'r') as file:
            district = geojson.load(file)

        for feature in district["features"]:
            district_type = feature["properties"]["zdm_id"]
            district_number = feature["properties"]["pnm"]

            with open("ga.csv", newline="") as f:
                district_info = csv.DictReader(f)

                if "rep" in district_type:
                    for row in district_info:    
                        if row["current_district"] == district_number and row["current_chamber"] == "lower":
                            district['features'][0]['properties']['current_party'] = row["current_party"]
                            district['features'][0]['properties']['current_chamber'] = row["current_chamber"]
                            district['features'][0]['properties']['rep_name'] = row["name"]
                            
                if "sen" in district_type:
                    for row in district_info:    
                        if row["current_district"] == district_number and row["current_chamber"] == "upper":
                            district['features'][0]['properties']['current_chamber'] = row["current_chamber"]
                            district['features'][0]['properties']['current_party'] = row["current_party"]
                            district['features'][0]['properties']['rep_name'] = row["name"]
            
            all_features.extend(district.get("features", []))                

        combined = geojson.FeatureCollection(all_features)
        with open('ga_assembly.geojson', 'w') as file:
            geojson.dump(combined, file)

        print(f"Downloaded {key}")
    except Exception as e:
        print(e)
