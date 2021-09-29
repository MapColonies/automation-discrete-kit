import os
import json

from jsonschema import *

import configuration.config


def validate_json_types(received_json=None):
    if received_json:
        if type(json.loads(received_json)) is dict:
            dir_name = os.path.dirname(__file__)
            full_path = os.path.join(dir_name, configuration.config.SCHEMA_FOLDER, configuration.config.JSON_NAME)
            try:
                with open(full_path, 'r') as fp:
                    schema = json.load(fp)
                    try:
                        validate(instance=json.loads(received_json), schema=schema)
                    except ValidationError as e:
                        raise Exception(e.schema['error_msg'])

            except IOError:
                raise Exception("Cannot open schema")
        else:
            raise Exception("not a dictionary")
    else:
        raise Exception("received None")
