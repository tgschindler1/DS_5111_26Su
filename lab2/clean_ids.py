#!/usr/bin/env python3 

import sys
import re
import logging

logging.basicConfig(filename="pipeline_autid.log", level=logging.INFO)
pattern = r'^[A-Za-z0-9_-]+$'

try:
    for line in sys.stdin:
        id = line.strip()
        if len(id) == 11 and bool(re.match(pattern, id)) == True:
            print(id)
        else:  logging.error(f"{id} is not a valid ID")

except KeyboardInterrupt:
    pass
