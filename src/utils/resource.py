import json

def to_resource(data) -> str:
    return json.dumps(data, ensure_ascii=False)
