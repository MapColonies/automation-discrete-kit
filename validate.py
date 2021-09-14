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
# from discrete_kit.app import *
#
# c = CreateJsonShape(r'D:\raster\shapes\1')
# jj = json.loads(c.get_json_output())
# print(c.get_json_output())
# # assert jj['metadata']['sourceDateEnd'] == temp_json['sourceDateEnd']
#
# print("0")


def pycsw_compare(json_pycsw, json_created):
    prd_id = json_pycsw['data']['search'][0]['productId']
    prd_name = json_pycsw['data']['search'][0]['productName']
    sensor_type = json_pycsw['data']['search'][0]['sensorType']
    description = json_pycsw['data']['search'][0]['description']
    scale = json_pycsw['data']['search'][0]['scale']
    footprint_type = json_pycsw['data']['search'][0]['footprint']['type']
    footprint_coordinates = json_pycsw['data']['search'][0]['footprint']['coordinates']
    layer_polygon_parts_bbox = json_pycsw['data']['search'][0]['layerPolygonParts']['bbox']
    layer_polygon_parts_type = json_pycsw['data']['search'][0]['layerPolygonParts']['type']
    layer_polygon_parts_features = json_pycsw['data']['search'][0]['layerPolygonParts']['features']
    raster_type = json_pycsw['data']['search'][0]['type']
    raster_id = json_pycsw['data']['search'][0]['id']
    accuracyCE90 = json_pycsw['data']['search'][0]['accuracyCE90']
    source_date_end = json_pycsw['data']['search'][0]['sourceDateEnd']
    links_list = json_pycsw['data']['search'][0]['links']

    assert prd_name == json_created['metadata']['productName']
    assert raster_type == json_created['metadata']['type']
    assert prd_id == json_created['metadata']['productId']
    assert description == json_created['metadata']['description']
    assert accuracyCE90 == json_created['metadata']['accuracyCE90']
    assert footprint_type == json_created['metadata']['footprint']['type']
    # assert footprint_coordinates == json_created['metadata']['footprint']['coordinates']
    # assert layer_polygon_parts_bbox == json_created['layerPolygonParts']['bbox']
    assert json_created['metadata']['sensorType'] == sensor_type
    assert source_date_end == json_created['metadata']['sourceDateEnd']

    assert scale == json_created['metadata']['layerPolygonParts']['features'][0]['properties']['Scale']
    assert layer_polygon_parts_type == json_created['metadata']['layerPolygonParts']['type']
    assert layer_polygon_parts_features == json_created['metadata']['layerPolygonParts']['features']


psyc_get = {'data': {'search': [
    {'__typename': 'LayerRasterRecord', 'productId': 'MAS_6_ORT_247993', 'productName': 'O_arzi_mz_w84geo_Tiff_20cm',
     'sensorType': ['OTHER'], 'description': 'תשתית אורתופוטו בישראל עדכני לאפריל 2019', 'scale': None,
     'footprint': {'type': 'Polygon', 'coordinates': [
         [[34.8468438649828, 32.0689996810298], [34.8637856279928, 32.0590059440186],
          [34.8773961450173, 32.0680478960404], [34.8804418550117, 32.0528193460686],
          [34.8786334639958, 32.0466327470143], [34.8605495609931, 32.0488218510146],
          [34.8468438649828, 32.0689996810298]]]},
     'layerPolygonParts': {'bbox': [34.8468438649828, 32.0466327470143, 34.8804418550117, 32.0689996810298],
                           'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'Polygon',
                                                                                                      'coordinates': [[[
                                                                                                          34.8468438649828,
                                                                                                          32.0689996810298],
                                                                                                          [
                                                                                                              34.8637856279928,
                                                                                                              32.0590059440186],
                                                                                                          [
                                                                                                              34.8773961450173,
                                                                                                              32.0680478960404],
                                                                                                          [
                                                                                                              34.8804418550117,
                                                                                                              32.0528193460686],
                                                                                                          [
                                                                                                              34.8786334639958,
                                                                                                              32.0466327470143],
                                                                                                          [
                                                                                                              34.8605495609931,
                                                                                                              32.0488218510146],
                                                                                                          [
                                                                                                              34.8468438649828,
                                                                                                              32.0689996810298]]]},
                                                                      'properties': {
                                                                          'Dsc': 'תשתית אורתופוטו בישראל עדכני לאפריל 2019',
                                                                          'Rms': None, 'Ep90': '3', 'Scale': None,
                                                                          'Source': 'MAS_6_ORT_247993-1.0',
                                                                          'Resolution': '0.2', 'SensorType': 'OTHER',
                                                                          'SourceName': 'O_arzi_mz_w84geo_Tiff_20cm',
                                                                          'UpdateDate': '06/04/2019'}}]},
     'type': 'RECORD_RASTER', 'id': 'e8962f2d-1b2e-483c-aeab-a8e58be248e2', 'accuracyCE90': 3,
     'sourceDateEnd': '2019-06-04T00:00:00.000Z', 'links': [{'name': None, 'description': None, 'protocol': 'WMS',
                                                             'url': 'http://mapproxy-qa-map-proxy-map-proxy-route-raster-dev.apps.v0h0bdx6.eastus.aroapp.io/service?REQUEST=GetCapabilities'},
                                                            {'name': None, 'description': None, 'protocol': 'WMTS',
                                                             'url': 'http://mapproxy-qa-map-proxy-map-proxy-route-raster-dev.apps.v0h0bdx6.eastus.aroapp.io/wmts/1.0.0/WMTSCapabilities.xml'},
                                                            {'name': None, 'description': None, 'protocol': 'WMTS_tile',
                                                             'url': 'http://mapproxy-qa-map-proxy-map-proxy-route-raster-dev.apps.v0h0bdx6.eastus.aroapp.io/wmts/MAS_6_ORT_247993-1.0/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png'}]}]}}

