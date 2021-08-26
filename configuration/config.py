from enum import Enum
import glob
import os
import datetime

files_extension_list = ['.cpg', '.dbf', '.prj', '.shp', '.shx']

metadata_type = 'RECORD_RASTER'


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
                                      '%d/%m/%Y').strftime('%Y-%d-%mT%H:%M:%S:%fZ')
