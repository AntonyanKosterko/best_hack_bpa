from flask import Flask, request, render_template_string, redirect, url_for
from database_services import DataBaseManager
import methods

app = Flask(__name__)

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
"""

MENU_TEMPLATE = """
<nav style="position: fixed; top: 10px; right: 10px;">
    <form action="{{url_for('data_input')}}" method="get">
        <button type="submit">Ввод данных</button>
    </form>
    <form action="{{url_for('data_view')}}" method="get">
        <button type="submit">Просмотр данных</button>
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

        category = '2'
        manager = DataBaseManager('Avito')
        manager.add_row('requests', [category, user_id, text_of_request])

        message = 'Обращению присвоена категория: ' + category
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
      {% if arrays %}
        <ul>
          {% for item in arrays %}
            <li>
              {{ item }}
              <!-- Кнопка удаления для каждого элемента -->
              <form method="post" style="display: inline;">
                <input type="hidden" name="delete" value="{{ item }}">
                <input type="hidden" name="array_choice" value="{{ array_choice }}">
                <input type="submit" value="Удалить">
              </form>
            </li>
          {% endfor %}
        </ul>
      {% endif %}
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
            user_id = to_delete[len('user_id: '):to_delete.index('     requests text: ')]
            text = to_delete[to_delete.index('requests text: ') + len('requests text: '):]
            manager = DataBaseManager('Avito')
            manager.delete_rows('requests', {'user_id': user_id, 'text_of_request': text})
            data = methods.get_data()

    arrays = data.get(array_choice, [])
    return render_template_string(HTML_TEMPLATE, arrays=arrays, array_choice=array_choice)

if __name__ == '__main__':
    app.run(debug=True)
