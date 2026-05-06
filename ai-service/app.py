from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from config import Config
from routes.compliance_routes import compliance_bp
from routes.health_routes import health_bp
from services.cache_service import CacheService
from services.chroma_service import ChromaService
from services.compliance_service import ComplianceService
from services.groq_client import GroqClient
from services.metrics_service import MetricsService
from services.prompt_service import PromptService


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    prompt_service = PromptService(str(Path(__file__).parent / "prompts"))
    groq_client = GroqClient(
        api_key=app.config["GROQ_API_KEY"],
        base_url=app.config["GROQ_BASE_URL"],
        model=app.config["GROQ_MODEL"],
        timeout_seconds=app.config["GROQ_TIMEOUT_SECONDS"],
    )
    cache_service = CacheService(app.config["REDIS_URL"])
    metrics_service = MetricsService()
    chroma_service = ChromaService(
        persist_dir=app.config["CHROMA_PERSIST_DIR"],
        collection_name=app.config["CHROMA_COLLECTION"],
        embedding_model=app.config["EMBEDDING_MODEL"],
    )
    compliance_service = ComplianceService(prompt_service, groq_client, chroma_service)

    app.extensions["cache_service"] = cache_service
    app.extensions["metrics_service"] = metrics_service
    app.extensions["chroma_service"] = chroma_service
    app.extensions["compliance_service"] = compliance_service

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none';"
        return response

    app.register_blueprint(compliance_bp)
    app.register_blueprint(health_bp)
    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host=Config.APP_HOST, port=Config.APP_PORT, debug=Config.DEBUG)
