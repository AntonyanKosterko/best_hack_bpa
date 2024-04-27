from database_services import DataBaseManager


def get_data():
    manager = DataBaseManager('Avito')
    categories = manager.get_original_items('requests', 'category')
    data = {}
    data['none'] = []
    for i, category in enumerate(categories):
        data[f"category{i}"] = []
        rows = manager.get_rows('requests', {'category': category[0]})
        for row in rows:
            data[f"category{i}"].append({'user_id': row[1], 'text_of_request': row[2]})
    return data

def get_html_code():
    string = ''
    manager = DataBaseManager('Avito')
    categories = manager.get_original_items('requests', 'category')
    for i, category in enumerate(categories):
        string += f'\n<option value="category{i}">{category[0]}</option>'

    return string

def str_to_dict(s):
    s = s.strip("'{ }").replace("': '", '": "').replace("', '", '", "')
    pairs = s.split('", "')
    dictionary = {}
    for pair in pairs:
        key, value = pair.split('": "')
        dictionary[key] = value.strip('"')

    return dictionary
