import json
import os


def read_response(filename) -> dict:
    filename = os.path.join('tests', 'responses', filename)
    with open(filename) as f:
        return json.loads(f.read())
