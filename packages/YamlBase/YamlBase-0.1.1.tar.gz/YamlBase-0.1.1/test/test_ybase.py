from YamlBase import YBase
import pytest
from YamlBase.dbworkers import SQLiteWorker
from YamlBase import ActionNotFound
from YamlBase import DataBaseTypeNotFound
from YamlBase import InsertActionImpossibleError, RemoveActionImpossibleError


class TestYBase:

    def test_initialize_sqlite_worker(self):
        obj = YBase('./test/test_base.yml')
        assert isinstance(obj.db_worker, SQLiteWorker)

        with pytest.raises(FileNotFoundError):
            YBase('randomfile.yaml')

        with pytest.raises(DataBaseTypeNotFound):
            YBase('test/configs_for_tests/test_ybase/test_miss_db_type.yml')

    def test_filter_table_by_tablename(self):
        obj = YBase('./test/test_base.yml')
        assert obj._filter_table_by_tablename('table1') == obj.yaml_config.tables_info[0]

    def test_insert_remove_action(self):
        obj = YBase('./test/test_base.yml')
        # Check for empty database
        assert not obj.db_worker.tables

        obj.insert_action(obj.yaml_config.tables_info[0])

        with pytest.raises(InsertActionImpossibleError):
            obj.insert_action(obj.yaml_config.tables_info[0])

        assert obj.db_worker.tables[0] == obj.yaml_config.tables_info[0].table_name

        obj.remove_action(obj.yaml_config.tables_info[0])

        with pytest.raises(RemoveActionImpossibleError):
            obj.remove_action(obj.yaml_config.tables_info[0])

        assert not obj.db_worker.tables

    def test_check_action_possibility(self):
        obj = YBase('./test/test_base.yml')

        assert not obj.check_action_possibility('remove', obj.yaml_config.tables_info[0])
        assert obj.check_action_possibility('insert', obj.yaml_config.tables_info[0])

        obj.insert_action(obj.yaml_config.tables_info[0])

        assert obj.check_action_possibility('remove', obj.yaml_config.tables_info[0])
        assert not obj.check_action_possibility('insert', obj.yaml_config.tables_info[0])

        obj.remove_action(obj.yaml_config.tables_info[0])

    def test_do_actions(self, capsys):
        obj = YBase('./test/test_base.yml')
        # Replace actions config with custom for test case
        obj.actions_config.action_table = {'table1': 'insert'}

        with pytest.raises(ActionNotFound):
            obj.do_action('add', 'table1')

        assert not obj.db_worker.tables

        obj.do_actions()

        assert obj.db_worker.tables[0] == obj.yaml_config.tables_info[0].table_name

        obj.actions_config.action_table = {'table1': 'remove'}
        obj.do_actions()
        capsys.readouterr()
        obj.do_actions()

        out, err = capsys.readouterr()
        assert out == "\nFAILED ACTION remove on table table1\nReason: Can't do remove action\n\n"
        assert not obj.db_worker.tables
