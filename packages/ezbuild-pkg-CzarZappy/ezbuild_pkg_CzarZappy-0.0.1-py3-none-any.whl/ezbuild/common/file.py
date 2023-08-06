import json

import yaml


def load_yaml(file):
    with open(file) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_config(file):
    with open(file) as f:
        return json.load(f)