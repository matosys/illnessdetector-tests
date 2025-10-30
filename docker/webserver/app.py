# app.py
import datetime
import pathlib

from flask import Flask, jsonify, request, send_file
import sqlite3
import uuid

app = Flask(__name__)

decision_tree = {
    'start': {
        'question': "Do you have a fever (temperature above 100°F / 38°C)?",
        'options': [
            {'text': "Yes", 'next': "fever1"},
            {'text': "No", 'next': "noFever1"}
        ]
    },
    'noFever1': {
        'question': "Do you have any respiratory symptoms, like coughing or sneezing?",
        'options': [
            {'text': "Yes", 'next': "respiratory1"},
            {'text': "No", 'next': "noRespiratory1"}
        ]
    },
    'noRespiratory1': {
        'question': "Do you have stomach-related issues, like nausea, vomiting, or diarrhea?",
        'options': [
            {'text': "Yes", 'next': "stomach1"},
            {'text': "No", 'next': "noStomach1"}
        ]
    },
    'noStomach1': {
        'question': "Do you have headaches, fatigue, or muscle aches without other symptoms?",
        'options': [
            {'text': "Yes", 'result': "Possible diagnosis: Stress or dehydration. Suggest resting and drinking water."},
            {'text': "No", 'result': "No clear illness detected. Maybe it's just a bad day - try again with more details!"}
        ]
    },
    'fever1': {
        'question': "Is the fever accompanied by chills or sweating?",
        'options': [
            {'text': "Yes", 'next': "fever2"},
            {'text': "No", 'result': "Possible diagnosis: Mild infection or overheating. Suggest monitoring and hydration."}
        ]
    },
    'fever2': {
        'question': "Do you have a sore throat or body aches?",
        'options': [
            {'text': "Yes", 'result': "Possible diagnosis: Flu. Recommend rest, fluids, and over-the-counter meds."},
            {'text': "No", 'next': "fever3"}
        ]
    },
    'fever3': {
        'question': "Any rash or swollen glands?",
        'options': [
            {'text': "Yes", 'result': "Possible diagnosis: Viral infection like mono. Advise seeing a doctor."},
            {'text': "No", 'result': "Possible diagnosis: Bacterial infection. Suggest antibiotics (in a real app, emphasize consulting a pro)."}
        ]
    },
    'respiratory1': {
        'question': "Is your cough dry (no mucus) or wet (with phlegm)?",
        'options': [
            {'text': "Dry", 'next': "respiratory2"},
            {'text': "Wet", 'result': "Possible diagnosis: Bronchitis or chest cold. Suggest cough syrup and rest."}
        ]
    },
    'respiratory2': {
        'question': "Do you have itchy eyes or a runny nose?",
        'options': [
            {'text': "Yes", 'result': "Possible diagnosis: Allergies. Recommend antihistamines."},
            {'text': "No", 'next': "respiratory3"}
        ]
    },
    'respiratory3': {
        'question': "Any shortness of breath?",
        'options': [
            {'text': "Yes", 'result': "Possible diagnosis: Asthma flare-up or pneumonia. Urge medical help."},
            {'text': "No", 'result': "Possible diagnosis: Common cold. Suggest tea and tissues."}
        ]
    },
    'stomach1': {
        'question': "Is there abdominal pain or cramping?",
        'options': [
            {'text': "Yes", 'next': "stomach2"},
            {'text': "No", 'result': "Possible diagnosis: Mild nausea, maybe from motion sickness. Suggest ginger ale."}
        ]
    },
    'stomach2': {
        'question': "Have you eaten something unusual recently?",
        'options': [
            {'text': "Yes", 'result': "Possible diagnosis: Food poisoning. Recommend bland foods and hydration."},
            {'text': "No", 'next': "stomach3"}
        ]
    },
    'stomach3': {
        'question': "Any blood in vomit or stool?",
        'options': [
            {'text': "Yes", 'result': "Possible diagnosis: Serious issue like ulcer - seek immediate help."},
            {'text': "No", 'result': "Possible diagnosis: Stomach flu or indigestion. Suggest antacids and light meals."}
        ]
    }
}

DATABASE_FILE = pathlib.Path('/app/databases/sessions.db')

def init_db():
    DATABASE_FILE.unlink(missing_ok=True)

    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (session_id TEXT PRIMARY KEY, current_node TEXT, result TEXT, score REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS answers 
                 (session_id TEXT, node TEXT, question TEXT, answer_text TEXT, created_at DATETIME,
                  PRIMARY KEY (session_id, node))''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/api/start', methods=['GET'])
def start():
    session_id = str(uuid.uuid4())
    current_node = 'start'
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO sessions VALUES (?, ?, ?, ?)', (session_id, current_node, None, None))
    conn.commit()
    conn.close()
    return get_question(session_id)

@app.route('/api/answer', methods=['GET'])
def answer():
    session_id = request.args.get('session_id')
    choice = int(request.args.get('choice'))
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT current_node FROM sessions WHERE session_id = ?', (session_id,))
    row = c.fetchone()
    if row is None:
        conn.close()
        return jsonify({'error': 'Session not found'}), 404
    current_node = row[0]
    node = decision_tree[current_node]
    option = node['options'][choice]
    # Store the answer
    c.execute('INSERT INTO answers VALUES (?, ?, ?, ?, ?)',
              (session_id, current_node, node['question'], option['text'], datetime.datetime.now()))
    conn.commit()
    if 'result' in option:
        # TODO do a calculation for score
        c.execute('UPDATE sessions SET result = ?, score = ? WHERE session_id = ?', (option['result'], 1.5, session_id,))
        conn.commit()
        conn.close()
        return jsonify({'result': option['result']})
    else:
        new_node = option['next']
        c.execute('UPDATE sessions SET current_node = ? WHERE session_id = ?', (new_node, session_id))
        conn.commit()
        conn.close()
        return get_question(session_id)

def get_question(session_id):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('SELECT current_node FROM sessions WHERE session_id = ?', (session_id,))
    current_node = c.fetchone()[0]
    conn.close()
    node = decision_tree[current_node]
    return jsonify({
        'question': node['question'],
        'options': [opt['text'] for opt in node['options']],
        'session_id': session_id
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)