[![Python 3.6](https://img.shields.io/badge/python-3.6-green.svg)](https://www.python.org/downloads/release/python-360/)
<img alt="GitHub release (The latest by date including pre-releases)" src="https://img.shields.io/github/v/release/MapColonies/automation-discrete-kit">
# Automation-discrete-kit

## Description
This package provides multiple utilities for discrete manipulations , validation tools and functions.

### required files:
- `Shapes folder`

### Features included:
1. ShapeToJSON - creates JSON from read files to be compared later on.
2. Change resource name in shape file - metadata.
3. Change discrete resolution
4. JSONs validation
5. Config - contains file extensions , and useful function for the JSON creation.
6. Write JSON to file for validation.
7. Validation of the JSON schema.
8. Types Validations
9. Updating tfw resolution value - TBD

### Return options:
 - JSON - contains relevant fields filled with values.
 - JSON File.

### Usage:
1. import the package : `automation-discrete-kit`.
2. create `ShapeToJSON` contains the path for shape folder.
3. Use any function of the class `ShapeToJSON`
