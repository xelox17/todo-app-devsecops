import os, logging, requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
API_URL = os.environ.get('API_URL', 'http://backend:5001')

@app.route('/')
def index():
    tasks = requests.get(f'{API_URL}/api/tasks').json()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    data = {'title': request.form['title'],
            'description': request.form.get('description', '')}
    requests.post(f'{API_URL}/api/tasks', json=data)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    requests.delete(f'{API_URL}/api/tasks/{task_id}')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
