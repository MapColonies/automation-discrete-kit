import geopandas
import json
import sys
import logging
from configuration import config

_log = logging.getLogger('discrete_kit.app')


def shp_to_geojson(path):
    try:
        shp_file = geopandas.read_file(path + '.shp')
        geo_json = shp_file._to_geo()
    except Exception as err:
        _log.error(str(err))
        raise Exception(str(err))
    return geo_json


class CreateJsonShape:
    def __init__(self, path):
        self.path = path
        # paths = glob(path + '/*/')  # ToDo: Find the path
        self.shapes_path = path
        self.tiff_path = path
        self.read_shapes = {}
        self.shapes_path += '\\' + 'Shapes' + '\\'
        files_names = ['Files', 'Product', 'ShapeMetadata']
        for name in files_names:
            full_file_path = self.shapes_path + name
            if config.validate_ext_files_exists(full_file_path):
                self.read_shapes[name] = shp_to_geojson(full_file_path)
        temp_json = self.make_full_json()
        print('d')

    # ToDo: Finish to create JSON - originDirectory.
    def make_full_json(self):

        # create_metadata
        self.create_metadata()
        full_json_str = {'fileNames': self.find_filenames(), 'metadata': self.create_metadata(),
                         'layerPolygonParts': self.read_shapes['Files'], 'originDirectory': 'fill it'}
        return json.dumps(full_json_str)

    def find_filenames(self):
        filenames_list = []
        try:
            shapes = self.read_shapes['Files']['features']
        except KeyError:
            raise Exception("Key not found in the Files")

        for shape in shapes:
            filenames_list.append(
                config.get_tiff_basename(self.path) + '/' + shape['properties']['File Name'] + '.tiff')
        return filenames_list


def create_metadata(self):
    # ToDo : Add / Check creationDate, ingestionDate, updateDate, sourceDateStart, sourceDateEnd, accuracyCE90
    try:
        metadata = {'type': config.metadata_type,
                    'productName': self.read_shapes['ShapeMetadata']['features'][0]['properties']['SourceName'],
                    'description': self.read_shapes['ShapeMetadata']['features'][0]['properties']['Dsc'],
                    'creationDate': config.convert_time_to_utc(
                        self.read_shapes['ShapeMetadata']['features'][0]['properties']['UpdateDate']),
                    'ingestionDate': config.convert_time_to_utc(
                        self.read_shapes['ShapeMetadata']['features'][0]['properties']['UpdateDate']),
                    'updateDate': config.convert_time_to_utc(
                        self.read_shapes['ShapeMetadata']['features'][0]['properties']['UpdateDate']),
                    'sourceDateStart': config.convert_time_to_utc(
                        self.read_shapes['ShapeMetadata']['features'][0]['properties']['UpdateDate']),
                    'sourceDateEnd': config.convert_time_to_utc(
                        self.read_shapes['ShapeMetadata']['features'][0]['properties']['UpdateDate']),
                    'accuracyCE90': '',
                    'sensorType': [self.read_shapes['ShapeMetadata']['features'][0]['properties']['SensorType']],
                    'productId':
                        self.read_shapes['ShapeMetadata']['features'][0]['properties']['Source'].split('-')[0],
                    'productVersion':
                        self.read_shapes['ShapeMetadata']['features'][0]['properties']['Source'].split('-')[1],
                    'productType': self.read_shapes['Product']['features'][0]['properties']['Type'],
                    'resolution': float(self.read_shapes['Product']['features'][0]['properties']['Resolution']),
                    'footprint': {'type': self.read_shapes['Product']['features'][0]['geometry']['type'],
                                  'coordinates': [[list(x) for x in
                                                   self.read_shapes['Product']['features'][0]['geometry'][
                                                       'coordinates'][0]]]}}
    except KeyError:
        raise Exception("Key not found in the ShapeMetadata")

    return metadata


# ToDo: Check what should i do with the returned JSON
# ToDo: Check what is the relevant path for the shape folder
c = CreateJsonShape(r'D:\raster\shapes\arzi_mz')
