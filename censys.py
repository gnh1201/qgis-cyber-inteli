# censys.py
# Require: QGIS (3.28.3-Firenze)
# Namhyeon Go <abuse@catswords.net>
# 2023-02-14

from qgis.core import (
    QgsVectorLayer,
    QgsPointXY,
    QgsField,
    QgsFeature,
    QgsProject,
    QgsCoordinateReferenceSystem,
)

from censys.search import CensysHosts
import os

# Connect to Censys API
censys_api_id = "YOUR_API_KEY"
censys_api_secret = "YOUR_API_SECRET"
censys = CensysHosts(api_id=censys_api_id, api_secret=censys_api_secret)

# Set up new point layer for results
layer_name = "Censys Hosts"
crs = QgsCoordinateReferenceSystem("EPSG:4326")
fields = [
    QgsField("ip", QVariant.String),
    QgsField("protocol", QVariant.String),
    QgsField("port", QVariant.Int),
]
writer = QgsVectorLayer(
    "Point?crs={}".format(crs.authid()), layer_name, "memory"
)
provider = writer.dataProvider()
for field in fields:
    provider.addAttributes([field])
writer.updateFields()

# Search Censys and add results to the point layer
query = censys.search("services.service_name: S7", per_page=100, pages=5)

for page in query:
    for result in page:
        print(result["location"]["coordinates"]["longitude"], result["location"]["coordinates"]["latitude"])
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(result["location"]["coordinates"]["longitude"], result["location"]["coordinates"]["latitude"])))
        feature.setAttributes([result["ip"], result["services"][0]["service_name"], result["services"][0]["port"]])
        provider.addFeatures([feature])

# Add the point layer to the current QGIS project
project = QgsProject.instance()
project.addMapLayer(writer)
