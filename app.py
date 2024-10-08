from flask import Flask, request, jsonify, send_from_directory
from assistant_manager import AssistantManager
from models import AssistantResponse
import os

app = Flask(__name__, static_folder='./dist')
assistant_manager = AssistantManager()

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message') 

    if not user_id or not message:
        return jsonify({"error": "Missing user_id or message"}), 400

    response: AssistantResponse = assistant_manager.send_message(user_id, message)
    return jsonify(response.dict())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))