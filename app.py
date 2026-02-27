from flask import Flask, request, jsonify
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)

# 🔐 Inicializar Firebase via variável de ambiente
firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("FIREBASE_CREDENTIALS não configurado no ambiente.")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)

        numero = data.get("phone")
        mensagem = data.get("text", {}).get("message")
        data_hora = datetime.now()

        registro = {
            "numero": numero,
            "mensagem": mensagem,
            "data_recebimento": data_hora,
            "json_bruto": data
        }

        db.collection("conversas").add(registro)

        return jsonify({"status": "salvo no firebase"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/')
def home():
    return "Agente Marcelo Vigia ONLINE 🚀", 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)