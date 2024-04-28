import datetime
from database_services import DataBaseManager
import json
from model.answer import get_cluster
import ast
import nltk

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


def str_to_dict(input_string):
    # Удаление пробелов в начале и конце строки, если они есть
    input_string = input_string.strip()

    # Парсинг строки в словарь
    result_dict = ast.literal_eval(input_string)

    return result_dict

def load_database_from_json():
    filename = 'dataset_hack.json'
    array_of_dicts = []

    with open(filename, 'r', encoding='utf-8') as file:
        array_of_dicts = json.load(file)

    time = str(datetime.datetime.now()).replace('-', ' ').replace(':', ' ').replace(':', ' ').replace('.', ' ')
    manager = DataBaseManager('Avito')
    for row in array_of_dicts[:200]:
        text = row['message']
        arr = text.split()
        id = 0
        for word in arr:
            try:
                id = int(word)
                break
            except:
                pass
        category = get_cluster(text)
        if id:
            manager.add_row('requests', [str(category[0]), str(id), text, time, '', '', ''])

def get_closed_req():
    manager = DataBaseManager('Avito')
    arr = manager.get_full_table('requests')
    result = []
    for a in arr:
        if a[6]:
            result.append(a)
    return result

def start_work():
    manager = DataBaseManager('Avito')
    manager.create_table('requests', ['category', 'user_id', 'text_of_request', 'creating_time', 'is_being_handled',
                                      'handled_time', 'close_time'],
                         ['text', 'text', 'text', 'text', 'text', 'text', 'text', ])
    # Предварительно загрузка необходимых ресурсов NLTK
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    load_database_from_json()


def convert_to_datetime(date_string):
    date_format = "%Y %m %d %H %M %S %f"
    return datetime.datetime.strptime(date_string, date_format)

def print_statistics():
    manager = DataBaseManager('Avito')
    table = manager.get_full_table('requests')
    count_of_hangled = 0
    count_of_closed = 0
    sum_of_hangled = 0
    sum_of_closed = 0
    for row in table:
        if row[5]:
            count_of_hangled += 1
            sum_of_closed += (convert_to_datetime(row[5]) - convert_to_datetime(row[3])).seconds
        if row[6]:
            count_of_closed += 1
            sum_of_hangled += (convert_to_datetime(row[6]) - convert_to_datetime(row[5])).seconds

    print('количество обращений, которые были в обработке', count_of_hangled)
    print('среднее время, перед тем, как обращение было принято в обработку ', sum_of_hangled / count_of_hangled)
    print('количество обращений, которые были закрыты', count_of_closed)
    print('среднее время обработки обращения', sum_of_closed / count_of_closed)

