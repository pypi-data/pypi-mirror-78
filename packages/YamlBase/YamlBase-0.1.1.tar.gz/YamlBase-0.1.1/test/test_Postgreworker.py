import sys
from sqlalchemy import create_engine

from YamlBase.dbworkers import PostgreWorker
from YamlBase.yaml_worker import YamlDataBaseWorker
import pytest


class TestPostgreWorker:

    def setup(self):
        self.cfg = YamlDataBaseWorker("./test/test_base_postgre.yml")
        self.postgre_connector = PostgreWorker(self.cfg)

    def test_remove_tables(self):
        self.postgre_connector.insert_new_table(self.cfg.tables_info[0])

        self.postgre_connector.remove_table(self.cfg.tables_info[0])

        assert not self.postgre_connector.tables

    def test_insert_new_tables(self):
        self.postgre_connector.insert_new_table(self.cfg.tables_info[0])
        assert set(self.postgre_connector.tables) <= set([i.table_name for i in self.cfg.tables_info])

        self.postgre_connector.remove_table(self.cfg.tables_info[0])

    def test_check_insert_table_possibility(self):
        self.postgre_connector.insert_new_table(self.cfg.tables_info[0])

        # Not to insert table that already exists
        assert not self.postgre_connector.check_insert_table_possibility(self.cfg.tables_info[0].table_name)

        assert self.postgre_connector.check_insert_table_possibility("test_name")

        self.postgre_connector.remove_table(self.cfg.tables_info[0])

    def test_check_remove_table_possibility(self):
        self.postgre_connector.insert_new_table(self.cfg.tables_info[0])

        # Not to insert table that already exists
        assert self.postgre_connector.check_remove_table_possibility(self.cfg.tables_info[0].table_name)

        assert not self.postgre_connector.check_remove_table_possibility("test_name")

        self.postgre_connector.remove_table(self.cfg.tables_info[0])

    def test_read_base_information_from_database(self):
        self.postgre_connector.insert_new_table(self.cfg.tables_info[0])
        self.postgre_connector.read_base_information_from_database()

        assert set(self.postgre_connector.schemas) == {'pg_catalog', 'information_schema', 'public'}
        assert self.cfg.tables_info[0].table_name in self.postgre_connector.tables

        self.postgre_connector.remove_table(self.cfg.tables_info[0])

    def test_save_config(self):

        self.postgre_connector.insert_new_table(self.cfg.tables_info[0])

        self.postgre_connector.read_base_information_from_config('YamlBaseCache/ec2-54-228-250-82.eu-west-1.compute.'
                                                                 'amazonaws.com_5432_SQLite_d5h3q2hrorhk5d.yaml')

        assert len(self.postgre_connector.tables) == 1
        assert len(self.postgre_connector.schemas) == 3
        # assert self.postgre_connector.tables[0] == 'table1'
        assert 'public' in self.postgre_connector.schemas

        self.postgre_connector.insert_new_table(self.cfg.tables_info[1])

        assert len(self.postgre_connector.tables) == 2
        assert 'table2' in self.postgre_connector.tables

        self.postgre_connector.remove_table(self.cfg.tables_info[0])
        self.postgre_connector.remove_table(self.cfg.tables_info[1])

        assert len(self.postgre_connector.tables) == 0

    def test_read_base_information_from_config(self):
        self.postgre_connector.insert_new_table(self.cfg.tables_info[0])
        self.postgre_connector.insert_new_table(self.cfg.tables_info[1])

        # Clear old data
        self.postgre_connector.tables = []
        self.postgre_connector.schemas = []

        self.postgre_connector.read_base_information_from_config('YamlBaseCache/ec2-54-228-250-82.eu-west-1.compute.'
                                                                 'amazonaws.com_5432_SQLite_d5h3q2hrorhk5d.yaml')

        assert len(self.postgre_connector.tables) == 2
        assert len(self.postgre_connector.schemas) == 3

        assert 'table1' in self.postgre_connector.tables and 'table2' in self.postgre_connector.tables

        assert 'public' in self.postgre_connector.schemas

        self.postgre_connector.remove_table(self.cfg.tables_info[0])
        self.postgre_connector.remove_table(self.cfg.tables_info[1])
