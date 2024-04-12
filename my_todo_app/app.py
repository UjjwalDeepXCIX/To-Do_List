from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample tasks list for demonstration purposes
tasks = [
    {'id': 1, 'text': 'Task 1', 'timestamp': datetime.now()},
    {'id': 2, 'text': 'Task 2', 'timestamp': datetime.now()},
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check login credentials (e.g., username and password)
        session['logged_in'] = True
        flash('You were successfully logged in', 'success')
        return redirect(url_for('todo_list'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were successfully logged out', 'info')
    return redirect(url_for('login'))

@app.route('/todo', methods=['GET', 'POST'])
def todo_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_task = request.form['new_task']
        tasks.append({'id': len(tasks) + 1, 'text': new_task})
        flash('Task added to the to-do list', 'success')
        return redirect(url_for('todo_list'))

    return render_template('todo.html', tasks=tasks)

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    flash('Task deleted from the to-do list', 'info')
    return redirect(url_for('todo_list'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    updated_task = request.form['updated_task']
    for task in tasks:
        if task['id'] == task_id:
            task['text'] = updated_task
            task['timestamp'] = datetime.now()
            break
    flash('Task updated', 'info')
    return redirect(url_for('todo_list'))

if __name__ == '__main__':
    app.run(debug=True)
