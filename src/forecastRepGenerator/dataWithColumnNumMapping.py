import json
def generateDataWithColNoMapping():
    mapping = {}
    fname = "src/forecastRepGenerator/dataWithColumnNumMapping.json"
    with open(fname) as f:
        mapping = json.load(f)
        return mapping