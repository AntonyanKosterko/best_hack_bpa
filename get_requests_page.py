from flask import Flask, request, render_template_string, redirect, url_for
from database_services import DataBaseManager
import methods
app = Flask(__name__)


data = methods.get_data()

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Массивы с элементами для удаления</title>
</head>
<body>
  <h1>Выберите массив и нажмите 'Поиск'</h1>
  <form method="post">
    <select name="dropdown">""" + methods.get_html_code() + """
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


@app.route('/', methods=['GET', 'POST'])
def index():
    global data
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
