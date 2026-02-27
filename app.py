from flask import Flask, request, jsonify
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# 🔐 Inicializar Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    numero = data.get("phone")
    mensagem = data.get("text", {}).get("message")
    data_hora = datetime.now()

    # Documento a ser salvo
    registro = {
        "numero": numero,
        "mensagem": mensagem,
        "data_recebimento": data_hora,
        "json_bruto": data
    }

    # Salva na coleção "conversas"
    db.collection("conversas").add(registro)

    return jsonify({"status": "salvo no firebase"}), 200


import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)