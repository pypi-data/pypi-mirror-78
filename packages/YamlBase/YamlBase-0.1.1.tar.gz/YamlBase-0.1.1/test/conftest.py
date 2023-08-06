from __future__ import absolute_import

import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

import YamlBase

if os.path.exists('./test/test_db'):
    os.remove('./test/test_db')

sqlite3.connect('./test/test_db')