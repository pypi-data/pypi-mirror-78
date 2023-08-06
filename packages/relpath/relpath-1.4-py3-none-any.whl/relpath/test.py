
# relpath

import sys
from __init__ import rel2abs

### How to use ###

# get the absolute path according to the relative path from this file
print("here: %s"%rel2abs("./"))
print("parent: %s"%rel2abs("../"))
