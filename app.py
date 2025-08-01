from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Información personal
PERSONAL_INFO = """
Soy Juan, tengo 20 años, estudio Big Data, me interesa el backend, la inteligencia artificial y el análisis de datos.
He desarrollado proyectos con React, Python, Laravel y scraping de datos.
Pregúntame sobre mis estudios, gustos o proyectos.
"""

# Cargar variables de entorno (.env local)
load_dotenv()

# Obtener API Key desde entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Mostrar en consola para verificar
print("🔑 API KEY al iniciar:", OPENROUTER_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("userMessage", "")
    
    print("📩 Mensaje recibido del usuario:", user_message)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",  # o dominio en producción
        "X-Title": "IA Personal Juan"
    }

    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {
                "role": "system",
                "content": f"Eres un asistente que responde preguntas sobre Juan, responde especificamente a lo que te pida con cordialidad pero sin excederte en el mensaje, al inicio de los mensajes antes de la respuesta da un saludo que pueda variar entre buenos días, gracias por preguntar entre otros que consideres. Aquí están sus datos:\n{PERSONAL_INFO}"
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    # Logs de depuración
    print("🔐 Encabezado Authorization:", headers["Authorization"])
    print("📤 Payload JSON enviado:", json.dumps(payload, indent=2))

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        print("✅ Respuesta recibida:", reply)
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ Error:", e)
        if hasattr(e, 'response') and e.response is not None:
            print("➡️ Detalles del error:", e.response.text)
        return jsonify({"reply": "Lo siento, ha ocurrido un error al generar la respuesta."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3001)
