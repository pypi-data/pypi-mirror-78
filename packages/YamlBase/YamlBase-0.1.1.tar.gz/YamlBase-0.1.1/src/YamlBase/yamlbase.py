"""Main file of YamlBase"""

import argparse
import yaml
import os
from YamlBase.ybase import YBase
import sys
import os


def main():

    parser = argparse.ArgumentParser(description='This utility allows you to manage changes to the database using '
                                                 'configurations')
    parser.add_argument('-cfg_db', action='store', dest='cfg_path',
                        help='Path to yaml file with DB config')

    args = parser.parse_args()
    base = YBase(args.cfg_path)
    base.do_actions()


if __name__ == '__main__':
    main()