import json


def deserialize_python(value):
    try:
        return eval(value)
    except Exception:
        return value
    

async def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)