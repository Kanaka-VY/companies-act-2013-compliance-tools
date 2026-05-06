from flask import Blueprint, current_app, jsonify


health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    metrics = current_app.extensions["metrics_service"]
    cache_service = current_app.extensions["cache_service"]
    chroma_service = current_app.extensions["chroma_service"]
    return jsonify(
        {
            "status": "ok",
            "model": current_app.config["GROQ_MODEL"],
            "avg_response_time_ms": metrics.avg_response_ms(),
            "uptime_seconds": metrics.uptime_seconds(),
            "cache_enabled": cache_service.enabled,
            "domain_docs_loaded": chroma_service.count(),
        }
    )
