import os
from functools import reduce
from collections import OrderedDict

from dipor.jinja.extensions import RoutesExtension

def get_structural_context(content_root):
    ctx = {}
    dir = {}
    rootdir = content_root.rstrip(os.sep)
    start = content_root.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = {}
        if '_branches' in folders:
            folders.remove('_branches')
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    processed_path = process_paths(dir)
    # html = __generate_routes(processed_path)
    return processed_path


def process_paths(dir, prefix="", is_subpath=False):
    for k, v in dir.items():
        if not v:
            dir[k] = (prefix+"/"+k, None)
        else:
            sub_paths = process_paths(v, prefix="/"+k, is_subpath=True)
            dir[k] =("/"+k, sub_paths)
    if is_subpath:
        return dir

    return dir

        