import json
import yaml

def read_json(uri):
    """Reads in a dictionary from a json file uri"""
    with open(uri, 'r') as f:
        return json.load(f)

def write_json(dict, uri):
    """Writes a json file from a dictionary"""
    json_obj = json.dumps(dict)

    with open(uri, 'w') as outf:
        outf.write(json_obj)

def read_yaml(uri):
    """Reads in a dictionary from a yaml file uri (dict version)"""
    with open(uri, 'r') as f:
        return yaml.safe_load(f)

def write_yaml(dict, uri):
    """Writes a yaml file from a dictionary"""
    with open(uri, 'w') as outf:
        yaml.dump(dict, outf)