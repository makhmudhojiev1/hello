from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'quiz_secret_key'

# Questions from the provided quiz
quiz_variants = {
    "variant1": [
        {"question": "Более 90 элементов из 118, представленных в периодической таблице, - ...", "options": ["металлы", "неметаллы"], "answer": "металлы"},
        {"question": "Все элементы первой, второй и третьей групп (кроме ... и ...) - металлы.", "options": ["бор, водород", "углерод, азот"], "answer": "бор, водород"},
        {"question": "Все элементы основной подгруппы четвертой группы (кроме ... и ...) - металлы.", "options": ["углерод, кремний", "полоний, висмут"], "answer": "углерод, кремний"},
        {"question": "В основной подгруппе пятой группы имеются два металла: ... и ...", "options": ["висмут, сурьма", "бор, алюминий"], "answer": "висмут, сурьма"},
        {"question": "В основной подгруппе шестой группы имеется один металл: ...", "options": ["полоний", "селен"], "answer": "полоний"},
        {"question": "Какие металлы относятся к легким?", "options": ["литий, натрий, калий, кальций, алюминий, магний, титан", "золото, серебро, платина"], "answer": "литий, натрий, калий, кальций, алюминий, магний, титан"},
    ],
    "variant2": [
        {"question": "Способ основан на высокотемпературной термической обработке соединений металлов или на восстановлении оксидов металлов.", "options": ["пирометаллургический", "гидрометаллургический"], "answer": "пирометаллургический"},
        {"question": "Данный способ применяется при производстве ... и ...", "options": ["стали и чугуна", "алюминия и меди"], "answer": "стали и чугуна"},
        {"question": "С помощью ... способа выделяют металлы", "options": ["гидрометаллургического", "электролитического"], "answer": "гидрометаллургического"},
        {"question": "Все элементы побочных подгрупп четвертой, пятой, шестой, седьмой и восьмой групп - ...", "options": ["металлы", "неметаллы"], "answer": "металлы"},
        {"question": "Самый легкий металл - ...", "options": ["литий", "натрий"], "answer": "литий"},
        {"question": "Самый тяжелый металл - ...", "options": ["осмий", "свинец"], "answer": "осмий"},
    ]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['variant'] = request.form['variant']
        session['score'] = 0
        session['current_question'] = 0
        session['answers'] = []
        return redirect(url_for('quiz'))
    
    return render_template_string(index_html)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    variant = session.get('variant', 'variant1')
    questions = quiz_variants[variant]
    current_question = session.get('current_question', 0)
    
    if current_question >= len(questions):
        return redirect(url_for('result'))
    
    question = questions[current_question]
    if request.method == 'POST':
        user_answer = request.form['answer']
        session['answers'].append({
            'question': question['question'],
            'user_answer': user_answer,
            'correct_answer': question['answer'],
            'correct': user_answer == question['answer']
        })
        if user_answer == question['answer']:
            session['score'] += 1
        session['current_question'] += 1
        return redirect(url_for('quiz'))
    
    return render_template_string(quiz_html, question=question, total=len(questions), current=current_question + 1)

@app.route('/result')
def result():
    score = session.get('score', 0)
    answers = session.get('answers', [])
    total = len(quiz_variants[session.get('variant', 'variant1')])
    percent = (score / total) * 100
    return render_template_string(result_html, score=score, total=total, percent=percent, answers=answers)

index_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Главная страница</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7fc;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }

        h1 {
            font-size: 36px;
            color: #4CAF50;
            margin-bottom: 20px;
        }

        label, select, button {
            font-size: 18px;
            margin: 10px 0;
            padding: 10px;
            width: 100%;
            max-width: 250px;
            margin-left: auto;
            margin-right: auto;
        }

        select, button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

    </style>
</head>
<body>
    <div class="container">
        <h1>Добро пожаловать в викторину!</h1>
        <form method="POST">
            <label for="variant">Выберите вариант викторины:</label>
            <select name="variant" id="variant">
                <option value="variant1">Вариант 1</option>
                <option value="variant2">Вариант 2</option>
            </select>
            <button type="submit">Начать викторину</button>
        </form>
    </div>
</body>
</html>
"""

quiz_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Викторина</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7fc;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .quiz-container {
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
            text-align: center;
        }

        h2 {
            color: #4CAF50;
        }

        .option {
            margin: 15px 0;
            display: block;
            font-size: 20px;
            padding-left: 30px;
        }

        .option input {
            margin-right: 15px;
            transform: scale(1.3);
            vertical-align: middle;
        }

        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            width: 100%;
            cursor: pointer;
            margin-top: 20px;
        }

        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="quiz-container">
        <h2>Вопрос {{ current }} из {{ total }}</h2>
        <p>{{ question['question'] }}</p>
        <form method="POST">
            {% for option in question['options'] %}
                <label class="option">
                    <input type="radio" name="answer" value="{{ option }}">
                    {{ option }}
                </label>
            {% endfor %}
            <button type="submit">Далее</button>
        </form>
    </div>
</body>
</html>
"""

result_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Результаты викторины</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7fc;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .result-container {
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
            text-align: center;
        }

        h2 {
            color: #4CAF50;
        }

        .answers ul {
            list-style-type: none;
            padding: 0;
        }

        .answers li {
            margin-bottom: 15px;
        }

        .correct {
            color: green;
            font-weight: bold;
        }

        .incorrect {
            color: red;
            font-weight: bold;
        }

        .btn {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            width: 100%;
            cursor: pointer;
            margin-top: 20px;
        }

        .btn:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="result-container">
        <h2>Викторина завершена!</h2>
        <p>Ваш результат: {{ score }} / {{ total }} ({{ percent }}%)</p>
        <div class="answers">
            <h3>Ваши ответы:</h3>
            <ul>
                {% for answer in answers %}
                    <li>
                        <strong>Вопрос:</strong> {{ answer['question'] }}<br>
                        <strong>Ваш ответ:</strong> {{ answer['user_answer'] }}<br>
                        <strong>Правильный ответ:</strong> {{ answer['correct_answer'] }}<br>
                        {% if answer['correct'] %}
                            <span class="correct">Правильно!</span>
                        {% else %}
                            <span class="incorrect">Неправильно</span>
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
        </div>
        <a href="/" class="btn">Попробовать снова</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
