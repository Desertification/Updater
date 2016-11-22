import os
import sys
import traceback
from distutils.core import setup
import py2exe
import shutil

# noinspection PyStatementEffect
py2exe  # prevent cleanup

# paths required for freeze fixes
PYTHON_INSTALLATION = os.path.dirname(sys.executable)
PYTHON_DDLS = os.path.join(PYTHON_INSTALLATION, "/DLLs")
PYTHON_PYSIDE = os.path.join(PYTHON_INSTALLATION, "/Lib/site-packages/PySide")


def apply_fixes():
    if os.path.exists(PYTHON_DDLS):
        try:
            shutil.copy("freezefix/msvcp90.dll", PYTHON_DDLS)  # fix distutils not able to find msvcp90.DLL
        except:
            traceback.print_exc()
            pass

    if os.path.exists(PYTHON_PYSIDE):
        try:
            shutil.copy("freezefix/__init__.py", PYTHON_DDLS)  # fix pyside crash when bundled to single file
        except:
            traceback.print_exc()
            pass


def clean():
    try:
        shutil.rmtree("dist")
    except:
        traceback.print_exc()
        return False

    return True

apply_fixes()

if clean():
    setup(
        # The first three parameters are not required, if at least a
        # 'version' is given, then a versioninfo resource is built from
        # them and added to the executables.
        version="0.0.0",
        description="news",
        name="news",
        # targets to build
        console=["news.py"],

        options={
            "py2exe": {
                "bundle_files": 1,
                # "compressed": 1,
            }

        },
        zipfile=None,
        requires=['PySide']
    )
