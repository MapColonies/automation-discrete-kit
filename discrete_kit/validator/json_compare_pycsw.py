import json
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
    pycsw_history_json = pycws_json[0]
    pycsw_original_json = pycws_json[1]
    for dic in pycws_json:
        if dic.get('mcraster:productType') == 'OrthophotoHistory':
            pycsw_history_json = dic
        else:
            pycsw_original_json = dic
    shape_json_metadata = shape_json['metadata']
    if shape_json_metadata['productId']['value'] != pycsw_original_json['mc:productId']:
        missing_values['productId'] = {'Expected: ' + shape_json_metadata['productId']['value'],
                                       'Actual: ' + pycsw_original_json['mc:productId']}

    if shape_json_metadata['productName']['value'] != pycsw_original_json['mc:productName']:
        missing_values['productName'] = {'Expected: ' + shape_json_metadata['productName']['value'],
                                         'Actual: ' + pycsw_original_json['mc:productName']}

    if shape_json_metadata['productVersion']['value'] != pycsw_original_json['mc:productVersion']:
        missing_values['productVersion'] = {'Expected: ' + shape_json_metadata['productVersion']['value'],
                                            'Actual: ' + pycsw_original_json['mc:productVersion']}

    if shape_json_metadata['productType']['value'] != pycsw_original_json['mc:productType']:
        missing_values['productType'] = {'Expected: ' + shape_json_metadata['productType']['value'],
                                         'Actual: ' + pycsw_original_json['mc:productVersion']}

    if shape_json_metadata['description']['value'] != pycsw_original_json['mc:description']:
        missing_values['description'] = {'Expected: ' + shape_json_metadata['description']['value'],
                                         'Actual: ' + pycsw_original_json['mc:description']}

    if shape_json_metadata['resolution']['value'] != pycsw_original_json['mc:maxResolutionDeg']:
        missing_values['resolution'] = {'Expected: ' + shape_json_metadata['resolution']['value'],
                                        'Actual: ' + pycsw_original_json['mc:maxResolutionDeg']}

    # ToDo: Check Max Resolution
    # if shape_json_metadata['resolution']['value'] != pycsw_original_json['mcraster:maxResolutionDeg']:
    #     missing_values['resolution'] = {'Expected: ' + shape_json_metadata['resolution']['value'],
    #                                      'Acutal: ' + pycsw_original_json['mcraster:maxResolutionDeg']}

    if str(shape_json_metadata['accuracyCE90']) != pycsw_original_json['mc:minHorizontalAccuracyCE90']:
        missing_values['Accuracy'] = {'Expected: ' + str(shape_json_metadata['accuracyCE90']),
                                      'Actual: ' + pycsw_original_json['mc:minHorizontalAccuracyCE90']}

    if shape_json_metadata['sensorType']['value'] != pycsw_original_json['mc:sensors']:
        missing_values['sensors'] = {'Expected: ' + shape_json_metadata['sensorType']['value'],
                                     'Actual: ' + pycsw_original_json['mc:sensors']}

    if json.dumps(shape_json_metadata['footprint']) != pycsw_original_json['mc:footprint']:
        missing_values['footprint'] = {'Expected: ' + json.dumps(shape_json_metadata['footprint']),
                                       'Actual: ' + pycsw_original_json['mc:footprint']}

    if shape_json_metadata['region']['value'] != pycsw_original_json['mc:region']:
        missing_values['region'] = {'Expected: ' + shape_json_metadata['sensorType']['value'],
                                    'Actual: ' + str(pycsw_original_json['mc:region'])}

    if shape_json_metadata['srsId']['value'] != pycsw_original_json['mc:SRS']:
        missing_values['srsId'] = {'Expected: ' + shape_json_metadata['srsId']['value'],
                                   'Actual: ' + str(pycsw_original_json['mc:SRS'])}

    if shape_json_metadata['srsName']['value'] != pycsw_original_json['mc:SRSName']:
        missing_values['srsName'] = {'Expected: ' + shape_json_metadata['srsName']['value'],
                                     'Actual: ' + str(pycsw_original_json['mc:SRSName'])}

    for k, v in json.loads(pycsw_original_json['mc:layerPolygonParts']).items():
        try:
            if k == 'bbox':
                if shape_json_metadata['layerPolygonParts']['bbox'] != v:
                    missing_values[k] = {'Expected': str(v),
                                         'Actual': str(shape_json_metadata['layerPolygonParts']['bbox'])}
            elif shape_json_metadata['layerPolygonParts']['value'][k] != v:
                missing_values[k] = {'Expected': str(v),
                                     'Actual': str(shape_json_metadata['layerPolygonParts']['value'][k])}
                # missmatch_values[o_k] = 'Expected : ' + str(o_v) + ' , Actual : ' + str(shape_json['metadata'][o_k])
        except KeyError:
            missing_values[k] = {'Expected': str(v), 'Actual': 'Missing Key in PYCSW JSON'}
            error_flag = False
    if len(missing_values) != 0:
        error_flag = False
    return True, missing_values
    #
    # if is_history:
    #     pass
    # if pycws_json is None:
    #     missing_values['PYCSW_JSON'] = 'Empty JSON'
    #     return False, missing_values
    # if shape_json is None:
    #     missing_values['ShapeJSON'] = 'Empty JSON'
    #     return False, missing_values

    #
    #
    #
    #
    # try:
    #     # ToDo: Added History Ortophoto JSON.
    #     original_ortophoto_json = pycws_json['data']['search'][0]
    #
    # except KeyError:
    #     missing_values['data']['search'] = {'Expected': 'JSON', 'Actual': 'Missing JSON'}
    #     error_flag = False
    #
    # for o_k, o_v in original_ortophoto_json.items():
    #     if o_k is not '__typename':
    #         try:
    #             if shape_json['metadata'][o_k] != o_v:
    #                 missing_values[o_k] = {'Expected': str(o_v), 'Actual': str(shape_json['metadata'][o_k])}
    #                 # missmatch_values[o_k] = 'Expected : ' + str(o_v) + ' , Actual : ' + str(shape_json['metadata'][o_k])
    #         except KeyError:
    #             missing_values[o_k] = {'Expected': str(o_v), 'Actual': 'Missing Key in PYCSW JSON'}
    #             error_flag = False

    # history_ortophoto_json = pycws_json['data']['search'][1]

    return error_flag, missing_values


def validate_pycsw_with_shape_json_old_version(pycws_json, shape_json):
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
