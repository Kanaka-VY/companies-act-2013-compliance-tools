import time

from flask import Blueprint, current_app, jsonify, request


compliance_bp = Blueprint("compliance", __name__)


def _validate_input(payload: dict):
    if not payload:
        return "Body is required."
    record = payload.get("record")
    if not isinstance(record, str) or not record.strip():
        return "Field 'record' must be a non-empty string."
    return None


@compliance_bp.post("/describe")
def describe():
    payload = request.get_json(silent=True) or {}
    error = _validate_input(payload)
    if error:
        return jsonify({"error": error}), 400

    start = time.perf_counter()
    cache_service = current_app.extensions["cache_service"]
    compliance_service = current_app.extensions["compliance_service"]
    cache_key = cache_service.build_key("describe", payload)

    cached = cache_service.get_json(cache_key)
    if cached:
        return jsonify(cached), 200

    result = compliance_service.describe(payload["record"])
    cache_service.set_json(cache_key, result, current_app.config["CACHE_TTL_SECONDS"])
    current_app.extensions["metrics_service"].record((time.perf_counter() - start) * 1000)
    return jsonify(result), 200


@compliance_bp.post("/recommend")
def recommend():
    payload = request.get_json(silent=True) or {}
    error = _validate_input(payload)
    if error:
        return jsonify({"error": error}), 400

    start = time.perf_counter()
    cache_service = current_app.extensions["cache_service"]
    compliance_service = current_app.extensions["compliance_service"]
    cache_key = cache_service.build_key("recommend", payload)

    cached = cache_service.get_json(cache_key)
    if cached:
        return jsonify(cached), 200

    result = compliance_service.recommend(payload["record"])
    cache_service.set_json(cache_key, result, current_app.config["CACHE_TTL_SECONDS"])
    current_app.extensions["metrics_service"].record((time.perf_counter() - start) * 1000)
    return jsonify(result), 200


@compliance_bp.post("/generate-report")
def generate_report():
    payload = request.get_json(silent=True) or {}
    error = _validate_input(payload)
    if error:
        return jsonify({"error": error}), 400

    start = time.perf_counter()
    cache_service = current_app.extensions["cache_service"]
    compliance_service = current_app.extensions["compliance_service"]
    cache_key = cache_service.build_key("generate-report", payload)

    cached = cache_service.get_json(cache_key)
    if cached:
        return jsonify(cached), 200

    result = compliance_service.generate_report(payload["record"])
    cache_service.set_json(cache_key, result, current_app.config["CACHE_TTL_SECONDS"])
    current_app.extensions["metrics_service"].record((time.perf_counter() - start) * 1000)
    return jsonify(result), 200
