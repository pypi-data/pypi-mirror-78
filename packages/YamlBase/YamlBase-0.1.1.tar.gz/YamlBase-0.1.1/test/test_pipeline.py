import os
import yaml
import pytest
import sys

@pytest.fixture
def test_insert_config():
    return {
        'table1' : 'insert',
        'table2' : 'insert'
    }

@pytest.fixture
def test_remove_config():
    return {
        'table1' : 'remove',
        'table2' : 'remove'
    }


def test_insert_pipeline(test_insert_config, test_remove_config):
    os.system("python setup.py sdist")
    filename = os.listdir('dist')[0]
    os.system("pip install dist/" + filename)
    with open("test/configs_for_tests/test_db_actions.yaml", 'w') as f: 
        yaml.dump(test_insert_config, f)

    os.system('yamlbase -cfg_db test/configs_for_tests/test_base_pipeline.yaml')
    
    with open("YamlBaseCache/test__SQLite_test_db.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.Loader)

    assert list(cfg['schemas'].keys()) == ['main']
    assert cfg['schemas']['main'][0]['name'] == 'table1'
    assert cfg['schemas']['main'][1]['name'] == 'table2'

    with open("test/configs_for_tests/test_db_actions.yaml", 'w') as f: 
        yaml.dump(test_remove_config, f)

    os.system('yamlbase -cfg_db test/configs_for_tests/test_base_pipeline.yaml')
    
    with open("YamlBaseCache/test__SQLite_test_db.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.Loader)
    
    assert not cfg['schemas']['main']

    os.system("pip uninstall sdist/" + filename)