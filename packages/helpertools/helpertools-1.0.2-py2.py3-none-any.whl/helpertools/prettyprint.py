import json


def prettyprint(object):
    if(isinstance(object, str)):
        print(json.dumps(json.loads(object), indent=2))
    else:
        print(json.dumps(object, indent=2))









