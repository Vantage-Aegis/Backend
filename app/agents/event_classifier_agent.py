import json
import logging
from typing import Dict, Any
from app.utils.llm_client import call_gemini_api

logger = logging.getLogger("uvicorn.error")

async def classify_event(raw_title: str, description: str = "") -> Dict[str, Any]:
    """
    Parses a raw geopolitical event headline into structured risk event fields.
    """
    system_instruction = (
        "You are a geopolitical risk classifier. Given a news headline or event description, "
        "extract the primary affected maritime corridor, event category, and estimated severity (0 to 100). "
        "Respond ONLY with valid JSON matching:\n"
        '{"corridor": "Strait of Hormuz"|"Red Sea / Bab-el-Mandeb"|"Cape of Good Hope Route", '
        '"category": "sanctions"|"conflict"|"shipping_attack"|"diplomatic"|"other", '
        '"severity": int, "confidence": float}'
    )

    prompt = f"Title: {raw_title}\nDescription: {description}"
    raw = await call_gemini_api(prompt, system_instruction)

    if raw:
        try:
            parsed = json.loads(raw)
            return {
                "title": raw_title,
                "corridor": parsed.get("corridor", "Strait of Hormuz"),
                "category": parsed.get("category", "conflict"),
                "severity": int(parsed.get("severity", 50)),
                "confidence": float(parsed.get("confidence", 1.0)),
                "source": "llm_classified",
                "description": description
            }
        except Exception as e:
            logger.error(f"Event classification JSON parse error: {e}")

    # Fallback default mapping
    corridor = "Strait of Hormuz" if "hormuz" in raw_title.lower() else "Red Sea / Bab-el-Mandeb" if "red sea" in raw_title.lower() or "houthi" in raw_title.lower() else "Cape of Good Hope Route"
    return {
        "title": raw_title,
        "corridor": corridor,
        "category": "conflict" if "attack" in raw_title.lower() else "sanctions" if "sanction" in raw_title.lower() else "diplomatic",
        "severity": 60,
        "source": "manual",
        "description": description
    }
