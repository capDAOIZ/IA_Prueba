from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Puedes modificar y extender esta info
PERSONAL_INFO = """
Soy Juan, tengo 20 años, estudio Big Data, me interesa el backend, la inteligencia artificial y el análisis de datos.
He desarrollado proyectos con React, Python, Laravel y scraping de datos.
Pregúntame sobre mis estudios, gustos o proyectos.
"""

# Tu API Key de OpenRouter
OPENROUTER_API_KEY = "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"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("userMessage", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",  # o tu dominio cuando lo tengas
        "X-Title": "IA Personal Juan"              # nombre para ranking en OpenRouter
    }

    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {
                "role": "system",
                "content": f"Eres un asistente que responde preguntas sobre Juan, responde especificamente a lo que te pida con cordialidad pero sin excederte en el mensaje, al inicio de los mensajes antes de la respuesta da un saludo que pueda varia entre buenos dias, gracias por preguntar entre otros que consideres. Aquí están sus datos:\n{PERSONAL_INFO}"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ Error:", e)
        if hasattr(e, 'response') and e.response is not None:
            print("➡️ Detalles del error:", e.response.text)
        return jsonify({"reply": "Lo siento, ha ocurrido un error al generar la respuesta."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3001)
