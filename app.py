from flask import Flask, render_template, request, redirect, url_for
import random
from datetime import datetime

app = Flask(__name__)

# Predefined data
QUOTES = [
    "Every workout counts. Keep pushing!",
    "You're getting stronger every day!",
    "Sweat now, shine later.",
    "Discipline beats motivation — but you’ve got both today!"
]

WORKOUTS = [
    "Go for a 30-minute walk or jog.",
    "Try 15 squats, 10 push-ups, and 20 jumping jacks.",
    "Do a 10-minute HIIT session.",
    "Try yoga or stretching for 20 minutes."
]

# Store logs temporarily in memory
logs = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/log', methods=['POST'])
def log():
    try:
        calories_consumed = int(request.form['calories_consumed'])
        calories_burned = int(request.form['calories_burned'])
        note = request.form.get('note', '').strip()
    except ValueError:
        return render_template('result.html', message="Please enter valid numbers!")

    if calories_burned > calories_consumed:
        message = random.choice(QUOTES)
        result_type = "quote"
    else:
        message = WORKOUTS
        result_type = "workouts"

    # Save log
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "consumed": calories_consumed,
        "burned": calories_burned,
        "note": note
    }
    logs.append(entry)

    return render_template('result.html',
                           calories_consumed=calories_consumed,
                           calories_burned=calories_burned,
                           result_type=result_type,
                           message=message)


@app.route('/logs')
def show_logs():
    return render_template('logs.html', logs=logs)


if __name__ == '__main__':
    app.run(debug=True)
