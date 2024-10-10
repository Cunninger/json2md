from flask import Flask, render_template, request, send_file, session, jsonify
import json
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'uuidiamadmin12345grttvfdbgdgfdg'  # 设置一个安全的密钥

def format_timestamp(timestamp):
    if timestamp:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return '未知时间'

def process_content(content):
    content = re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', content)
    content = re.sub(r'\$(.*?)\$', r'\$$\1\$$', content)
    return content

def format_chat(json_data):
    data = json.loads(json_data)
    formatted_chat = []

    messages = data.get('messages', [])

    for message in messages:
        author = message.get('author', {})
        role = author.get('role')
        content = message.get('content', {}).get('parts', [''])[0]
        timestamp = message.get('create_time')

        processed_content = process_content(content)

        if role == 'user':
            formatted_message = f"### 用户 ({format_timestamp(timestamp)}):\n\n{processed_content}\n"
        elif role == 'assistant':
            formatted_message = f"### GPT ({format_timestamp(timestamp)}):\n\n{processed_content}\n"
        elif role == 'tool':
            tool_name = author.get('name', '未知工具')
            formatted_message = f"### {tool_name} ({format_timestamp(timestamp)}):\n\n{processed_content}\n"
        else:
            continue

        formatted_chat.append(formatted_message)

    return "\n".join(formatted_chat)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'usage_count' not in session:
        session['usage_count'] = 0

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and file.filename.endswith('.json'):
            json_data = file.read().decode('utf-8')
            formatted_md = format_chat(json_data)
            session['usage_count'] += 1
            return jsonify({
                'markdown': formatted_md,
                'usage_count': session['usage_count']
            })
    return render_template('index.html', usage_count=session['usage_count'])

@app.route('/get_usage_count', methods=['GET'])
def get_usage_count():
    return jsonify({'usage_count': session.get('usage_count', 0)})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
