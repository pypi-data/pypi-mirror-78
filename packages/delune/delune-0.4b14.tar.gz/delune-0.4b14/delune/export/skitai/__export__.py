# 2017. 3. 13 by Hans Roh (hansroh@gmail.com)

from atila import Atila
import delune
from rs4 import pathtool
import os
import json
import codecs
import time
import shutil
import time
from exports import apis, admin
from exports.helpers import dpath

app = Atila (__name__)
app.last_maintern = time.time ()

app.mount ("/admin", admin)
app.mount ("/apis", apis)

@app.before_mount
def before_mount (wasc):
	app.config.numthreads = wasc.numthreads
	app.config.plock = wasc.get_lock (__name__)
	permission_check_handler = wasc.app.config.get ("permission_check_handler")
	if permission_check_handler:
		app.permission_check_handler (permission_check_handler)

	delune.configure (app.config.numthreads, wasc.logger.get ("app"), 16384, 128)
	pathtool.mkdir (dpath.getdir ("config"))

	for alias in os.listdir (dpath.getdir ("config")):
		if alias.startswith ("-"): # remove dropped col
			with app.config.plock:
				with codecs.open (dpath.getdir ("config", alias), "r", "utf8") as f:
					colopt = json.loads (f.read ())
				for d in [dpath.getdir ("collections", dpath.normpath(d)) for d in colopt ['data_dir']]:
					if os.path.isdir (d):
						shutil.rmtree (d)
				os.remove (dpath.getdir ("config", alias))
		elif alias.startswith ("#"): # unused col
			continue
		else:
			dpath.load_data (alias, app.config.numthreads, app.config.plock)
	app.store.set (delune.SIG_UPD, time.time ())

@app.umounted
def umounted (wasc):
	delune.shutdown ()

@app.before_request
def before_request (was):
	if was.request.args.get ('alias') and not (was.request.routed.__name__ == "collections2" and was.request.method == "POST"):
		alias = was.request.args.get ('alias')
		if not delune.get (alias):
			return was.response.Fault ("404 Not Found", 40401, "resource %s not exist" % alias)

@app.maintain (1, threading = False)
def maintain_collections (was, now, count):
	configs = os.listdir (dpath.getdir ("config"))
	for alias in configs:
		if os.path.getmtime (dpath.getdir ("config", alias)) <= app.store.get (delune.SIG_UPD, 0):
			continue
		delune.close (alias)
		dpath.load_data (alias, app.config.numthreads, app.config.plock)
		was.setlu (delune.SIG_UPD)
	if was.getlu (delune.SIG_UPD) <= app.store.get (delune.SIG_UPD):
		return

	was.log ('collection changed, maintern ({}th)...' .format (count))
	for alias in configs:
		if alias [0] in "#-" and delune.get (alias [1:]):
			delune.close (alias [1:])
		elif not delune.get (alias):
			dpath.load_data (alias, app.config.numthreads, app.config.plock)
	app.store.set (delune.SIG_UPD, was.getlu (delune.SIG_UPD))

@app.permission_check_handler
def permission_check_handler (was, perms):
	raddr = was.request.get_remote_addr ()
	if raddr == "127.0.0.1":
		return
	allowed = was.app.config.get ("ADMIN_IPS", {})
	if '*' in allowed:
		return
	if raddr in allowed:
		return
	raise was.Error ("403 Permission Denied")

#----------------------------------------------------------------------------

@app.route ("/status")
@app.permission_required (["index", "replica"])
def status (was):
	return was.status ()


