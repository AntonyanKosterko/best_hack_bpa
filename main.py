import datetime

from flask import Flask, request, render_template_string, redirect, url_for
from database_services import DataBaseManager
import methods
import nltk
import joblib
from model.answer import get_cluster
app = Flask(__name__)

# Предварительная обработка текстов
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

CSS_STYLE = """
/* Общие стили */
body {
  font-family: 'Arial', sans-serif;
  background-color: #121212;
  color: #ffffff;
  margin: 0;
  padding: 0;
}

h1 {
  color: #ffffff;
}

button, input[type="submit"], select {
  background-color: #1f1f1f;
  border: none;
  color: #fff;
  padding: 10px 20px;
  text-transform: uppercase;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1rem;
}

button:hover, input[type="submit"]:hover, select:hover {
  background-color: #383838;
}

input[type="text"] {
  background-color: #1f1f1f;
  border: none;
  color: #fff;
  padding: 10px;
  border-radius: 5px;
  width: calc(100% - 24px);
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

/* Меню навигации */
nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background-color: #1c1c1c;
  position: fixed;
  top: 0;
  width: calc(100% - 40px);
}

form {
  margin: 0;
}

/* Стили для улучшенной красоты и читаемости */
.container {
  padding: 20px;
  margin-top: 60px; /* Отступ, чтобы навигационное меню не перекрывало содержимое */
}

/* Стили для скрипта */
.alert {
  color: #ff5722;
}
.card {
  background-color: #25282c;
  border: 1px solid #444;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
}
.card-header {
  background-color: #33383d;
  border-bottom: 1px solid #444;
  padding: 0.75rem 1rem;
  border-top-left-radius: calc(0.25rem - 1px);
  border-top-right-radius: calc(0.25rem - 1px);
  color: #aaa;
  font-weight: bold;
}
.card-body {
  padding: 1rem;
}
.card-body p {
  margin: 0;
  color: #ddd;
}
.delete-button {
  background-color: #d9534f;
  color: white;
  padding: 0.2rem 0.6rem;
  border: none;
  margin-left: 1rem;
  border-radius: 0.2rem;
  cursor: pointer;
}
.delete-button:hover {
  background-color: #c9302c;
}
"""

MENU_TEMPLATE = """
<nav style="position: fixed; top: 10px; right: 10px;">
    <form action="{{url_for('data_input')}}" method="get">
        <button type="submit">Создать обращение</button>
    </form>
    <form action="{{url_for('data_view')}}" method="get">
        <button type="submit">Просмотр обращений</button>
    </form>
</nav>
"""

@app.route('/')
def home():
    return redirect(url_for('data_view'))

@app.route('/input', methods=['GET', 'POST'])
def data_input():
    message = None


    if request.method == 'POST':
        # Получение данных из полей формы
        user_id = request.form.get('user_id')
        text_of_request = request.form.get('text_of_request')
        time = str(datetime.datetime.now()).replace('-', ' ').replace(':', ' ').replace(':', ' ').replace('.', ' ')
        category = get_cluster(text_of_request)
        manager = DataBaseManager('Avito')
        manager.add_row('requests', [str(category[0]), str(user_id), text_of_request, time, '', '', ''])

        message = 'Обращению присвоена категория: ' + str(category[0])
    js_message = repr(message) if message else 'null'

    HTML_TEMPLATE = """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <title>Введите данные</title>
          <style>
          {css}
          </style>
          <script type="text/javascript">
        // Скрипт для отображения алерта после отправки формы
        window.onload = function() {{
          var message = {js_message};
          if (message) {{
            alert(message);
          }}
        }};
      </script>
        </head>
        <body>
            {menu}
          <h1>Введите данные</h1>
          <form method="post">
            <input type="text" name="user_id" placeholder="Введите id пользователя" />
            <input type="text" name="text_of_request" placeholder="Введите текст обращения" />
            <input type="submit" value="Отправить">
          </form>
        </body>
        </html>
        """.format(js_message=js_message, menu=MENU_TEMPLATE, css=CSS_STYLE)

    return render_template_string(HTML_TEMPLATE)

