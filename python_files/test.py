import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.Room
room = db.OneRoom
import json
# -*- coding: utf-8 -*-

import js2py
js2py.translate_file('../static/js/json.js', '../static/js/testing.py')