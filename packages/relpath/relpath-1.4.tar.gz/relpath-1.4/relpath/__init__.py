
# relpath

import sys
import pathlib
import inspect

# get the absolute path according to the relative path from this file
def rel2abs(relative_path):
	# Getting the call stack
	stack = inspect.stack()
	# Get the caller's location
	python_file_path = stack[1].filename
	# Raise exception if the caller is not a file
	if python_file_path == "<stdin>": raise Exception("[relpath error] This module must be called from a python file. (Don't call this module from a place where the script is not located in a particular file, such as a shell.) This is because it is a module to handle paths relative to the location of the python file.")
	# Combining Paths
	comb_rel_path = python_file_path + "/../" + relative_path
	# Conversion to absolute path
	p = pathlib.Path(comb_rel_path)
	return str(p.resolve())
