from sqlalchemy import create_engine
import pandas as pd
from YamlBase.table_representation import Table
from .sql import SQL
from .sql import table_schema
from typing import List


class PostgreSQL(SQL):

    excluded_schemas = ['pg_catalog', 'information_schema']

    def __init__(self, host, db_name, user, password):
        super().__init__()
        self.conn = create_engine(f"postgresql://{user}:{password}@{host}/{db_name}")

    def get_schemas_list(self) -> list:
        tt = pd.read_sql("select schema_name from information_schema.schemata;", self.conn)
        return list(tt['schema_name'].unique())

    def get_table_list(self) -> List[table_schema]:
        temp = pd.read_sql("SELECT * FROM information_schema.tables", self.conn)
        temp = temp[~temp['table_schema'].isin(self.excluded_schemas)]
        result = []
        for table_name, schema_name in zip(temp['table_name'], temp['table_schema']):
            result.append(table_schema(table_name, schema_name))
        return result

    def create_schema(self, schema_name):
        self.conn.execute(f"create schema {schema_name}")

    def remove_schema(self, schema_name, cascade=False):
        if not cascade:
            self.conn.execute(f"drop schema {schema_name}")
        else:
            self.conn.execute(f"drop schema {schema_name} CASCADE")

    def create_table(self, table_data: Table, if_exists_check=False):
        query = f"CREATE TABLE {table_data.schema_name}.{table_data.table_name}"
        if if_exists_check:
            query += "IF NOT EXISTS"
        query += "("

        for col in table_data.columns:
            query += f"{col.column_name} {col.column_type}"
            if col.is_pk:
                query += " PRIMARY KEY"
            query += ","

        # Removing last comma
        query = query[:-1]

        query += ")"
        self.conn.execute(query)

    def remove_table(self, schema, table_name):
        query = f"DROP TABLE {schema}.{table_name}"
        self.conn.execute(query)

    def _get_pk_list(self, table_name, schema_name) -> list:
        query = f"""SELECT
              pg_attribute.attname,
              format_type(pg_attribute.atttypid, pg_attribute.atttypmod)
            FROM pg_index, pg_class, pg_attribute, pg_namespace
            WHERE
              pg_class.oid = '{table_name}'::regclass AND
              indrelid = pg_class.oid AND
              nspname = '{schema_name}' AND
              pg_class.relnamespace = pg_namespace.oid AND
              pg_attribute.attrelid = pg_class.oid AND
              pg_attribute.attnum = any(pg_index.indkey)"""
        # query = ''
        return list(pd.read_sql(query, self.conn)['attname'].values)

    def get_table_data(self, schema, table_name) -> dict:
        query = f"select * from information_schema.columns where table_schema = '{schema}' and table_name  = '{table_name}'"
        temp = pd.read_sql(query, self.conn)[['column_name', 'data_type', 'is_nullable']]
        pk_list = self._get_pk_list(table_name, schema)

        table_data = dict()
        table_data['name'] = table_name
        table_data['schema'] = schema
        table_data['permissions'] = []
        table_data['columns'] = {}

        for col in temp['column_name'].values:
            table_data['columns'][col] = {
                'name': col,
                # list() and type transform are necessary because values by default
                # returns np object and spoils yaml
                'type': str(list(temp[temp['column_name'] == col]['data_type'].values)[0]),
                'is_nullable': str(list(temp[temp['column_name'] == col]['is_nullable'].values)[0]),
                'is_pk': col in pk_list
            }
        return table_data

    def get_table_schema_dict(self):
        temp = pd.read_sql(f"select * from information_schema.tables", self.conn)[['table_schema', 'table_name']]
        temp = temp[temp['table_schema'] != 'pg_catalog']
        temp = temp[temp['table_schema'] != 'information_schema']
        return {k: v for k, v in zip(temp['table_schema'], temp['table_name'])}