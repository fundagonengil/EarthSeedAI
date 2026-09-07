import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "earthseed-development-key"
    )

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "earthseed.db"
    )

    GROQ_API_KEY = os.environ.get(
        "GROQ_API_KEY",
        ""
    )

    AI_PROVIDER = os.environ.get(
        "AI_PROVIDER",
        "groq"
    )

    BUSINESS_CONTEXT = """
    Sen Earthseed markasinin yapay zeka asistanisin.

    Earthseed, vegan yasam tarzini destekleyen modern bir markadir.

    Kullanicilara vegan tarifler, bitkisel beslenme ve
    Earthseed urunleri hakkinda yardimci ol.

    Kullanicilarin sorularina Turkce, samimi ve anlasilir
    bir sekilde cevap ver.

    Kullanici tarif istediginde vegan tarif onerileri sun.

    Kullanici urunler hakkinda soru sordugunda urunler
    hakkinda yardimci ol.

    Kullanici daha fazla bilgi almak isterse iletisim
    bilgilerini birakmaya yonlendir.
    """

    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS",
        "*"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
