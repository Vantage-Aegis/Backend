import logging
import httpx
from typing import Dict, Any, Optional
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")

async def call_gemini_api(prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
    """
    Calls the Gemini API (using REST endpoint with API key) to generate content.
    Returns response string or None if API key is missing/failed.
    """
    settings = get_settings()
    api_key = settings.GEMINI_API_KEY

    if not api_key or api_key == "your_gemini_api_key_here":
        logger.warning("Gemini API key is not configured. Falling back to deterministic narrative builder.")
        return None

    # Official Google AI Studio REST Endpoint for Gemini Flash
    model_name = settings.LLM_MODEL or "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    
    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }
    
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    async def _call_api(current_payload):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=current_payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                else:
                    logger.error(f"Gemini API call returned HTTP status {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.error(f"Error communicating with Gemini API: {e}")
        return None

    result = await _call_api(payload)
    
    if result:
        import json
        try:
            json.loads(result)
            return result
        except json.JSONDecodeError:
            # Retry once with modified prompt
            current_prompt_text = payload["contents"][0]["parts"][0]["text"]
            payload["contents"][0]["parts"][0]["text"] = current_prompt_text + "\n\nReturn valid JSON only."
            return await _call_api(payload)
            
    return result
