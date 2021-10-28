from builtins import Exception

#
# def pycsw_compare(json_pycsw, json_created):
#     prd_id = json_pycsw['data']['search'][0]['productId']
#     prd_name = json_pycsw['data']['search'][0]['productName']
#     sensor_type = json_pycsw['data']['search'][0]['sensorType']
#     description = json_pycsw['data']['search'][0]['description']
#     scale = json_pycsw['data']['search'][0]['scale']
#     footprint_type = json_pycsw['data']['search'][0]['footprint']['type']
#     footprint_coordinates = json_pycsw['data']['search'][0]['footprint']['coordinates']
#     layer_polygon_parts_bbox = json_pycsw['data']['search'][0]['layerPolygonParts']['bbox']
#     layer_polygon_parts_type = json_pycsw['data']['search'][0]['layerPolygonParts']['type']
#     layer_polygon_parts_features = json_pycsw['data']['search'][0]['layerPolygonParts']['features']
#     raster_type = json_pycsw['data']['search'][0]['type']
#     raster_id = json_pycsw['data']['search'][0]['id']
#     accuracyCE90 = json_pycsw['data']['search'][0]['accuracyCE90']
#     source_date_end = json_pycsw['data']['search'][0]['sourceDateEnd']
#     links_list = json_pycsw['data']['search'][0]['links']
#
#     assert prd_name == json_created['metadata']['productName']
#     assert raster_type == json_created['metadata']['type']
#     assert prd_id == json_created['metadata']['productId']
#     assert description == json_created['metadata']['description']
#     assert accuracyCE90 == json_created['metadata']['accuracyCE90']
#     assert footprint_type == json_created['metadata']['footprint']['type']
#     # assert footprint_coordinates == json_created['metadata']['footprint']['coordinates']
#     # assert layer_polygon_parts_bbox == json_created['layerPolygonParts']['bbox']
#     assert json_created['metadata']['sensorType'] == sensor_type
#     assert source_date_end == json_created['metadata']['sourceDateEnd']
#
#     assert scale == json_created['metadata']['layerPolygonParts']['features'][0]['properties']['Scale']
#     assert layer_polygon_parts_type == json_created['metadata']['layerPolygonParts']['type']
#     assert layer_polygon_parts_features == json_created['metadata']['layerPolygonParts']['features']


#
# def replace_json_nulls(rcv_json):
#     rcv_json

def validate_pycsw_with_shape_json(pycws_json, shape_json):
    missing_values = {}
    error_flag = True

    if pycws_json is None:
        missing_values['PYCSW_JSON'] = 'Empty JSON'
        return False, missing_values
    if shape_json is None:
        missing_values['ShapeJSON'] = 'Empty JSON'
        return False, missing_values

    try:
        # ToDo: Added History Ortophoto JSON.
        original_ortophoto_json = pycws_json['data']['search'][0]

    except KeyError:
        missing_values['data']['search'] = {'Expected': 'JSON', 'Actual': 'Missing JSON'}
        error_flag = False

    for o_k, o_v in original_ortophoto_json.items():
        if o_k is not '__typename':
            try:
                if shape_json['metadata'][o_k] != o_v:
                    missing_values[o_k] = {'Expected': str(o_v), 'Actual': str(shape_json['metadata'][o_k])}
                    # missmatch_values[o_k] = 'Expected : ' + str(o_v) + ' , Actual : ' + str(shape_json['metadata'][o_k])
            except KeyError:
                missing_values[o_k] = {'Expected': str(o_v), 'Actual': 'Missing Key in PYCSW JSON'}
                error_flag = False

    # history_ortophoto_json = pycws_json['data']['search'][1]

    return error_flag, missing_values
