import xml.etree.ElementTree as ET
import requests

# Listing all of the .geojson files in this bucvket that are associated with Georgia
r = requests.get("https://gm-zdm.s3.amazonaws.com/?prefix=gj/pol/ga")

tree = ET.fromstring(r.content)

ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}

for key in root.iter("{http://s3.amazonaws.com/doc/2006-03-01/}Key"):
    if key.text.endswith(".geojson"):
        print("https://s3.amazonaws.com/gm-zdm/" + key.text)

urls = []
