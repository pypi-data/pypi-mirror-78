import os
import json

def dir_to_dict(path):
    """Get dictionary of directory strcuture where path
    is root node.
    
    :param path: Absolute path of root node
    :type path: str
    :returns: dictionary of all file inside the path
    :rtype: dict
    """
    try:
        d = {'name': os.path.basename(path)}
        if os.path.isdir(path):
            d['type'] = "directory"
            d['children'] = [dir_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
        else:
            d['type'] = "file"
        return d

    except Exception as e:
        print("Path error: "+e)
        return None