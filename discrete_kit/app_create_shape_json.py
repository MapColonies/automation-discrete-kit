import json
import logging
from pathlib import Path
from discrete_kit.validator import schema_validator
from discrete_kit.functions.shape_functions import *

_log = logging.getLogger('discrete_kit.app')

"""
This is an example of creating json from shape file.
"""
if __name__ == '__main__':
    c = CreateJsonShape(r'/home/dimitry/Downloads/2021-2686-0')  # Created with None
    print(c.get_json_output())
    # try:
    #     with open(Path(Path(__file__).resolve()).parent.parent / 'jsons/shape_file.json', 'w', encoding='utf-8') as f:
    #         json.dump(json.loads(c.get_json_output()), f, ensure_ascii=False)
    # except IOError:
    #     raise Exception("Cannot write json file")
    # schema_validator.validate_json_types(c.get_json_output())
    # json_compare_pycsw()