import sys
from cx_Freeze import setup, Executable

include_files = []
includes = []
excludes = ['Tkinter']
packages = [ "lxml", 'lxml.etree', 'lxml._elementpath', "docx", "inspect"]

build_exe_options = {
    "includes": includes,
    "excludes": excludes,
    "packages": packages,
    "include_files": include_files,
    "create_shared_zip": False}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

setup(  name = "tsDocxUpdater",
        version = "0.1",
        description = "Update a ts file with info forma a docx file!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("tsDocxUpdater.py", base=base)])