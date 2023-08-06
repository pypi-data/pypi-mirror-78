from sqlalchemy import create_engine
from YamlBase.table_representation import Table
from collections import namedtuple

table_schema = namedtuple('table_schema', ['table', 'schema'])


class SQL:

    def __init__(self):
        pass

    def get_schemas_list(self) -> list:
        pass

    def get_table_list(self) -> list:
        pass

    def add_column_to_table(self):
        pass

    def create_schema(self, schema_name):
        pass

    def create_table(self, table_data: Table, if_exists_check=False):
        pass

    def remove_table(self, table_name):
        pass

    def get_table_schema_dict(self):
        pass

    def get_table_data(self, schema, tablename):
        pass