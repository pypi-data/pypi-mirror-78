import skitai
import delune
import sys, os
import atila
from skitai.corequest.dbi import cluster_manager

def __setup__ (pref):
	skitai.register_states (delune.SIG_UPD)
	assert pref.config.resource_dir
	pref.config.resource_dir = os.path.abspath (pref.config.resource_dir)
