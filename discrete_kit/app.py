import json
import logging
import os

import geopandas
from pathlib import Path
from validator import schema_validator
from validator import json_compare_pycsw
from configuration import config

_log = logging.getLogger('discrete_kit.app')


def shp_to_geojson(path):
    """
    This function reads shp files.
    :param path: path to to file with suffix shp
    :return: JSON string.
    """
    try:
        shp_file = geopandas.read_file(path + '.shp')
        geo_json = shp_file._to_geo()
    except Exception as err:
        _log.error(str(err))
        raise Exception(str(err))
    return geo_json


class CreateJsonShape:
    def __init__(self, folder_path):
        self.path = folder_path
        self.shapes_path = folder_path
        self.tiff_path = folder_path
        self.read_shapes = {}
        self.shapes_path += '\\' + 'Shapes' + '\\'
        files_names = ['Files', 'Product', 'ShapeMetadata']
        for name in files_names:
            full_file_path = self.shapes_path + name
            if config.validate_ext_files_exists(full_file_path):
                self.read_shapes[name] = shp_to_geojson(full_file_path)
        self.created_json = self.make_full_json()

    def __call__(self, *args, **kwargs):
        return self.make_full_json()

    def create_origin_dir(self):
        """
        Function cuts the folder path and slices the last 2 names as required.
        :return: last 2 folders from the given path as string.
        """
        path_list = self.path.split('\\')[-2:]
        str_origin_dir = str(path_list[0]) + r'/' + str(path_list[1])
        return str_origin_dir

    def make_full_json(self):
        """
        The function creating full JSON with , Filenames + metadata + layPolygonParts JSON.
        :return: full JSON string.
        """
        full_json_str = {'fileNames': self.find_filenames(), 'metadata': self.create_metadata(),
                         'originDirectory': self.create_origin_dir()}
        # return json.dumps(full_json_str)
        return full_json_str

    def get_json_output(self):
        """
        This function encodes the full json with uft8 to be able show hebrew.
        :return: decoded json as string.
        """
        data = json.dumps(self.created_json, ensure_ascii=False).encode('utf8')
        decoded_data = data.decode()
        return decoded_data

    def bounding_box(self, points):
        """
        The function calculates bounding_box from the coordinates. XY - Min , XY - Max
        :param points: coordinates list
        :return: List of bounding box.
        """
        x_coordinates, y_coordinates = zip(*points)
        return [(min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))]

    def find_filenames(self):
        """
        This function find file names in "Files.shp" and appending tiff suffix to it and return a list of filenames.
        :return: Tiff file names.
        """
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
        """
        This function reads the metadata from ShapeMetadata and fills all the keys with the relevant values.
        :return: metadata JSON string.
        """
        # ToDo : Add / Check creationDate, ingestionDate, updateDate, sourceDateStart, sourceDateEnd
        try:
            metadata = {'type': config.METADATA_TYPE,
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
                        'accuracyCE90': int(self.read_shapes['ShapeMetadata']['features'][0]['properties']['Ep90']),
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
                                                           'coordinates'][0]]]},
                        'layerPolygonParts': self.read_shapes['ShapeMetadata']}
            bbox_list = self.bounding_box(
                [list(x) for x in self.read_shapes['Product']['features'][0]['geometry']['coordinates'][0]])
            del metadata['layerPolygonParts']['features'][0]['id']
            bbox_to_append = []
            for index in bbox_list:
                for tup_index in index:
                    bbox_to_append.append(tup_index)
            metadata['layerPolygonParts']['bbox'] = bbox_to_append
        except KeyError:
            raise Exception("Key not found in the ShapeMetadata")
        return metadata


if __name__ == '__main__':
    c = CreateJsonShape(r'D:\raster\shapes\1')
    try:
        with open(Path(Path(__file__).resolve()).parent.parent / 'jsons/shape_file.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(c.get_json_output()), f, ensure_ascii=False)
    except IOError:
        raise Exception("Cannot write json file")
    schema_validator.validate_json(c.get_json_output())
    # json_compare_pycsw()
