from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

questions = [
    {
        'question': 'Co to jest Fifa?',
        'answers': ['Gra stworzona przez EA','Protokół sieciowy', 'Odgrzewany kotlet'],
        'correct': 'Odgrzewany kotlet'
    },
    {
        'question': 'Nazwa biblioteki do obsługi plików w C++',
        'answers': ['fstream', 'iostream', 'Biblioteka nie jest potrzebna'],
        'correct': 'fstream'
    },
    {
        'question': 'W którym roku został założony Rzym',
        'answers': ['435 p.n.e', '753 p.n.e', '2016'],
        'correct': '753 p.n.e'
    }
]

app.config.update(dict(
    SECRET_KEY='fifatoodgrzewanykotletzpoprzednijesoboty',
))


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        points = 0
        user_answers = request.form
        for pnr, answer in user_answers.items():
            if answer == questions[int(pnr)]['correct']:
                points += 1
        flash('Liczba poprawnych odpowiedzi, to: {0}'.format(points))
        flash(user_answers)
        correct_answers = []
        index = 0
        for question in questions:
            correct_answers.append(question['correct'])
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
