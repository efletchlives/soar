import ee
import geemap
import os
from PIL import Image
import numpy as np

# functions


# geemap.update_package()

# authenticate and initialize google earth engine
# ee.Authenticate(auth_mode='notebook')
ee.Initialize()
print("connected successfully!")


# pick a center point for your photo
region = ee.Geometry.Polygon([
    [[-99.88, 32.88],
     [-99.88, 32.87],
     [-99.87, 32.87],
     [-99.87, 32.88],
     [-99.88, 32.88]]
]) # (longitude, latitude)

# pick 2km x 2km area 

# choose a satellite image collection (with help from chatgpt)
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(region)
    .filterDate("2023-04-01", "2023-05-01")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30))
)

image = collection.median().clip(region)
rgb = image.select(["B4", "B3", "B2"])

arr = geemap.ee_to_numpy(rgb, region=region, scale=10)
arr = np.nan_to_num(arr)
arr = (arr / arr.max() * 255).astype(np.uint8)

path = '/workspaces/soar/texas_pics'
png = os.path.join(path,'texas_patch.png')
Image.fromarray(arr).save(png)


print('successfully exported image')





