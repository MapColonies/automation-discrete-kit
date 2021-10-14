import os
import json
import logging
from jsonschema import *

import discrete_kit
_log = logging.getLogger('discrete_kit.validator.schema_validator')

def validate_json_types(received_json=None):
    _log.info("Starting validate Shape JSON")
    if received_json:
        if type(json.loads(received_json)) is dict:
            dir_name = os.path.dirname(__file__)
            full_path = os.path.join(dir_name, discrete_kit.configuration.config.SCHEMA_FOLDER,
                                     discrete_kit.configuration.config.JSON_NAME)
            try:
                with open(full_path, 'r') as fp:
                    schema = json.load(fp)
                    try:
                        validate(instance=json.loads(received_json), schema=schema)
                        _log.info("End validate Shape JSON")
                    except ValidationError as e:
                        raise Exception(e.schema['error_msg'])

            except IOError:
                raise Exception("Cannot open schema")
        else:
            raise Exception("not a dictionary")
    else:
        raise Exception("received None")
