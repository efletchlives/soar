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
# center_lon, center_lat = -99.885, 32.8845
# width_m = 200  # meters
# height_m = 200  # meters

# # Earth Engine distances are in degrees, so approximate:
# deg_per_meter = 1 / 111320  # ~meters per degree latitude

# region = ee.Geometry.Rectangle([
#     center_lon - width_m * deg_per_meter / 2,
#     center_lat - height_m * deg_per_meter / 2,
#     center_lon + width_m * deg_per_meter / 2,
#     center_lat + height_m * deg_per_meter / 2
# ])

region = ee.Geometry.Polygon([
    [[-99.9, 32.9],
     [-99.9, 32.8],
     [-99.8, 32.8],
     [-99.8, 32.9],
     [-99.9, 32.9]]
])

# (longitude, latitude)

# pick 2km x 2km area 

# choose a satellite image collection (with help from chatgpt)
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")  # other choice: "USDA/NAIP/DOQQ"
    .filterBounds(region)
    .filterDate("2023-04-01", "2023-05-01")
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30))
)

image = collection.median().clip(region)
rgb = image.select(["B4", "B3", "B2"])

arr = geemap.ee_to_numpy(rgb, region=region, scale=20)
arr = np.nan_to_num(arr)
arr = (arr / arr.max() * 255).astype(np.uint8)

path = '/workspaces/soar/texas_pics'
png = os.path.join(path,'texas_patch.png')
Image.fromarray(arr).save(png)


print('successfully exported image')





