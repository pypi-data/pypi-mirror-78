import sys
from sqlalchemy import create_engine
import os

from YamlBase.sql import SQLite
from YamlBase.yaml_worker import YamlDataBaseWorker
import pytest


class TestSQLite:

    def setup(self):
        self.sqlite_connector = SQLite('', './test/test_db.db')
        self.cfg = YamlDataBaseWorker("./test/test_base.yml")

    def test_empty_base(self):
        """Check if base is empty"""
        assert not self.sqlite_connector.get_table_list()

    def test_add_remove_table(self):
        """Add and remove table to sqlite DB"""
        self.sqlite_connector.create_table(self.cfg.tables_info[0])
        assert len(self.sqlite_connector.get_table_list())
        self.sqlite_connector.remove_table('table1')
        assert not self.sqlite_connector.get_table_list()

    def test_get_table_data(self):

        self.sqlite_connector.create_table(self.cfg.tables_info[0])

        print(self.cfg.tables_info[0])

        assert self.sqlite_connector.get_table_data(self.cfg.tables_info[0].schema_name,
                                             self.cfg.tables_info[0].table_name)['name'] == self.cfg.tables_info[0].table_name

        self.sqlite_connector.remove_table(self.cfg.tables_info[0].table_name)

    def test_get_table_schema_dict(self):
        self.sqlite_connector.create_table(self.cfg.tables_info[0])

        assert self.sqlite_connector.get_table_schema_dict() == {'main': self.cfg.tables_info[0].table_name}

        self.sqlite_connector.remove_table(self.cfg.tables_info[0].table_name)
