from YamlBase.utils import convert_table_data_from_dict_to_table_obj
import yaml


def test_convert_table_data_from_dict_to_table_obj():
    with open('./test/test_base.yml') as f:
        cfg = yaml.load(f, Loader=yaml.Loader)

    test_schema_name = 'main'
    test_table_name = 'table_1'

    converted_table = convert_table_data_from_dict_to_table_obj(cfg['schemas'][test_schema_name][test_table_name],
                                                    test_schema_name)
    assert converted_table.table_name == cfg['schemas'][test_schema_name][test_table_name]['name']
    assert converted_table.schema_name == test_schema_name
    assert converted_table.permissions == cfg['schemas'][test_schema_name][test_table_name]['permissions']

    assert converted_table.columns[0].column_name == \
           cfg['schemas'][test_schema_name][test_table_name]['columns']['column1']['name']

    assert converted_table.columns[0].column_type == \
           cfg['schemas'][test_schema_name][test_table_name]['columns']['column1']['type']

    assert converted_table.columns[0].is_pk == \
           bool(cfg['schemas'][test_schema_name][test_table_name]['columns']['column1']['is_pk'])

    assert converted_table.columns[0].is_sk == \
           bool(cfg['schemas'][test_schema_name][test_table_name]['columns']['column1']['is_sk'])
