from pathlib import Path
from discrete_kit.validator import schema_validator
from discrete_kit.functions.shape_functions import *

_log = logging.getLogger('discrete_kit.app')

"""
This is an example of creating json from shape file.
"""
if __name__ == '__main__':
    path_to_check = r'/home/dimitry/Downloads/example-shps/3276'
    c = [x[0] for x in os.walk(path_to_check)]
    shape_path = ("\n".join(s for s in c if 'Shape'.lower() in s.lower()))
    c = CreateJsonShape(shape_path)  # Created with None
    #c.add_ext_source_name(path_to_check, ".shp", True)
    print(c.get_json_output())
    try:
        with open(Path(Path(__file__).resolve()).parent / 'jsons/shape_file.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(c.get_json_output()), f, ensure_ascii=False)
    except IOError:
        raise Exception("Cannot write json file")
    schema_validator.validate_json_types(c.get_json_output())
    # json_compare_pycsw()
