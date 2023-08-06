"""Custom classes to present table/column from config or table"""


from dataclasses import dataclass


@dataclass
class Column:
    """class to present column from config or table"""
    column_name: str
    column_type: str
    is_pk = bool
    is_sk = bool
    sk_link = str

    def __init__(self, column_name, column_type, is_pk, is_sk, sk_link=None):
        self.column_name = column_name
        self.column_type = column_type
        self.is_pk = is_pk
        self.is_sk = is_sk
        self.sk_link = sk_link

    def __str__(self):

        return f"column_name = {self.column_name}\ncolumn_type = {self.column_type}\n" \
               f"is_pk = {self.is_pk}\nis_sk = {self.is_sk}\nsk_link = {self.sk_link}"


@dataclass
class Table:
    """class to table column from config or table"""
    schema_name: str
    table_name: str
    columns: list
    permissions: dict

    def __eq__(self, other):
        return self.table_name == other.table_name and self.schema_name == other.schema_name and \
               all([i in other.columns for i in self.columns])