@app.route('/view', methods=['GET', 'POST'])
def data_view():
    HTML_TEMPLATE = """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>Массивы с элементами для удаления</title>
      <style>
      {css}      
      </style>
    </head>
    <body>
    {menu}
      <h1>Выберите массив и нажмите 'Поиск'</h1>
      <form method="post">
        <select name="dropdown">
        <option value="none">Не выбрано</option>""".format(menu=MENU_TEMPLATE, css=CSS_STYLE) + methods.get_html_code() + """
        </select>
        <input type="submit" name="search" value="Поиск">
      </form>
      <br>
      {% for item in arrays %}
      {% if not item.close_time %}
    <div class="card">
      <div class="card-header">
        Обращение #{{ loop.index }}
      </div>
      <div class="card-body">
        <p><b>user_id:</b> {{ item.user_id }}<br>{{ item.text_of_request }}</p>
        {% if item.is_being_handled %}
          <span class="handled-badge">Обращение в обработке</span>
          <!-- Форма удаления элемента -->
        <form method="post" style="display: inline;">
              <input type="hidden" name="delete" value="{{ item }}">
              <input type="hidden" name="array_choice" value="{{ array_choice }}">
              <button type="submit" class="delete-button">Закрыть</button>
        </form>
        {% endif %}
        <!-- Форма отметки обработки элемента -->
        {% if not item.is_being_handled %}
          <form method="post" style="display: inline;">
              <input type="hidden" name="mark" value="{{ item }}">
              <input type="hidden" name="array_choice" value="{{ array_choice }}">
              <button type="submit" class="mark-button">Отметить</button>
          </form>
        {% endif %}
        
        
      </div>
    </div>
    {% endif %}
  {% endfor %}
    </body>
    </html>
    """
    data = methods.get_data()
    array_choice = None

    if request.method == 'POST':
        array_choice = request.form.get('array_choice')

        if 'search' in request.form:
            array_choice = request.form.get('dropdown')
        elif 'delete' in request.form:
            to_delete = request.form.get('delete')
            manager = DataBaseManager('Avito')
            delete_dict = methods.str_to_dict(to_delete)
            manager.delete_rows('requests', methods.str_to_dict(to_delete))
            delete_dict['close_time'] = str(datetime.datetime.now()).replace('-', ' ').replace(':', ' ').replace(':',
                                                                                                                 ' ').replace('.', ' ')
            if delete_dict['is_being_handled'] != '1':
                delete_dict['handled_time'] = str(datetime.datetime.now()).replace('-', ' ').replace(':', ' ').replace(':',
                                                                                                                 ' ').replace('.', ' ')
                delete_dict['is_being_handled'] = '1'
            delete_arr = []
            for v in delete_dict.values():
                delete_arr.append(v)
            manager.add_row('requests', delete_arr)

            manager.delete_rows('requests', methods.str_to_dict(to_delete))
            data = methods.get_data()
            array_choice = request.form.get('array_choice')
        elif 'mark' in request.form:
            to_mark = request.form.get('mark')
            manager = DataBaseManager('Avito')
            mark_dict = methods.str_to_dict(to_mark)
            manager.delete_rows('requests', methods.str_to_dict(to_mark))
            mark_dict['is_being_handled'] = '1'
            mark_dict['handled_time'] = str(datetime.datetime.now()).replace('-', ' ').replace(':', ' ').replace(':', ' ').replace('.', ' ')
            mark_arr = []
            for v in mark_dict.values():
                mark_arr.append(v)

            manager.add_row('requests', mark_arr)

            data = methods.get_data()
            array_choice = request.form.get('array_choice')

    arrays = data.get(array_choice, [])
    return render_template_string(HTML_TEMPLATE, arrays=arrays, array_choice=array_choice)

if __name__ == '__main__':
    try:
        methods.start_work()
    except:
        pass
    app.run(debug=True)
