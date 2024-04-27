import datetime

from database_services import DataBaseManager
import json

def get_data():
    manager = DataBaseManager('Avito')
    categories = manager.get_original_items('requests', 'category')
    data = {}
    data['none'] = []
    for i, category in enumerate(categories):
        data[f"category{i}"] = []
        rows = manager.get_rows('requests', {'category': category[0]})
        for row in rows:
            data[f"category{i}"].append({'category': row[0], 'user_id': row[1], 'text_of_request': row[2],
                                         'creating_time': row[3], 'is_being_handled': row[4], 'handled_time': row[5],
                                         'close_time': row[6]})
    return data

def get_html_code():
    string = ''
    manager = DataBaseManager('Avito')
    categories = manager.get_original_items('requests', 'category')
    for i, category in enumerate(categories):
        string += f'\n<option value="category{i}">{category[0]}</option>'

    return string

def str_to_dict(data_str):
    data_str = data_str.strip("{}")
    data_pairs = data_str.split(", ")
    data_dict = {}

    for pair in data_pairs:
        key, value = pair.split(": ")
        key = key.strip("''").strip('""')
        value = value.strip("''").strip('""')
        if value == 'True':
            value = True
        elif value == 'False':
            value = False
        elif value == 'None':
            value = None
        data_dict[key] = value

    return data_dict

def load_database_from_json():
    filename = 'dataset_hack.json'
    array_of_dicts = []

    with open(filename, 'r', encoding='utf-8') as file:
        array_of_dicts = json.load(file)

    time = str(datetime.datetime.now()).replace('-', ' ').replace(':', ' ').replace(':', ' ').replace('.', ' ')
    manager = DataBaseManager('Avito')
    manager.clear_table('requests') ### УДАЛИТЬ ПОТОМ НАДО
    for row in array_of_dicts[:100]:
        text = row['message']
        arr = text.split()
        id = 0
        for word in arr:
            try:
                id = int(word)
                break
            except:
                pass
        category = '1' ### ДОБАВИТЬ МОДЕЛЬ
        if id:
            manager.add_row('requests', [category, str(id), text, time, '', '', ''])
    print(manager.get_full_table('requests'))

