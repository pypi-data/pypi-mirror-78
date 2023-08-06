# YamlBase
[![codecov](https://codecov.io/gh/mv-yurchenko/YBase/branch/dev/graph/badge.svg)](https://codecov.io/gh/mv-yurchenko/YBase)
[![Actions Status](https://github.com/mv-yurchenko/YBase/workflows/deploy_on_master/badge.svg)](https://github.com/mv-yurchenko/YBase/actions)
[![CodeFactor](https://www.codefactor.io/repository/github/mv-yurchenko/ybase/badge)](https://www.codefactor.io/repository/github/mv-yurchenko/ybase)
[![PyPI version](https://badge.fury.io/py/YamlBase.svg)](https://badge.fury.io/py/YamlBase)
[![GitHub version](https://badge.fury.io/gh/mv-yurchenko%2FYBase.svg)](https://badge.fury.io/gh/mv-yurchenko%2FYBase)

This utility allows you to manage tables in a database using YAML files, which makes it faster to create and delete tables in multiple databases simultaneously

## The following databases are currently supported: 

- [SQLite](###sqlite-config-example) 

## Installation 

```shell script
pip install YamlBase
``` 
## Config examples
### SQLite config example 

<details>
  <summary>Click to expand!</summary>
  
> base_example.yaml
```
db_type: "SQLite" # -  type of database
ip: "H:/YBase/" # - path to file with database 
db_name: "test_db" # - database file name

username: ""
password: ""

schemas: # - list of schemas in database (main - default in SQLite)

  main:

    table_1: # - table description example
      name: "table1" # - must be same as block name
      descriprion: "table for test" # - some custom descriprions
      permissions: [] # - unused in SQLite

      columns: # - list of columns 
        column1: # - column example
          name: "column1" # - must be same as block name
          type: "text" # - type of columns in SQLite
          is_pk: 1 # - is column a primary key 
          is_sk: 0 # - is column is secondary key (if 1 than defina sk_link)
          sk_link: 0 # - sk link for table (table.column)
``` 

> actions_example.yaml 
```
# table : action
# table must be in database if remove or in base_config if insert
# table1 : insert - insert action
# table2 : remove - remove action
```
</details>

## Usage Example

To use this utility, you need 2 files, one is the configuration of new tables for the database, and the second is a file with a list of actions

File examples: 
- actions_example.yaml
- base_example.yaml
