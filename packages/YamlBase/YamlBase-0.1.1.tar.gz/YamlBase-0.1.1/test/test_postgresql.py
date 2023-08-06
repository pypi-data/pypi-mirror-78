import sys
from sqlalchemy import create_engine
import os
from YamlBase.sql import PostgreSQL
from YamlBase.yaml_worker import YamlDataBaseWorker
import pytest


class TestPostgreSQL:

    def setup(self):
        test_db_ip = 'ec2-54-228-250-82.eu-west-1.compute.amazonaws.com:5432'
        test_db = 'd5h3q2hrorhk5d'
        test_user = 'mzhrcgiqucfnxv'
        test_password = 'bba3716ee4b3af0bd724333fb22afed02d588371c149b5685f9f62e7e2029b24'

        self.postgresql_connector = PostgreSQL(test_db_ip, test_db, test_user, test_password)

        self.cfg = YamlDataBaseWorker("./test/test_base_postgre.yml")

    def test_empty_base(self):
        """Check if base is empty"""
        # If some test failed then it should be table in database
        if self.postgresql_connector.get_table_list():
            for table in self.postgresql_connector.get_table_list():
                self.postgresql_connector.remove_table(table.schema, table.table)
        assert not self.postgresql_connector.get_table_list()

    def test_add_remove_schema(self):
        assert set(self.postgresql_connector.get_schemas_list()) == {'public', 'pg_catalog', 'information_schema'}
        self.postgresql_connector.create_schema('test_schema')
        assert set(self.postgresql_connector.get_schemas_list()) == {'public', 'pg_catalog', 'information_schema',
                                                                     'test_schema'}
        self.postgresql_connector.remove_schema('test_schema')
        assert set(self.postgresql_connector.get_schemas_list()) == {'public', 'pg_catalog', 'information_schema'}

    def test_add_remove_table(self):
        """Add and remove table to sqlite DB"""
        self.postgresql_connector.create_table(self.cfg.tables_info[0])
        assert len(self.postgresql_connector.get_table_list())
        self.postgresql_connector.remove_table('public', 'table1')
        assert not self.postgresql_connector.get_table_list()

    def test_get_table_data(self):

        self.postgresql_connector.create_table(self.cfg.tables_info[0])

        table_data = self.postgresql_connector.get_table_data(self.cfg.tables_info[0].schema_name,
                                                              self.cfg.tables_info[0].table_name)
        assert table_data['name'] == self.cfg.tables_info[0].table_name
        assert table_data['schema'] == self.cfg.tables_info[0].schema_name

        self.postgresql_connector.remove_table(self.cfg.tables_info[0].schema_name, self.cfg.tables_info[0].table_name)

    def test_get_table_schema_dict(self):
        self.postgresql_connector.create_table(self.cfg.tables_info[0])

        assert self.postgresql_connector.get_table_schema_dict() == {self.cfg.tables_info[0].schema_name:
                                                                         self.cfg.tables_info[0].table_name}

        self.postgresql_connector.remove_table(self.cfg.tables_info[0].schema_name, self.cfg.tables_info[0].table_name)
