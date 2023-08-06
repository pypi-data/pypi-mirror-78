import delune
import os
import json
import codecs

RESOURCE_DIR = None

def getdir (*d):
    global RESOURCE_DIR
    return os.path.join (RESOURCE_DIR, "delune", *d)

def normpath (path):
    if os.name == "nt":
        return path.replace ("/", "\\")
    return path.replace ("\\", "/")

def load_data (alias, numthreads, plock):
    with codecs.open (getdir ("config", alias), "r", "utf8") as f:
        colopt = json.loads (f.read ())
        colopt ['data_dir'] = [getdir ("collections", normpath(d)) for d in colopt ['data_dir']]

    name = "standard"
    if "name" in colopt ["analyzer"]:
        name = colopt ["analyzer"].get ("name")
        del colopt ["analyzer"]["name"]

    analyzer_class = delune.get_analyzer (name)
    try:
        colopt ["analyzer"].pop ("max_terms")
    except KeyError:
        pass
    analyzer = analyzer_class (8, numthreads, **colopt ["analyzer"])

    si = delune.collection (colopt ["data_dir"], delune.READ, analyzer, plock = plock, version = colopt.get ("version", 1))
    actor = si.get_searcher (**colopt.get ('searcher', {}))
    actor.create_queue ()
    delune.assign (alias, actor)