import psycopg2


class DataBaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.user = 'postgres'
        self.password = '1q2ws3edc4r'
        self.host = 'localhost'

    def get_struct(self, data_base_name):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                request_for_a_structure = f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{data_base_name}';
                """
                try:
                    cursor.execute(request_for_a_structure)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return []

    def check_table(self, table_name):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                query = f'''SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = {table_name});
                        '''
                cursor.execute(query)
                print(cursor.fetchone())

    @staticmethod
    def get_data_type(value):
        if isinstance(value, int):
            return 'INTEGER'
        elif isinstance(value, float):
            return 'REAL'
        elif isinstance(value, str):
            return 'VARCHAR(255)'
        else:
            raise TypeError(f"Unsupported data type: {type(value)}")

    def create_table(self, table_name, columns, first_row):
        if len(columns) != len(first_row):
            raise Exception('Count of columns don`t match count of args')

        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                column_definitions = [
                    f"{col} {self.get_data_type(val)}"
                    for col, val in zip(columns, first_row)
                ]

                create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ('
                for i, value in enumerate(column_definitions):
                    create_table_query += '\n\t' + value
                    if i != len(column_definitions) - 1:
                        create_table_query += ','
                create_table_query += '\n);'

                cursor.execute(create_table_query)
                connection.commit()

    def add_row(self, table_name, row):
        if len(row) != len(self.get_struct(table_name)):
            raise Exception('Count of args don`t match count of columns')

        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                struct = self.get_struct(table_name)
                columns = []
                for pair in struct:
                    columns.append(pair[0])

                column_names = ', '.join(columns)
                placeholders = ','.join(['%s'] * len(row))
                insert_row_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders});"

                try:
                    cursor.execute(insert_row_query, row)
                    connection.commit()
                except Exception as e:
                    print(f"An error occurred: {e}")

    def get_full_table(self, table_name):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                read_query = f'SELECT * FROM {table_name}'
                cursor.execute(read_query)
                return cursor.fetchall()

    def clear_table(self, table_name):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                drop_query = f'TRUNCATE TABLE {table_name};'
                cursor.execute(drop_query)
                connection.commit()

    def print_all_tables(self):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                                SELECT table_schema, table_name
                                FROM information_schema.tables
                                WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                                ORDER BY table_schema, table_name;
                            """)
                tables_list = cursor.fetchall()
                return tables_list

    def drop_table(self, table_name):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
                cursor.execute(drop_table_query)
                connection.commit()

    def get_rows(self, table_name, args: dict):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                get_row_query = f"SELECT * FROM {table_name} WHERE "
                for i, key in enumerate(args.keys()):
                    if isinstance(args[key], str):
                        get_row_query += f"{key} = '{args[key]}'"
                    else:
                        get_row_query += f"{key} = {args[key]}"
                    if i != len(args) - 1:
                        get_row_query += ' AND '
                get_row_query += ';'
                cursor.execute(get_row_query)
                rows = cursor.fetchall()
                connection.commit()
                return rows

    def get_original_items(self, table_name, column):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                get_original_items_query = f"SELECT DISTINCT {column} FROM {table_name};"
                cursor.execute(get_original_items_query)
                rows = cursor.fetchall()
                connection.commit()
                return rows

    def delete_rows(self, table_name, args: dict):
        with psycopg2.connect(dbname=self.db_name, user=self.user,
                              password=self.password, host=self.host) as connection:
            with connection.cursor() as cursor:
                delete_row_query = f"DELETE FROM {table_name} WHERE "
                for i, key in enumerate(args.keys()):
                    if isinstance(args[key], str):
                        delete_row_query += f"{key} = '{args[key]}'"
                    else:
                        delete_row_query += f"{key} = {args[key]}"
                    if i != len(args) - 1:
                        delete_row_query += ' AND '
                delete_row_query += ';'
                cursor.execute(delete_row_query)
                connection.commit()

