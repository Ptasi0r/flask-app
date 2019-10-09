from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors
app = Flask(__name__)

# questions = [
#     {
#         'question': 'Co to jest Fifa?',
#         'answers': ['Gra stworzona przez EA North','Protokół sieciowy', 'Odgrzewany kotlet'],
#         'correct': 'Odgrzewany kotlet'
#     },
#     {
#         'question': 'Nazwa biblioteki do obsługi plików w C++',
#         'answers': ['fstream', 'iostream', 'Biblioteka nie jest potrzebna'],
#         'correct': 'fstream'
#     },
#     {
#         'question': 'W którym roku został założony Rzym',
#         'answers': ['435 p.n.e', '753 p.n.e', '2016'],
#         'correct': '753 p.n.e'
#     }
# ]

questions = []

app.config.update(dict(
    SECRET_KEY='fifatoodgrzewanykotletzpoprzednijesoboty',
))

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='',
#                              db='flask',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

connection = pymysql.connect(host='eu-cdbr-west-02.cleardb.net',
                             user='be088d48b4c018',
                             password='0603f8d2',
                             db='heroku_f0516d25d5b7ef9',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def get_array(result):
    array = []
    for line in result:
        array.append(line['answer'])
    return array

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM questions"
        cursor.execute(sql)
        db_questions = cursor.fetchall()
        for question in db_questions:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM answers WHERE answered_by_id =%s"
                cursor.execute(sql, question['question_id'])
                result = cursor.fetchall()
                print(result, )
                questions.append({
                    'question': question['question'],
                    'answers': get_array(result),
                    'correct_answers': result[int(question['correct_answers_id']) - 1]['answer']
                })
finally:
    print(questions)
    connection.close()


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        points = 0
        user_answers = request.form
        for pnr, answer in user_answers.items():
            if answer == questions[int(pnr)]['correct_answers']:
                points += 1
        flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points))
        flash(user_answers)
        correct_answers = []
        index = 0
        for question in questions:
            correct_answers.append(question['correct_answers'])
            index += 1
        flash(correct_answers)
        return redirect(url_for('main'))
    return render_template('index.html', questions=questions)

# def index():
#     if request.method == 'POST':
#         points = 0
#         user_answers = request.form
#         for pnr, answer in user_answers.items():
#             if answer == questions[int(pnr)]['correct']:
#                 points += 1
#         flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points))
#         return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
