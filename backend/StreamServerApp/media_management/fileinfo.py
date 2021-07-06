import os
import json


def createfileinfo(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)


def readfileinfo(path):
    data = []
    with open(path) as json_file:
        data = json.load(json_file)
    return data