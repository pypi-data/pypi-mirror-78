from YamlBase import Table, Column
import pytest


@pytest.fixture
def test_column_1():
    return Column(
        column_name='column1',
        column_type='text',
        is_pk=True,
        is_sk=False
    )


@pytest.fixture
def test_column_2():
    return Column(
        column_name='column2',
        column_type='int',
        is_pk=False,
        is_sk=False
    )


@pytest.fixture
def test_permission():
    return {
        'user1': 'r*w*',
        'user2': 'r'
    }


class TestTable:

    def test_eq_right_order(self, test_column_1, test_column_2, test_permission):
        table1 = Table(
            schema_name='schema1',
            table_name='table1',
            columns=[test_column_1, test_column_2],
            permissions=test_permission
        )

        table2 = Table(
            schema_name='schema1',
            table_name='table1',
            columns=[test_column_1, test_column_2],
            permissions=test_permission
        )

        assert table1 == table2

    def test_eq_wrong_col_order(self, test_column_1, test_column_2, test_permission):
        table1 = Table(
            schema_name='schema1',
            table_name='table1',
            columns=[test_column_1, test_column_2],
            permissions=test_permission
        )

        table2 = Table(
            schema_name='schema1',
            table_name='table1',
            columns=[test_column_2, test_column_1],
            permissions=test_permission
        )

        assert table1 == table2


class TestColumns:

    def test_str(self, test_column_1):
        assert f"column_name = column1\ncolumn_type = text\n" \
               f"is_pk = True\nis_sk = False\nsk_link = None" == str(test_column_1)

