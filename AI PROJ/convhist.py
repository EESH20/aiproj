import sqlite3

from flask import app, jsonify, request, session

from app import generate_response


@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    data = request.json
    user_input = data.get("user_input")
    user_id = session['user_id']

    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    bot_response = generate_response(user_input)

    # Save to database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat (user_id, user_input, bot_response)
        VALUES (?, ?, ?)
    ''', (user_id, user_input, bot_response))
    conn.commit()
    conn.close()

    return jsonify({"user_input": user_input, "bot_response": bot_response})
@app.route('/history', methods=['GET'])
def history():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    user_id = session['user_id']

    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_input, bot_response, timestamp FROM chat WHERE user_id = ? ORDER BY timestamp ASC', (user_id,))
    history = cursor.fetchall()
    conn.close()

    return jsonify([
        {"user_input": row[0], "bot_response": row[1], "timestamp": row[2]}
        for row in history
    ])

