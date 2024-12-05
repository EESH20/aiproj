from flask import Flask, request, jsonify
import sqlite3
import openai

# Initialize Flask app
app = Flask(__name__)

# OpenAI API key
openai.api_key = "your-openai-api-key"

# Chat function
def generate_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# API endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("user_input")

    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    bot_response = generate_response(user_input)

    # Save to database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat (user_input, bot_response)
        VALUES (?, ?)
    ''', (user_input, bot_response))
    conn.commit()
    conn.close()

    return jsonify({"user_input": user_input, "bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
