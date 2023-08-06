import delune
import os
from ..helpers import dpath
import codecs
import json

def __mount__ (app):
    @app.route ("", methods = ["GET"])
    @app.permission_required (["replica", "index"])
    def collections (was, alias = None, side_effect = ""):
        return was.API (collections = list (delune.status ().keys ()))

    @app.route ("/<alias>", methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    @app.permission_required (["replica", "index"])
    def collections2 (was, alias, side_effect = ""):
        fn = dpath.getdir ("config", alias)
        if was.request.method == "GET":
            if not delune.get (alias):
                return was.Fault ("404 Not Found", "resource %s not exist" % alias, 40401)
            status = delune.status (alias)
            conf = dpath.getdir ("config", alias)
            if not os.path.isfile (conf):
                return was.Fault ("404 Not Found", "resource not exist", 40401)
            with codecs.open (conf, "r", "utf8") as f:
                colopt = json.loads (f.read ())
                status ['colopt'] = {
                    'data': colopt,
                    'mtime': os.path.getmtime (conf),
                    'size': os.path.getsize (conf),
                    'path': conf
                }
            return was.API (status)

        if was.request.method == "DELETE":
            if not os.path.isfile (fn):
                return was.Fault ("404 Not Found", "resource not exist", 40401)
            a, b = os.path.split (fn)
            if side_effect.find ("data") != -1:
                newfn = os.path.join (a, "-" + b)
            else:
                newfn = os.path.join (a, "#" + b)
            if os.path.isfile (newfn):
                os.remove (newfn)
            os.rename (fn, newfn)
            was.setlu (delune.SIG_UPD)
            if side_effect.find ("now") != -1:
                delune.close (alias)
                return was.API ("204 No Content")
            return was.API ("202 Accepted")

        if was.request.method == "POST" and delune.get (alias):
            return was.Fault ("406 Conflict", "resource already exists", 40601)

        elif was.request.method in ("PUT", "PATCH") and not delune.get (alias):
            return was.Fault ("404 Not Found", "resource not exist", 40401)

        if was.request.method == "PATCH":
            with open (fn) as f:
                config = json.load (f)
            data = was.request.JSON
            section = data ["section"]
            for k, v in data ["data"].items ():
                if k not in config [section]:
                    return was.Fault ("400 Bad Request", "{} is not propety of {}".format (k, section), 40001)
                config [section][k] = v
        else:
            config = was.request.JSON

        with open (fn, "w") as f:
            json.dump (config, f)

        was.setlu (delune.SIG_UPD)
        if was.request.method == "POST":
            if side_effect == "now":
                dpath.load_data (alias, app.config.numthreads, was.plock)
                return was.API ("201 Created", **config)
            return was.API ("202 Accepted", **config)
        return was.API (**config)
