import logging
from flask import Blueprint, jsonify, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)
page_bp = Blueprint("page", __name__)


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    data = request.get_json(silent=True) or {}

    mesaj = str(data.get("mesaj", "")).strip()
    gecmis = data.get("gecmis", [])

    # AI chatbot mesajı geldiyse
    if mesaj and not data.get("isim") and not data.get("telefon"):
        try:
            cevap = ai_service.yanit_uret(
                mesaj,
                gecmis
            )

            return jsonify({
                "basari": True,
                "cevap": cevap
            }), 200

        except AIServiceError as e:
            logger.error(f"AI HATASI: {e}", exc_info=True)

            return jsonify({
                "basari": False,
                "hata": "AI yaniti alinamadi."
            }), 500

    # Gerçek lead kaydı
    isim = str(data.get("isim", "")).strip()
    telefon = str(data.get("telefon", "")).strip()

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "Isim ve telefon alanlari zorunludur."
        }), 400

    try:
        lead_ekle(isim, telefon, mesaj)

        return jsonify({
            "basari": True,
            "mesaj": "Kaydiniz basariyla alindi."
        }), 201

    except Exception as e:
        logger.error(
            f"VERITABANI HATASI: {e}",
            exc_info=True
        )

        return jsonify({
            "basari": False,
            "hata": "Sunucu hatasi olustu."
        }), 500


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
    try:
        veriler = tum_leadler()

        return jsonify({
            "status": "success",
            "data": veriler
        }), 200

    except Exception as e:
        logger.error(
            f"DASHBOARD GET HATASI: {e}",
            exc_info=True
        )

        return jsonify({
            "status": "error",
            "message": "Veriler alinamadi."
        }), 500