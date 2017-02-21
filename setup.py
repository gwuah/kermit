from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True }},
	windows = [{
            "script":"kermit.py",
            "icon_resources": [(1, "kermit.ico")],
            "dest_base":"kermit"
            }],
    zipfile = None,
)
