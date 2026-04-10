import os, logging
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres'),
        port=os.environ.get('DB_PORT', '5432'),
        dbname=os.environ.get('DB_NAME', 'tododb'),
        user=os.environ.get('DB_USER', 'todouser'),
        password=os.environ.get('DB_PASSWORD', 'todopass'))

def init_db():
    conn = get_db(); cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY, title VARCHAR(200) NOT NULL,
        description TEXT, status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit(); cur.close(); conn.close()

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = cur.fetchall(); cur.close(); conn.close()
    app.logger.info(f'Retrieved {len(tasks)} tasks')
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    app.logger.debug(f'Creating task: {data}')
    conn = get_db(); cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING *',
        (data['title'], data.get('description', '')))
    task = cur.fetchone(); conn.commit(); cur.close(); conn.close()
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db(); cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit(); cur.close(); conn.close()
    return jsonify({'message': 'deleted'}), 200

if __name__ == '__main__':
    init_db(); app.run(host='0.0.0.0', port=5001, debug=True)
