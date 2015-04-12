#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from earthporn import *
import json

LIMIT = 10 # change as needed
OUTFILE = "earthporn.json" # change as needed
json.dump(get_data(LIMIT), open(OUTFILE, "w"))
