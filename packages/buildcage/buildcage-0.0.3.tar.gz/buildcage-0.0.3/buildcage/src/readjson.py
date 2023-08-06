import json

# __all__=["ArgsFromJson"]

def ArgsFromJson(fname):
    '''
    :param fname: JSON file name
    :return: Json dict
    '''
    with open(fname,"r") as f:
        args=json.load(f)
    return args