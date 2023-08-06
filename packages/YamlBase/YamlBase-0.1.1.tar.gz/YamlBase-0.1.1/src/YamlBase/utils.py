from .table_representation import Table, Column


def convert_table_data_from_dict_to_table_obj(table_dict: dict, schema_name: str) -> Table:

    columns = []

    for col in table_dict['columns']:

        is_pk = table_dict['columns'][col]['is_pk'] == 1

        is_sk = table_dict['columns'][col]['is_sk'] == 1
        sk_link = None

        if is_sk:
            sk_link = table_dict['columns'][col]['link']

        columns.append(
            Column(
                table_dict['columns'][col]['name'],
                table_dict['columns'][col]['type'],
                is_pk,
                is_sk,
                sk_link
            )
        )

    return Table(
        schema_name=schema_name,
        table_name=table_dict['name'],
        permissions=table_dict['permissions'],
        columns=columns
    )

