from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

entries = []

# Fitness categories
CATEGORIES = ['Workout', 'Diet', 'Progress', 'Goals']

# Fitness daily prompts (less theoretical, more action-based)
DAILY_PROMPTS = [
    "How many calories did you burn during your workout today?",
    "How many calories did you consume today?",
    "What was your best lift or longest run today?",
    "How did your diet support your workout goals today?",
    "How close are you to hitting your weekly fitness target?",
    "What activity helped you stay active outside the gym?",
    "How much water did you drink today?"
]

@app.route('/')
def home():
    total_entries = len(entries)
    today = datetime.now().date()
    today_entries = [e for e in entries if e['date'].date() == today]

    # Calculate total calories burned/consumed today
    total_burned = sum(e.get('calories_burned', 0) for e in today_entries)
    total_consumed = sum(e.get('calories_consumed', 0) for e in today_entries)

    # Count per category
    categories_count = {cat: len([e for e in entries if e['category'] == cat]) for cat in CATEGORIES}

    import random
    daily_prompt = random.choice(DAILY_PROMPTS)

    recent_entries = sorted(entries, key=lambda x: x['date'], reverse=True)[:5]

    return render_template(
        'home.html',
        total_entries=total_entries,
        today_entries=len(today_entries),
        total_burned=total_burned,
        total_consumed=total_consumed,
        categories_count=categories_count,
        daily_prompt=daily_prompt,
        recent_entries=recent_entries
    )

@app.route('/new-entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        calories_burned = request.form.get('calories_burned')
        calories_consumed = request.form.get('calories_consumed')

        # Convert to int safely
        try:
            calories_burned = int(calories_burned) if calories_burned else 0
            calories_consumed = int(calories_consumed) if calories_consumed else 0
        except ValueError:
            flash('Calories must be numbers', 'error')
            return redirect(url_for('new_entry'))

        if title and content and category:
            entry = {
                'id': len(entries) + 1,
                'title': title,
                'content': content,
                'category': category,
                'calories_burned': calories_burned,
                'calories_consumed': calories_consumed,
                'date': datetime.now()
            }
            entries.append(entry)
            flash('Fitness log added successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please fill in all required fields', 'error')

    return render_template('new_entry.html', categories=CATEGORIES)

@app.route('/history')
def history():
    filter_category = request.args.get('category', 'All')

    if filter_category == 'All':
        filtered_entries = entries
    else:
        filtered_entries = [e for e in entries if e['category'] == filter_category]

    sorted_entries = sorted(filtered_entries, key=lambda x: x['date'], reverse=True)

    return render_template(
        'history.html',
        entries=sorted_entries,
        categories=CATEGORIES,
        current_filter=filter_category
    )

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry:
        return render_template('view_entry.html', entry=entry)
    else:
        flash('Log not found', 'error')
        return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
