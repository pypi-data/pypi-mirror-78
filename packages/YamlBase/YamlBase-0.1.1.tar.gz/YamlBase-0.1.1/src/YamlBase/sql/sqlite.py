from sqlalchemy import create_engine
import pandas as pd
from YamlBase.table_representation import Table
from .sql import SQL
from .sql import table_schema
from typing import List


class SQLite(SQL):

    def __init__(self, host, db_name):
        super().__init__()
        self.conn = create_engine(f"sqlite:///{host}{db_name}")

    def get_schemas_list(self) -> list:
        return ['main']

    def get_table_list(self) -> List[table_schema]:
        temp = pd.read_sql("SELECT * FROM sqlite_master", self.conn)
        result = []
        for table_name in list(temp['name']):
            result.append(table_schema(table_name, 'main'))
        return result

    def create_schema(self, schema_name):
        self.conn.execute(f"attach {schema_name} as 'schemaname'")

    def create_table(self, table_data: Table, if_exists_check=False):
        query = f"CREATE TABLE {table_data.table_name}"
        if if_exists_check:
            query += "IF NOT EXISTS"
        query += "("

        for col in table_data.columns:
            query += f"{col.column_name} {col.column_type},"

        # Removing last comma
        query = query[:-1]

        query += ")"
        self.conn.execute(query)

    def remove_table(self, table_name):
        query = f"DROP TABLE {table_name}"
        self.conn.execute(query)

    def get_table_schema_dict(self):
        temp = pd.read_sql("SELECT * FROM sqlite_master", self.conn)
        return {'main': v for v in temp['name']}

    def get_table_data(self, schema, tablename) -> dict:
        temp = pd.read_sql(f"PRAGMA table_info({tablename});", self.conn)[['name', 'type', 'pk']]

        table_data = dict()
        table_data['name'] = tablename
        table_data['permissions'] = []
        table_data['columns'] = {}

        for col in temp['name'].values:
            table_data['columns'][col] = {
                'name': col,
                # list() and type transform are necessary because values by default
                # returns np object and spoils yaml
                'type': str(list(temp[temp['name'] == col]['type'].values)[0]),
                'is_pk': int(list(temp[temp['name'] == col]['pk'].values)[0])
            }

        return table_data
