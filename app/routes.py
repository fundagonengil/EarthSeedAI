from flask import Blueprint, jsonify, request, render_template

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError


api_bp = Blueprint("api", __name__)
page_bp = Blueprint("pages", __name__)


@page_bp.route("/")
def home():
    return render_template("index.html")


@page_bp.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@page_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json(silent=True) or {}

    mesaj = data.get("mesaj", "").strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alani zorunludur."
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        }), 200

    except AIServiceError:
        return jsonify({
            "basari": False,
            "hata": "Yapay zeka servisine su anda ulasilamiyor."
        }), 503


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    data = request.get_json(silent=True) or {}

    isim = data.get("isim", "").strip()
    telefon = data.get("telefon", "").strip()
    mesaj = data.get("mesaj", "").strip()

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "Isim ve telefon alanlari zorunludur."
        }), 400

    lead_ekle(isim, telefon, mesaj)

    return jsonify({
        "basari": True,
        "mesaj": "Kaydiniz basariyla alindi."
    }), 201


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
    leads = tum_leadler()

    lead_listesi = []

    for lead in leads:
        lead_listesi.append({
            "id": lead["id"],
            "isim": lead["isim"],
            "telefon": lead["telefon"],
            "mesaj": lead["mesaj"],
            "tarih": lead["tarih"]
        })

    return jsonify({
        "basari": True,
        "leadler": lead_listesi
    }), 200