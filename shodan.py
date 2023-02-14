# shodan.py
# Require: QGIS (3.28.3-Firenze)
# Namhyeon Go <abuse@catswords.net>
# 2023-02-14

import shodan
from qgis.core import QgsPointXY, QgsGeometry, QgsVectorLayer, QgsField, QgsFeature, QgsCoordinateReferenceSystem

# Connect to Shodan API
SHODAN_API_KEY = "YOUR_API_KEY"
api = shodan.Shodan(SHODAN_API_KEY)

# Search Shodan for your query and location
query = "apache"
#location = "Los Angeles, California"
results = api.search(f"{query}")

# Create a new point layer in QGIS
layer = QgsVectorLayer("Point?crs=EPSG:4326", "Shodan results", "memory")
layer_data = layer.dataProvider()
layer.startEditing()

# Add fields for the point data
layer_data.addAttributes([QgsField("ip",  QVariant.String)])

# Loop through the results and add points to the layer
for result in results['matches']:
    lat = result['location']['latitude']
    lon = result['location']['longitude']
    ip = result['ip_str']
    print(lon, lat)
    point = QgsPointXY(lon, lat)
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPointXY(point))
    feature.setAttributes([ip])
    layer_data.addFeature(feature)

layer.commitChanges()

# Add the layer to the QGIS map
crs = QgsCoordinateReferenceSystem("EPSG:4326")
layer.setCrs(crs)
QgsProject.instance().addMapLayer(layer)
