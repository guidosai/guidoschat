from flask import Flask, request, render_template_string, session, redirect, url_for
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "guidos_chat_secret"

client = OpenAI()


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

<form method="POST" action="/chat">
<input name="message" placeholder="Escribe tu mensaje" required>
<button>Enviar</button>
</form>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template_string(chat_template, messages=session.get("chat_history", []))

@app.route("/chat", methods=["POST"])
def chat(): 

    if "chat_history" not in session:
        session["chat_history"] = []

    user_message = request.form.get("message")

    system_prompt = """
    Actua como una estrategia de negocios y crecimiento personal enfocado en latinoamerica.
    Tu objetivo es ayudar al usauario a generar mas ingresos, mejorar su disciplina y pensar como empresario.
    Responde de forma clara, directa y estructurada. Incluye pasos accionables.
    Evita respuestas genericas.
    habla con seguridad y mentalidad de crecimiento.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )


    bot_reply = response.output_text

    session["chat_history"].append(("user", user_message))
    session["chat_history"].append(("bot", bot_reply))

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))) 

