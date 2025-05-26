from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ TikTok Video Generator is running!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    question = data.get("question", "No question provided.")
    # (Ici tu pourras mettre la logique de génération plus tard)
    return jsonify({"message": f"Video for '{question}' is being generated."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
