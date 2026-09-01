import requests
from pathlib import Path
import zipfile

response = requests.get("https://s3.amazonaws.com/baywheels-data/")
print(response.status_code)
print(response.text[:2000])

import xml.etree.ElementTree as ET
namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
root = ET.fromstring(response.text)

keys = []
for key in root.findall(".//s3:Key", namespace):
    keys.append(key.text)

#check that the file ends in tripdata.csv.zip
#the first four characters in the file name are the year
#check the file ending before checking the year
Path("data/raw").mkdir(parents=True, exist_ok=True)

for k in keys:
    if "tripdata" in k and k.endswith('.zip') and int(k[:4]) > 2018:
        print(f"Downloading {k}...")
        local_path = Path("data/raw/" + k)

        if local_path.exists():
            continue

        response = requests.get("https://s3.amazonaws.com/baywheels-data/" + k)
        if response.status_code != 200:
            print(f"Failed to download {k}: status {response.status_code}")
            continue
        with open(local_path, "wb") as f:
            f.write(response.content)

#get list of zip files
for zip_path in Path("data/raw").glob("*.zip"):

    with zipfile.ZipFile(zip_path) as zf:
        for f in zf.namelist():
            local_path = Path("data/interim/" + f)
            if f.startswith("__MACOSX"):
                continue
            elif local_path.exists():
                continue
            else:
                zf.extract(f, "data/interim")