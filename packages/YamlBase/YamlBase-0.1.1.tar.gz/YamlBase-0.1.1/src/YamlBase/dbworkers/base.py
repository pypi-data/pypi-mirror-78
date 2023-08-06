from YamlBase.sql import SQLite, SQL


class DBWorker:
    cache_folder = "YamlBaseCache"

    def __init__(self, yaml):
        pass

    def check_if_used(self):
        pass

    def initialize_connection(self) -> SQL:
        pass

    def read_base_information_from_database(self):
        pass

    def read_base_information_from_config(self, cfg_path):
        pass

    def check_base_updates(self):
        pass

    def remove_table(self, table_name):
        pass

    def insert_new_table(self, new_table):
        pass

    def save_config(self):
        pass

    def check_insert_table_possibility(self, new_table_name):
        pass

    def create_db_identifier(self) -> str:
        return f"{self.db_data.db_info['ip']}_{self.db_data.db_info['db_type']}_" \
                             f"{self.db_data.db_info['db_name']}".replace('/', '_').replace(':', '_')
