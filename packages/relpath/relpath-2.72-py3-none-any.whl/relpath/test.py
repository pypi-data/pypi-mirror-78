
# relpath

### How to use ###

from __init__ import add_import_path

# add import path to sys.path
add_import_path("../")

from relpath import rel2abs

# get the absolute path according to the relative path from this file
print("here: %s"%rel2abs("./"))
print("parent: %s"%rel2abs("../"))
