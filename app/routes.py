from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service


pages = Blueprint("pages", __name__)


api = Blueprint("api", __name__)


@pages.route("/")
def index():
    return render_template("index.html")


@pages.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api.route("/sohbet", methods=["POST"])
def sohbet():

    data = request.get_json()

    if not data:
        return jsonify({
            "basari": False,
            "mesaj": "Geçerli bir JSON verisi gönderilmelidir."
        }), 400

    mesaj = data.get("mesaj")
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "mesaj": "Mesaj alanı zorunludur."
        }), 400

    try:
        cevap = ai_service.yanit_uret(
            mesaj=mesaj,
            gecmis=gecmis
        )

        return jsonify({
            "basari": True,
            "cevap": cevap
        })

    except AIServiceError as error:
        return jsonify({
            "basari": False,
            "mesaj": str(error)
        }), 503


@api.route("/leads", methods=["POST"])
def lead_olustur():


    data = request.get_json()

    if not data:
        return jsonify({
            "basari": False,
            "mesaj": "Geçerli bir JSON verisi gönderilmelidir."
        }), 400

    isim = data.get("isim")
    telefon = data.get("telefon")
    mesaj = data.get("mesaj", "")

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "mesaj": "İsim ve telefon alanları zorunludur."
        }), 400

    try:
        lead_ekle(
            isim=isim,
            telefon=telefon,
            mesaj=mesaj
        )

        return jsonify({
            "basari": True,
            "mesaj": "Bilgileriniz başarıyla kaydedildi."
        }), 201

    except Exception:
        return jsonify({
            "basari": False,
            "mesaj": "Bilgiler kaydedilirken bir hata oluştu."
        }), 500


@api.route("/leads", methods=["GET"])
def leadleri_getir():

    try:
        leads = tum_leadler()

        sonuc = []

        for lead in leads:
            sonuc.append({
                "id": lead["id"],
                "isim": lead["isim"],
                "telefon": lead["telefon"],
                "mesaj": lead["mesaj"],
                "tarih": lead["tarih"]
            })

        return jsonify({
            "basari": True,
            "leadler": sonuc
        })

    except Exception:
        return jsonify({
            "basari": False,
            "mesaj": "Kayıtlar alınırken bir hata oluştu."
        }), 500