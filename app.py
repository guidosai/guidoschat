from flask import Flask, request, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "guidos_chat_secret"

client = OpenAI()

chat_history = []

chat_template = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Guidos Chat</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #eef2f7;
    display: flex;
    justify-content: center;
}
.chat-box {
    width: 100%;
    max-width: 500px;
    background: white;
    padding: 15px;
    margin-top: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
h2 {
    text-align: center;
}
.user {
    background: #007bff;
    color: white;
    padding: 10px;
    border-radius: 15px;
    margin: 5px 0;
    text-align: right;
}
.bot {
    background: #28a745;
    color: white;
    padding: 10px;
    border-radius: 15px;
    margin: 5px 0;
    text-align: left;
}
form {
    display: flex;
    margin-top: 10px;
}
input {
    flex: 1;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
}
button {
    padding: 10px 15px;
    margin-left: 5px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}
button:hover {
    background: #0056b3;
}
</style>
</head>
<body>
<div class="chat-box">
<h2>🤖 Guidos Chat</h2>

{% for role, msg in messages %}
<div class="{{ role }}">{{ msg }}</div>
{% endfor %}

<form method="post" action="/chat">
<input name="message" placeholder="Escribe tu mensaje" required>
<button>Enviar</button>
</form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(chat_template, messages=chat_history)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=user_message
    )

    bot_reply = response.output_text

    chat_history.append(("user", user_message))
    chat_history.append(("bot", bot_reply))

    return render_template_string(chat_template, messages=chat_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

