import ee
import os
import json
import geemap
# geemap.update_package()

# authenticate and initialize google earth engine
# ee.Authenticate(auth_mode='notebook')
ee.Initialize()
print("connected successfully!")


# pick a center point for your photo
region = ee.Geometry.Polygon([
    [[-100.0, 33.0],
     [-100.0, 32.5],
     [-99.5, 32.5],
     [-99.5, 33.0],
     [-100.0, 33.0]]
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

# export as png
geemap.ee_export_image(
    rgb,
    filename="/workspaces/soar/texas_patch.tif",
    scale=50,
    region=region,
    file_per_band=False
)

print('successfully exported image')





