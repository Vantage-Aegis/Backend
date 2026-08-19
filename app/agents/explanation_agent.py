import json
import logging
from typing import Dict, Any
from app.utils.llm_client import call_gemini_api

logger = logging.getLogger("uvicorn.error")

def generate_fallback_explanation(scenario_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic narrative fallback if Gemini API is unreachable or rate limited.
    """
    risk_score = scenario_data.get("risk", {}).get("score", 88.0)
    risk_cat = scenario_data.get("risk", {}).get("category", "Critical")
    deficit = scenario_data.get("supply_impact", {}).get("deficit_bpd", 1974000)
    price_impact = scenario_data.get("supply_impact", {}).get("price_impact_pct", 18.5)
    coverage_days = scenario_data.get("reserve_plan", {}).get("days_of_coverage", 6.2)
    avg_draw = scenario_data.get("reserve_plan", {}).get("drawdown_bpd_avg", 320000)

    alternatives = scenario_data.get("alternatives", [])
    top_supplier = alternatives[0]["supplier"] if alternatives else "UAE & Russia"

    return {
        "executive_summary": (
            f"A severe supply chain disruption creates an estimated daily crude deficit of {deficit:,} bpd, "
            f"elevating the national energy vulnerability score to {risk_score} ({risk_cat}). "
            f"Immediate crude spot price volatility is projected at +{price_impact}%."
        ),
        "why_risky": (
            f"Heavy reliance on maritime chokepoints (42% via Hormuz) exposes refining hubs to acute bottlenecks. "
            f"Corridor disruption directly cuts crude inflows to western Indian ports."
        ),
        "why_recommended": (
            f"Rerouting procurement toward non-disrupted suppliers such as {top_supplier} via bypass terminals "
            f"(e.g., Fujairah pipeline or Cape route) offers optimal landed cost and lowest transit disruption risk."
        ),
        "reserve_rationale": (
            f"Authorizing strategic reserves at an average draw rate of ~{avg_draw:,} bpd secures a {coverage_days}-day "
            f"operational buffer, allowing replacement shipments from alternative global suppliers to complete transit."
        ),
        "key_assumptions": [
            "Alternative maritime suppliers can scale export capacity within 5 to 7 days.",
            "Strategic reserve offloading infrastructure maintains nominal discharge rates.",
            "No secondary chokepoints experience simultaneous military blockades."
        ],
        "uncertainties": [
            "Real-world spot market price premiums during geopolitical crisis escalations.",
            "Tanker charter availability and surge war-risk insurance rates.",
            "Short-term refinery yield adjustments for varying crude gravity blends."
        ],
        "model_used": "deterministic-fallback"
    }

async def generate_explanation(scenario_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates an executive AI narrative explanation of simulation results using Gemini API.
    """
    system_instruction = (
        "You are an energy-security analyst assistant. You are given fully computed, "
        "verified numerical data about an oil supply chain disruption. Do NOT invent or alter "
        "any numbers. Respond ONLY with valid JSON matching this schema:\n"
        "{\n"
        '  "executive_summary": "string",\n'
        '  "why_risky": "string",\n'
        '  "why_recommended": "string",\n'
        '  "reserve_rationale": "string",\n'
        '  "key_assumptions": ["string"],\n'
        '  "uncertainties": ["string"]\n'
        "}"
    )

    prompt = f"Here is the verified disruption scenario dataset:\n{json.dumps(scenario_data, indent=2)}\nProvide the executive brief."

    raw_response = await call_gemini_api(prompt, system_instruction)

    if raw_response:
        try:
            parsed = json.loads(raw_response)
            parsed["model_used"] = "gemini-2.5-flash"
            return parsed
        except Exception as err:
            logger.error(f"Failed to parse Gemini response as JSON: {err}. Raw response: {raw_response[:200]}")

    return generate_fallback_explanation(scenario_data)
