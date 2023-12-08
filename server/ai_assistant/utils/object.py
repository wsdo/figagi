from typing import Dict
class Object:
    pass

def copyDictToObj(dict: Dict, obj, skipNone = True):
    for key, value in dict.items():
        if ((not hasattr(obj, key)) or (skipNone and not value)):
            continue
        setattr(obj, key, value)

def copyObjToObj(src: object, dst, skipNone = True):
    copyDictToObj(src.__dict__, dst, skipNone=skipNone) 