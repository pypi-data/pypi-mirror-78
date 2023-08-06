from .base import DBWorker
from YamlBase.yaml_worker import YamlDataBaseWorker
import os
import yaml
from YamlBase.sql import PostgreSQL


class PostgreWorker(DBWorker):
    tables: list
    schemas: list

    def __init__(self, yaml_db: YamlDataBaseWorker):
        super().__init__(yaml_db)
        self.db_data = yaml_db
        self.conn = self.initialize_connection()
        self.db_identifier = self.create_db_identifier()
        if not self.check_if_used():
            self.read_base_information_from_database()
            self.save_config()
        else:
            self.read_base_information_from_config(self.cache_folder + '/' + self.db_identifier + '.yaml')

    def check_if_used(self):
        return self.db_identifier + '.yaml' in os.listdir(self.cache_folder)

    def initialize_connection(self) -> PostgreSQL:
        return PostgreSQL(self.db_data.db_info['ip'], self.db_data.db_info['db_name'],
                          self.db_data.db_info['username'], self.db_data.db_info['password'])

    def insert_new_table(self, new_table):
        self.conn.create_table(new_table)
        self.tables = [i.table for i in self.conn.get_table_list()]
        self.save_config()

    def remove_table(self, table_obj):
        self.conn.remove_table(table_obj.schema_name, table_obj.table_name)
        self.tables = [i.table for i in self.conn.get_table_list()]
        self.save_config()

    def read_base_information_from_database(self):
        self.schemas = self.conn.get_schemas_list()
        self.tables = [i.table for i in self.conn.get_table_list()]

    def read_base_information_from_config(self, cfg_path):
        with open(cfg_path, 'r') as f:
            cfg = yaml.load(f, yaml.Loader)
        self.schemas = list(cfg['schemas'].keys())
        self.tables = []
        for schema in self.schemas:
            for table in cfg['schemas'][schema]:
                self.tables.append(table['name'])

    def save_config(self):
        cfg = dict()
        cfg.update(self.db_data.db_info)

        cfg['schemas'] = {}
        for schema in self.conn.get_schemas_list():
            cfg['schemas'][schema] = []

        for table_schema in self.conn.get_table_list():
            table_data = self.conn.get_table_data(table_schema.schema, table_schema.table)
            cfg['schemas'][table_schema.schema].append(table_data)

        with open(self.cache_folder + '/' + self.db_identifier + '.yaml', 'w') as f:
            yaml.dump(cfg, f)

    def check_insert_table_possibility(self, new_table_name) -> bool:
        """
        :param new_table_name:name of new table
        :return: true if inserting is possible
        """
        # Check if table already exists
        for table in self.tables:
            if table == new_table_name:
                return False

        # Check if all tables that exists in base - defined in config
        for table in self.conn.get_table_schema_dict().values():
            if table not in [i.table_name for i in self.db_data.tables_info]:
                return False

        return True

    def check_remove_table_possibility(self, table_name_to_remove) -> bool:
        """
        :param table_name_to_remove: name of table to check
        :return: if table can be removed
        """
        return table_name_to_remove in [i.table for i in self.conn.get_table_list()]
