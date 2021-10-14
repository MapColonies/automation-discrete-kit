from pathlib import Path
from discrete_kit.validator import schema_validator
from discrete_kit.functions.shape_functions import *
import sys

_log = logging.getLogger('discrete_kit.app')

"""
This is an example of creating json from shape file.
"""

if __name__ == '__main__':

    # path_to_check = sys.argv[1] #ToDo : Added from CMD ?
    shape_json = [x[0] for x in os.walk(config.PATH_TO_CHECK)]
    shape_path = ("\n".join(s for s in shape_json if 'Shape'.lower() in s.lower()))
    shape_json = ShapeToJSON(shape_path)  # Created with None
    # c.add_ext_source_name(path_to_check, ".shp", True)
    print(shape_json.get_json_output())
    try:
        _log.info("Start Writing JSON to file")
        with open(Path(Path(__file__).resolve()).parent / 'jsons/shape_file.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(shape_json.get_json_output()), f, ensure_ascii=False)
    except IOError:
        _log.error("Cannot write json file")
        raise Exception("Cannot write json file")
    _log.info("End Writing JSON to file")
    schema_validator.validate_json_types(shape_json.get_json_output())
    # json_compare_pycsw()
