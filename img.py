import pandas as pd
import numpy as np
import requests
from StringIO import StringIO
from PIL import Image

counter = 0
bad_requests = []

img_urls = pd.read_csv("image_urls.csv",delimiter=";")

for each_url in img_urls:
    counter += 1
    image_name = str(counter) + ".jpg"
    r = requests.get(each_url)

    if r.status_code == 200:
        try:
            i = Image.open(StringIO(r.content))
            i.save(image_name)
            # print(each_url)
        except:
            bad_requests.append(counter)
    
    if counter%100:
        print(counter)

print("Completed successfully")
print("Couldn't download" + str(len(bad_requests)))
