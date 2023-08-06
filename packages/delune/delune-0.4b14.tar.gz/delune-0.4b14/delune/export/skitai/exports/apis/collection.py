import delune
import os
from ..helpers.dpath import getdir

def __mount__ (app):
    # replica -------------------------------------------------------
    @app.route ("/<alias>/config", methods = ["GET"])
    @app.permission_required (["index", "replica"])
    def config (was, alias):
        fn = getdir ("config", alias)
        return was.response.file (fn, "application/json")

    @app.route ("/<alias>/locks", methods = ["GET"])
    @app.permission_required ("replica")
    def locks (was, alias):
        return was.API ({"locks": delune.get (alias).si.lock.locks ()})

    @app.route ("/<alias>/locks/<name>", methods = ["POST", "DELETE", "OPTIONS"])
    @app.permission_required ("replica")
    def lock (was, alias, name):
        if was.request.command == "post":
            delune.get (alias).si.lock.lock (name)
            return was.API ("201 Created")
        delune.get (alias).si.lock.unlock (name)
        return was.API ("205 No Content")

    @app.route ("/<alias>/commit", methods = ["POST"])
    @app.permission_required ("index")
    def commit (was, alias):
        delune.get (alias).queue.commit ()
        return was.API ("205 No Content")

    @app.route ("/<alias>/rollback", methods = ["POST"])
    @app.permission_required ("index")
    def rollback (was, alias):
        delune.get (alias).queue.rollback ()
        return was.API ("205 No Content")

    # utilities --------------------------------------------------------------

    @app.route ("/<alias>/stem", methods = ["GET", "POST", "OPTIONS"])
    def stem (was, alias, **args):
        q = args.get ("q")
        if not q:
            returnwas.Fault ("400 Bad Request", 'parameter q required', 40003)
        if isinstance (q, str):
            q = q.split (",")
        l = args.get ("lang", 'en')
        return was.API (dict ([(eq, " ".join (delune.stem (alias, eq, l))) for eq in q]))

    @app.route ("/<alias>/analyze", methods = ["GET", "POST", "OPTIONS"])
    def analyze (was, alias, **args):
        q = args.get ("q")
        if not q:
            return was.Fault ("400 Bad Request", 'parameter q required', 40003)
        l = args.get ("lang", 'en')
        return was.API (delune.analyze (alias, q, l))

    # utilities --------------------------------------------------------------

    @app.route ("/<alias>/devices/<group>/<fn>", methods = ["GET"])
    @app.permission_required ("replica")
    def getfile (was, alias, group, fn):
        s = delune.status (alias)
        if group == "primary":
            path = os.path.join (s ["indexdirs"][0], fn)
        else:
            path = os.path.join (s ["indexdirs"][0], group, fn)
        return was.response.file (path)

    @app.route ("/<alias>/devices/<group>/segments/<fn>", methods = ["GET"])
    @app.permission_required ("replica")
    def getsegfile (was, alias, group, fn):
        s = delune.status (alias)
        seg = fn.split (".") [0]
        if group == "primary":
            if seg not in s ["segmentsizes"]:
                return was.Fault ("404 Not Found", "resource not exist", 40401)
            path = os.path.join (s ["segmentsizes"][seg][0], fn)
        else:
            path = os.path.join (s ["indexdirs"][0], group, fn)
        return was.response.file (path)