app_json = {"fileNames": ["tiff/O_arzi_mz_w84geo_Apr19_tiff_0.2.tiff"],
            "metadata": {"type": "RECORD_RASTER", "productName": "O_arzi_mz_w84geo_Tiff_20cm",
                         "description": "תשתית אורתופוטו בישראל עדכני לאפריל 2019",
                         "creationDate": "2019-06-04T00:00:00.000Z", "ingestionDate": "2019-06-04T00:00:00.000Z",
                         "updateDate": "2019-06-04T00:00:00.000Z", "sourceDateStart": "2019-06-04T00:00:00.000Z",
                         "sourceDateEnd": "2019-06-04T00:00:00.000Z", "accuracyCE90": 3, "sensorType": ["OTHER"],
                         "productId": "MAS_6_ORT_247993", "productVersion": "1.0", "productType": "Orthophoto",
                         "resolution": 0.2, "footprint": {"type": "Polygon", "coordinates": [
                    [[34.8468438649768, 32.0689996810415], [34.8637856279967, 32.0590059440131],
                     [34.8773961450108, 32.0680478960332], [34.8804418550096, 32.0528193460393],
                     [34.8786334639992, 32.0466327470035], [34.8605495610029, 32.0488218510031],
                     [34.8468438649768, 32.0689996810415]]]}, "layerPolygonParts": {"type": "FeatureCollection",
                                                                                    "features": [{"type": "Feature",
                                                                                                  "properties": {
                                                                                                      "Dsc": "תשתית אורתופוטו בישראל עדכני לאפריל 2019",
                                                                                                      "Ep90": "3",
                                                                                                      "Resolution": "0.2",
                                                                                                      "Rms": None,
                                                                                                      "Scale": None,
                                                                                                      "SensorType": "OTHER",
                                                                                                      "Source": "MAS_6_ORT_247993-1.0",
                                                                                                      "SourceName": "O_arzi_mz_w84geo_Tiff_20cm",
                                                                                                      "UpdateDate": "06/04/2019"},
                                                                                                  "geometry": {
                                                                                                      "type": "Polygon",
                                                                                                      "coordinates": [[[
                                                                                                          34.8468438649828,
                                                                                                          32.0689996810298],
                                                                                                          [
                                                                                                              34.8637856279928,
                                                                                                              32.0590059440186],
                                                                                                          [
                                                                                                              34.8773961450173,
                                                                                                              32.0680478960404],
                                                                                                          [
                                                                                                              34.8804418550117,
                                                                                                              32.0528193460686],
                                                                                                          [
                                                                                                              34.8786334639958,
                                                                                                              32.0466327470143],
                                                                                                          [
                                                                                                              34.8605495609931,
                                                                                                              32.0488218510146],
                                                                                                          [
                                                                                                              34.8468438649828,
                                                                                                              32.0689996810298]]]}}],
                                                                                    "bbox": [34.8468438649768,
                                                                                             32.0466327470035,
                                                                                             34.8804418550096,
                                                                                             32.0689996810415]}},
            "originDirectory": "shapes/1"}
pycsw_compare(psyc_get, app_json)
print(())
