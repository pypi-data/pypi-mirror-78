from YamlBase.yaml_worker import YamlDataBaseWorker, YamlActionsWorker, ActionConfigSyntaxError
from YamlBase.exceptions import FieldNotFoundError
import pytest
import os
from YamlBase.table_representation import Table, Column


@pytest.fixture
def test_no_fields_folder():
    return "./test/configs_for_tests/test_no_fields/"


@pytest.fixture
def test_action_folder():
    return "./test/configs_for_tests/test_actions/"


@pytest.fixture
def correct_first_column_object():
    return Column(
        "column1",
        "text",
        1,
        0
    )


@pytest.fixture
def correct_second_column_object():
    return Column(
        "column2",
        "double",
        0,
        1,
        'table2'
    )


@pytest.fixture
def correct_third_column_object():
    return Column(
        "column3",
        "text",
        0,
        0
    )


@pytest.fixture
def correct_first_table_permissions():
    return {
        "usr1": "r*",
        "usr2": "w*"
    }


class TestYamlDatabaseWorker:

    def test_read_yaml_base_config_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            YamlDataBaseWorker('some_file.yaml')

    def test_read_yaml_base_config_field_not_found(self, test_no_fields_folder):

        for f in os.listdir(test_no_fields_folder):

            with pytest.raises(FieldNotFoundError):
                YamlDataBaseWorker(test_no_fields_folder + f)

    def test_parse_yaml(self, correct_first_column_object, correct_second_column_object,
                        correct_third_column_object, correct_first_table_permissions):

        obj = YamlDataBaseWorker('./test/test_base.yml')

        assert obj.tables_info[0].columns[0] == correct_first_column_object
        assert obj.tables_info[0].columns[1] == correct_second_column_object
        assert obj.tables_info[0].columns[2] == correct_third_column_object

        assert obj.tables_info[0].table_name == 'table1'
        assert obj.tables_info[0].permissions == correct_first_table_permissions


class TestYamlActionsWorker:

    def test_read_yaml_base_config_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            YamlActionsWorker('some_file.yaml')

    def test_data_parsing(self):
        obj = YamlActionsWorker('./test/test_db')
        assert obj.action_table == {
            "table1": "insert",
            "table2": "remove"
        }

    def test_check_syntax(self, test_action_folder):
        with pytest.raises(ActionConfigSyntaxError):
            YamlActionsWorker(test_action_folder + 'test_db')
