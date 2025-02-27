import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Ensure the API key is set via environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is missing!")

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# Configure genai library
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

@app.route('/')
def home():
    return "Flask Server is Running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = chat_session.send_message(user_message)
        return jsonify({"response": response.text})  # Proper JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
