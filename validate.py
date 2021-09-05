import json
from unittest import *

# temp_json = dict_to_compare['search'][0]

'''
Compared
'''
# temp_json['type'] == json_got['metadata']['type']
# temp_json['productId'] == json_got['metadata']['productId']
# temp_json['productName'] == json_got['metadata']['productName']
# temp_json['description'] == json_got['metadata']['description']
# temp_json['accuracyCE90'] == json_got['metadata']['accuracyCE90']
# temp_json['footprint']['type'] == json_got['metadata']['footprint']['type']
# temp_json['footprint']['coordinates'] == json_got['metadata']['footprint']['coordinates']
# temp_json['layerPolygonParts']['type'] == json_got['metadata']['layerPolygonParts']['type']
# json_got['metadata']['layerPolygonParts']['features'][0]['properties'] == temp_json['layerPolygonParts']['features'][0]['properties']
# json_got['metadata']['layerPolygonParts']['features'][0]['geometry'] == temp_json['layerPolygonParts']['features'][0]['geometry']
# json_got['metadata']['layerPolygonParts']['bbox'] == temp_json['layerPolygonParts']['bbox']
# json_got['metadata']['sensorType'] == temp_json['sensorType']
# json_got['metadata']['sourceDateEnd'][:19] == temp_json['sourceDateEnd'][:19]


### temp_json['layerPolygonParts'] == json_got['metadata']['layerPolygonParts']

"""  First way  """
# assert temp_json['type'] in json_got['metadata']['type']
# assert temp_json['productId'] in json_got['metadata']['productId']

""" Second way """
# assert temp_json['type'] == json_got['metadata']['type']
# assert temp_json['productId'] == json_got['metadata']['productId']
# assert temp_json['productName'] == json_got['metadata']['productName']
# assert temp_json['description'] == json_got['metadata']['description']
# assert temp_json['accuracyCE90'] == json_got['metadata']['accuracyCE90']
# assert temp_json['footprint']['type'] == json_got['metadata']['footprint']['type']
# assert temp_json['footprint']['coordinates'] == json_got['metadata']['footprint']['coordinates'] , "['footprint']['coordinates'] are not equal"
# assert temp_json['layerPolygonParts']['type'] == json_got['metadata']['layerPolygonParts']['type']
# assert json_got['metadata']['layerPolygonParts']['features'][0]['properties'] == \
#        temp_json['layerPolygonParts']['features'][0]['properties']
# assert json_got['metadata']['layerPolygonParts']['features'][0]['geometry'] == \
#        temp_json['layerPolygonParts']['features'][0]['geometry']
# #assert json_got['metadata']['layerPolygonParts']['bbox'] == temp_json['layerPolygonParts']['bbox']
# assert json_got['metadata']['sensorType'] == temp_json['sensorType']
from discrete_kit.app import *

c = CreateJsonShape(r'D:\raster\shapes\1')
jj = json.loads(c.get_json_output())
print(c.get_json_output())
# assert jj['metadata']['sourceDateEnd'] == temp_json['sourceDateEnd']

print("0")
