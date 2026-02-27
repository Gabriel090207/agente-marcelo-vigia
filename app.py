from flask import Flask, request, jsonify
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# =========================
# 🔐 Inicializar Firebase
# =========================
firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("FIREBASE_CREDENTIALS não configurado no ambiente.")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

# =========================
# 🔥 WEBHOOK Z-API
# =========================
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)

        numero = data.get("phone")
        message_id = data.get("messageId")
        tipo = data.get("type")
        from_me = data.get("fromMe")
        timestamp = data.get("time")
        nome_contato = data.get("senderName")

        mensagem = None

        if tipo == "text":
            mensagem = data.get("text", {}).get("message")
        elif tipo == "image":
            mensagem = "📷 Imagem recebida"
        elif tipo == "audio":
            mensagem = "🎧 Áudio recebido"
        elif tipo == "video":
            mensagem = "🎥 Vídeo recebido"
        else:
            mensagem = "Tipo não identificado"

        registro = {
            "numero": numero,
            "message_id": message_id,
            "tipo": tipo,
            "from_me": from_me,
            "nome_contato": nome_contato,
            "timestamp_zapi": timestamp,
            "data_recebimento_servidor": datetime.now(),
            "mensagem": mensagem,
            "ultima_atualizacao": firestore.SERVER_TIMESTAMP
        }

        # 🔥 Usa o número como ID do documento
        db.collection("conversas").document(numero).set(registro)

        return jsonify({"status": "atualizado com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# =========================
# 📡 API PARA O FRONTEND
# =========================
@app.route('/api/conversas', methods=['GET'])
def listar_conversas():
    conversas_ref = db.collection("conversas") \
        .order_by("ultima_atualizacao", direction=firestore.Query.DESCENDING) \
        .stream()

    resultado = []

    for doc in conversas_ref:
        dados = doc.to_dict()
        dados["id"] = doc.id
        resultado.append(dados)

    return jsonify(resultado), 200


# =========================
# 🏠 ROTA HOME
# =========================
@app.route('/')
def home():
    return "Agente Marcelo Vigia ONLINE 🚀", 200


# =========================
# 🚀 START
# =========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)