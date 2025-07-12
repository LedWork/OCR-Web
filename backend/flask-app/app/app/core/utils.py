import json
from bson import json_util
from bson.objectid import ObjectId

# Global constants
EXPECTED_CHECKS_PER_CARD = 2

def parse_json(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
    return json.loads(json_util.dumps(data))
