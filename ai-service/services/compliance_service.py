from datetime import datetime, timezone
from typing import Any, Dict, List


class ComplianceService:
    def __init__(self, prompt_service, groq_client, chroma_service):
        self._prompt_service = prompt_service
        self._groq_client = groq_client
        self._chroma_service = chroma_service

    @staticmethod
    def _fallback_describe(text: str) -> Dict[str, Any]:
        return {
            "description": f"Fallback description for input: {text[:140]}",
            "risk_level": "medium",
            "is_fallback": True,
        }

    @staticmethod
    def _fallback_recommend() -> Dict[str, Any]:
        return {
            "recommendations": [
                {"action_type": "review", "description": "Review current controls.", "priority": "high"},
                {"action_type": "implement", "description": "Implement missing safeguards.", "priority": "medium"},
                {"action_type": "monitor", "description": "Monitor outcomes weekly.", "priority": "low"},
            ],
            "is_fallback": True,
        }

    @staticmethod
    def _fallback_report(text: str) -> Dict[str, Any]:
        return {
            "title": "Fallback Compliance Report",
            "summary": f"Fallback summary generated for: {text[:120]}",
            "overview": "AI provider unavailable, using deterministic template.",
            "key_items": ["Stabilize controls", "Schedule review", "Track actions"],
            "recommendations": [
                {"action_type": "review", "description": "Perform manual validation.", "priority": "high"}
            ],
            "is_fallback": True,
        }

    def _build_prompt(self, prompt_file: str, record_text: str) -> str:
        prompt_template = self._prompt_service.load(prompt_file)
        context = self._chroma_service.query_context(record_text, limit=3)
        context_block = "\n".join(f"- {item}" for item in context) if context else "- No additional context"
        return prompt_template.format(record=record_text, context=context_block)

    def describe(self, record_text: str) -> Dict[str, Any]:
        prompt = self._build_prompt("summary_prompt.txt", record_text)
        try:
            payload = self._groq_client.complete_json(prompt)
            payload["is_fallback"] = False
        except Exception:
            payload = self._fallback_describe(record_text)
        payload["generated_at"] = datetime.now(timezone.utc).isoformat()
        return payload

    def recommend(self, record_text: str) -> Dict[str, Any]:
        prompt = self._build_prompt("compliance_prompt.txt", record_text)
        try:
            payload = self._groq_client.complete_json(prompt)
            recs: List[Dict[str, str]] = payload.get("recommendations", [])
            payload["recommendations"] = recs[:3]
            payload["is_fallback"] = False
        except Exception:
            payload = self._fallback_recommend()
        payload["generated_at"] = datetime.now(timezone.utc).isoformat()
        return payload

    def generate_report(self, record_text: str) -> Dict[str, Any]:
        prompt = self._build_prompt("risk_analysis_prompt.txt", record_text)
        try:
            payload = self._groq_client.complete_json(prompt)
            payload["is_fallback"] = False
        except Exception:
            payload = self._fallback_report(record_text)
        payload["generated_at"] = datetime.now(timezone.utc).isoformat()
        return payload
