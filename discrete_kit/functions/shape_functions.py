import geopandas
import logging
from discrete_kit.configuration import config
import os
import json
import glob

_log = logging.getLogger('discrete_kit.shape_functions')


def shape_to_geojson(path):
    """
    This function reads shp files.
    :param path: path to to file with suffix shp
    :return: JSON string.
    """
    try:
        _log.info("Start converting shape file to JSON for : " + path)
        shp_file = geopandas.read_file(path + config.ExtensionTypes.SHAPE.value)
        # shp_file = geopandas.read_file(path + '.shp')
        geo_json = shp_file._to_geo()
    except Exception as err:
        _log.error(str(err))
        raise Exception(str(err))
    _log.info("End convert shape file to JSON for : " + path)
    return geo_json


class ShapeToJSON:
    def __init__(self, folder_path):
        _log.info("Start Shape to JSON class creation")
        # shape_json = [x[0] for x in os.walk(folder_path)]
        # folder_path = ("\n".join(s for s in shape_json if 'Shape'.lower() in s.lower()))
        self.path = folder_path
        self.shapes_path = folder_path
        self.tiff_path = folder_path
        self.read_shapes = {}

        for name in config.files_names:
            _log.info("Looping : " + name)
            full_file_path = os.path.join(self.shapes_path, name)
            # if config.validate_ext_files_exists(full_file_path):
            self.read_shapes[name] = shape_to_geojson(full_file_path)
        current_time_str = config.generate_datatime_zulu().replace('-', '_').replace(':', '_')
        # self.add_ext_source_name(full_file_path + '.shp', current_time_str, True)
        _log.info("End looping")
        _log.info("End Shape to JSON class")
        self.created_json = self.make_full_json()

    def __call__(self, *args, **kwargs):
        return self.make_full_json()

    # ToDo :
    def create_origin_dir(self):
        """
        Function cuts the folder path and slices the last 2 names as required.
        :return: last 2 folders from the given path as string.
        """
        _log.info("Start collecting origin directory")
        if os.uname().sysname == config.OSName.LINUX.value:
            path_list = self.path.split('/')[-2:]
            str_origin_dir = str(path_list[0]) + r'/' + str(path_list[1])
        else:
            path_list = self.path.split('\\')[-2:]
            str_origin_dir = str(path_list[0]) + r'/' + str(path_list[1])
        _log.info("End collecting origin directory")
        return str_origin_dir

    def add_ext_source_name(self, shape_file, ext, new_name=False):
        """
        will update shapefile source name
        :param shape_file: original metadata shape file
        :param ext: extension to original name
        :param new_name: if True -> will set ext as entire name
        :return: new rendered name [str]
        """
        _log.info("Start adding extension to source name")
        shp_file = geopandas.read_file(shape_file)
        if new_name:
            source_new_name = ext
        else:
            source_new_name = "_".join([ext, shp_file.Source[0]])
        # shp_file.Source[0] = source_new_name
        shp_file.Source.update(source_new_name)
        shp_file.to_file(shape_file, encoding='utf-8')
        _log.info("End adding extension to source name")
        return source_new_name

    def make_full_json(self):
        """
        The function creating full JSON with , Filenames + metadata + layPolygonParts JSON.
        :return: full JSON string.
        """
        _log.info("Start creating full json")
        full_json_str = {'fileNames': self.find_filenames(), 'metadata': self.create_metadata(),
                         'originDirectory': self.create_origin_dir()}
        # return json.dumps(full_json_str)
        _log.info("End creating full json")
        return full_json_str

    def get_json_output(self):
        """
        This function encodes the full json with uft8 to be able show hebrew.
        :return: decoded json as string.
        """
        _log.info("Start returning json output")
        data = json.dumps(self.created_json, ensure_ascii=False).encode('utf8')
        decoded_data = data.decode()
        _log.info("End returning json output")
        return decoded_data

    def calculate_bounding_box(self, points):
        """
        The function calculates bounding_box from the coordinates. XY - Min , XY - Max
        :param points: coordinates list
        :return: List of bounding box.
        """
        _log.info("Start Calculating bounding box")
        x_coordinates, y_coordinates = zip(*points)
        return [(min(x_coordinates), min(y_coordinates)), (max(x_coordinates), max(y_coordinates))]

    def load_resolution_from_tfw(self):
        _log.info("Start reading maxResolution from twf")
        abs_path = os.path.abspath(os.path.join(self.path, os.pardir, os.pardir))
        tfw_file = glob.glob(abs_path + "/**/*" + config.ExtensionTypes.TFW.value, recursive=True)[0]
        try:
            f = open(tfw_file)
        except IOError:
            _log.error('Failed to load tfw on following path : ' + tfw_file)
            raise Exception('Failed to load tfw on following path : ' + tfw_file)
        else:
            with f:
                resolution_num = f.readline()
        _log.info("End reading maxResolution from twf")
        return resolution_num

    def find_filenames(self):
        """
        This function find file names in "Files.shp" and appending tiff suffix to it and return a list of filenames.
        :return: Tiff file names.
        """
        _log.info("Start collecting file names")
        filenames_list = []
        try:
            shapes = self.read_shapes['Files']['features']
        except KeyError:
            _log.error("Key not found in the Files")
            raise Exception("Key not found in the Files")
        for shape in shapes:
            filenames_list.append(
                config.get_tiff_basename(self.path) + '/' + shape['properties']['File Name'] + '.tiff')
        _log.info("End collecting file names")
        return filenames_list

    def create_metadata(self):
        """
        This function reads the metadata from ShapeMetadata and fills all the keys with the relevant values.
        :return: metadata JSON string.
        """
        _log.info("Start collecting metadata for the json")
        # ToDo : Add / Check creationDate, ingestionDate, updateDate, sourceDateStart, sourceDateEnd
        # ToDo : add  producerName , classification - how to calculate

        ### self.read_shapes['ShapeMetadata']['features'][0]['properties']['Cities']
        ### self.read_shapes['ShapeMetadata']['features'][0]['properties']['Countries']
        try:
            metadata = {'type': config.METADATA_TYPE,
                        'productName': self.read_shapes['ShapeMetadata']['features'][0]['properties']['SourceName'],
                        'region': self.read_shapes['ShapeMetadata']['features'][0]['properties']['Countries'],
                        'producerName': 'undefined',
                        'classification': '9999999999999',
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
                        'sensorType': ['UNDEFINED'],
                        'rms': self.read_shapes['ShapeMetadata']['features'][0]['properties']['Rms'],
                        'scale': self.read_shapes['ShapeMetadata']['features'][0]['properties']['Scale'],
                        # 'sensorType': [self.read_shapes['ShapeMetadata']['features'][0]['properties']['SensorType']],
                        'productId':
                            self.read_shapes['ShapeMetadata']['features'][0]['properties']['Source'].split('-')[0],
                        'productVersion':
                            self.read_shapes['ShapeMetadata']['features'][0]['properties']['Source'].split('-')[1],
                        'productType': self.read_shapes['Product']['features'][0]['properties']['Type'],
                        'resolution': format(float(self.load_resolution_from_tfw()), '.10f'),
                        'maxResolutionMeter': float(
                            self.read_shapes['Product']['features'][0]['properties']['Resolution']),
                        'footprint': {'type': self.read_shapes['Product']['features'][0]['geometry']['type'],
                                      'coordinates': [[list(x) for x in
                                                       self.read_shapes['Product']['features'][0]['geometry'][
                                                           'coordinates'][0]]]},
                        'srsName': 'undefined',
                        'srsId': 'undefined',
                        'layerPolygonParts': self.read_shapes['ShapeMetadata'],
                        'includedInBests': 'undefined',
                        'productBoundingBox': 'undefined'}
            bbox_list = self.calculate_bounding_box(
                [list(x) for x in self.read_shapes['Product']['features'][0]['geometry']['coordinates'][0]])
            _log.info("End calculating bounding box")
            del metadata['layerPolygonParts']['features'][0]['id']
            bbox_to_append = []
            for index in bbox_list:
                for tup_index in index:
                    bbox_to_append.append(tup_index)
            metadata['layerPolygonParts']['bbox'] = bbox_to_append
        except KeyError:
            _log.error("Key not found in the ShapeMetadata")
            raise Exception("Key not found in the ShapeMetadata")
        if metadata['rms'] is None:
            metadata['rms'] = 'undefined'
        if metadata['scale'] is None:
            metadata['scale'] = 'undefined'
        # metadata['rms'] = 'hara'
        _log.info("End collecting metadata for the json")
        return metadata
