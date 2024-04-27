from flask import Flask, request, render_template_string
from database_services import DataBaseManager
app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Введите данные</title>
</head>
<body>
  <h1>Введите данные</h1>
  <form method="post">
    <input type="text" name="user_id" placeholder="Введите id пользователя" />
    <input type="text" name="text_of_request" placeholder="Введите текст обращения" />
    <input type="submit" value="Отправить">
  </form>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из полей формы
        user_id = request.form.get('user_id')
        text_of_request = request.form.get('text_of_request')

        category = '2'
        manager = DataBaseManager('Avito')
        manager.add_row('requests', [category, user_id, text_of_request])


        return 'Обращения присвоена категория: ' + category

    return render_template_string(HTML_TEMPLATE)


if __name__ == '__main__':
    app.run(debug=True)