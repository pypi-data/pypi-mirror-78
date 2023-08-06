"""module for working with yaml config"""

from os import path
from .exceptions import FileReadError, FieldNotFoundError, ActionConfigSyntaxError
import yaml
from .table_representation import Column, Table


class YamlDataBaseWorker:
    """Class checks if data in YAML are correct and then parse it"""

    lvl1_fields_required = ['db_type', 'ip', 'username', 'password', 'db_name']

    def __init__(self, filepath: str):
        self.base_config = self._read_yaml_base_config(filepath)
        self._check_syntax()
        self.db_info, self.tables_info = self._parse_yaml()

    @staticmethod
    def _read_yaml_base_config(filepath: str):
        """
        :param filepath:
        :return:
        """
        if path.exists(filepath):

            try:
                with open(filepath) as file_thread:
                    return yaml.load(file_thread, Loader=yaml.Loader)

            except Exception:
                raise FileReadError(filepath)

        else:
            raise FileNotFoundError(f"File {filepath} not found")

    def _check_syntax(self):

        # Check if lvl_1 fields defined in config
        if not len(
                list(set(self.base_config.keys()) & set(self.lvl1_fields_required))
        ) == len(self.lvl1_fields_required):

            for field in self.lvl1_fields_required:
                if field not in list(self.base_config.keys()):
                    raise FieldNotFoundError(field)

        # Check for errors in schemas input
        if not len(list(self.base_config['schemas'])):
            raise ValueError("Schemas are empty")

        for schema in self.base_config['schemas']:
            if not len(list(self.base_config['schemas'][schema])):
                raise ValueError(f"Schema {schema} is empty")

    def _parse_yaml(self) -> (dict, dict):
        conf_dict = {}

        for field in self.lvl1_fields_required:
            conf_dict[field] = self.base_config[field]

        schemas_info = self.base_config['schemas']

        tables = []

        for schema in schemas_info:

            for table in list(self.base_config['schemas'][schema]):

                columns = []

                for col in list(self.base_config['schemas'][schema][table]['columns']):

                    is_pk = self.base_config['schemas'][schema][table]['columns'][col]['is_pk'] == 1

                    is_sk = self.base_config['schemas'][schema][table]['columns'][col]['is_sk'] == 1
                    sk_link = None

                    if is_sk:
                        sk_link = self.base_config['schemas'][schema][table]['columns'][col]['link']

                    columns.append(
                        Column(
                            self.base_config['schemas'][schema][table]['columns'][col]['name'],
                            self.base_config['schemas'][schema][table]['columns'][col]['type'],
                            is_pk,
                            is_sk,
                            sk_link
                        )
                    )

                permissions = self.base_config['schemas'][schema][table]['permissions']

                tables.append(Table(
                    schema, self.base_config['schemas'][schema][table]['name'], columns, permissions
                ))

        return conf_dict, tables


class YamlActionsWorker:

    allowed_actions = ['insert', 'remove', 'init']

    def __init__(self, filepath: str):
        filepath = filepath.replace('/', '') if filepath[0] == '/' else filepath
        self.action_table = self.read_yaml(filepath + '_actions.yaml')
        if not self.check_syntax():
            raise ActionConfigSyntaxError

    @staticmethod
    def read_yaml(filepath):
        """
                :param filepath:
                :return:
                """
        if path.exists(filepath):

            try:
                with open(filepath) as file_thread:
                    return yaml.load(file_thread, Loader=yaml.Loader)

            except Exception:
                raise FileReadError(filepath)

        else:
            raise FileNotFoundError(f"File {filepath} not found")

    def check_syntax(self):
        return all([i in self.allowed_actions for i in self.action_table.values()])
