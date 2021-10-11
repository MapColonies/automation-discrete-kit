import enum
import glob
import os
import datetime

files_extension_list = ['.cpg', '.dbf', '.prj', '.shp', '.shx']

METADATA_TYPE = 'RECORD_RASTER'
JSON_NAME = "metadata_schema.json"
SCHEMA_FOLDER = 'schema'


class EnvironmentTypes(enum.Enum):
    """
    Types of environment.
    """
    QA = 1
    DEV = 2
    PROD = 3


def validate_ext_files_exists(path):
    for ext in files_extension_list:
        if not glob.glob(path + ext):
            raise Exception("Missing filename {0}{1}".format(path, ext))
    return True


def get_tiff_basename(path):
    return ''.join(os.path.basename(item) for item in (glob.glob(path + '//t*')))


def get_folder_names(path):
    # glob.glob(path + '/*/')
    return


def convert_time_to_utc(received_time):
    return datetime.datetime.strptime(received_time,
                                      '%d/%m/%Y').strftime('%Y-%d-%mT%H:%M:%S.%f')[:-3] + 'Z'


def generate_datatime_zulu(current=True, time_dict=None):
    """
    generate current time on zulu format
    :param current: if curren=True (as default) will return current time, if False wil generate by time_dict
    :param time_dict: should be as example: {'year':2020, 'month':12, 'day':12, 'hour':12, 'minute':10,'second':10}
    """
    if current:
        res = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    elif time_dict:
        res = datetime.datetime(time_dict['year'], time_dict['month'], time_dict['day'], time_dict['hour'],
                                time_dict['minute'], time_dict['second']).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        raise ValueError("Should provide current=True param or time dictionary value")

    return res
