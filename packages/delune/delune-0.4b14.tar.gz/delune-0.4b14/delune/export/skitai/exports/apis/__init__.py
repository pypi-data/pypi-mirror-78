import delune
from . import collections, collection, documents
from ..helpers import dpath

def __setup__ (app, mntopt):
    app.mount ("/cols", collections, collection, documents)

def __mount__ (app):
    dpath.RESOURCE_DIR = app.config.resource_dir

    @app.route ("", methods = ["GET"])
    @app.permission_required (["replica", "index"])
    def delune_ (was):
        return was.response.API (
            mounted_dir = "@" + app.config.resource_dir.replace (was.env.get ("HOME", ""), ""),
            n_threads = app.config.numthreads
        )
