# coding=utf-8
"""
Setup file to freeze the application to a single exe

Run the build process by entering 'setup.py py2exe' or
'python setup.py py2exe' in a console prompt.
"""
import os
import shutil
import sys
import traceback
from distutils.core import setup
from warnings import warn

import py2exe

from bin.convenience import find_substrings_in_list
from news import __version__, __description__, __author__, __name___

# noinspection PyStatementEffect
py2exe  # prevent cleanup

# paths required for freeze fixes
PYTHON_DDLS = find_substrings_in_list("DLLs", sys.path)[0]  # location of python DLLs directory
PYTHON_PYSIDE = os.path.join(find_substrings_in_list("site-packages", sys.path)[0], "PySide")  # location of pyside

# paths to fixed files
msvcp_dll = "freezefix/msvcp90.dll"
init_py = "freezefix/__init__.py"


def apply_dll_fix():
	"""
	Moves the msvcp90.dll from freezefix to the python DLLs folder
	"""
	if os.path.exists(PYTHON_DDLS):
		try:
			shutil.copy(msvcp_dll, PYTHON_DDLS)  # fix distutils not able to find msvcp90.DLL
			return
		except:
			traceback.print_exc()
	warn("Could not apply dll fix, freeze could fail")


def apply_pyside_fix():
	"""
	Moves the __init__.py from freezefix to the directory of the pyside module
	The new file fixes an error when running from a single exe
	"""
	if os.path.exists(PYTHON_PYSIDE):
		try:
			shutil.copy(init_py, PYTHON_PYSIDE)  # fix pyside crash when bundled to single file
			return
		except:
			traceback.print_exc()
	warn("Could not apply pyside fix, the execuatable will probably not work")


def clean():
	"""
	Cleans the dist directory
	"""
	try:
		shutil.rmtree("dist")
	except WindowsError as e:
		if e.args[0] == 3:  # path not found
			return True
		elif e.args[0] == 5:
			warn("Could not clean dist folder: Directory or file is in use")
			return False
		else:
			traceback.print_exc()
			return False
	return True


def tree(src):
	"""
	Generates a list of tupples containing the root directory and all of its members (root, member)

	:param src: root folder to traverse
	:type src: basestring
	:return: list of (root, meber) tupples
	:rtype: list
	"""
	files = [
		(root, [os.path.join(root, file) for file in files])
		for (root, dirs, files)
		in os.walk(os.path.normpath(src))
		]
	return files


if __name__ == '__main__':
	apply_dll_fix()
	apply_pyside_fix()

	if clean():
		data_files = tree("resources")
		data_files.extend(tree("ui"))

		sys.stdout.flush()
		setup(
			# The first three parameters are not required, if at least a
			# 'version' is given, then a versioninfo resource is built from
			# them and added to the executables.
			version=__version__,
			description=__description__,
			name=__name___,
			author=__author__,

			# targets to build
			console=[{
				"script": "news.py",
				"icon_resources": [(0, "resources/icon.ico")],
				"dest_base": __name___,  # resulting name of file
				"other_resources": [()]
			}],

			options={
				"py2exe": {
					"bundle_files": 1,
					"compressed": True,
					"skip_archive": 0
				}
			},
			zipfile=None,
			requires=['PySide', 'py2exe'],
			data_files=data_files
		)
