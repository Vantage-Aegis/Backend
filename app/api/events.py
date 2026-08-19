import uuid
from typing import List
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.schemas.event import EventCreateRequest, EventResponse
from app.agents.event_classifier_agent import classify_event

router = APIRouter(prefix="/api/events", tags=["Risk Events"])

@router.get("", response_model=List[EventResponse])
async def get_events(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Returns active geopolitical and logistics risk events.
    """
    cursor = db.risk_events.find({})
    docs = await cursor.to_list(length=100)
    result = []
    for d in docs:
        result.append(EventResponse(
            id=d["_id"],
            title=d["title"],
            corridor=d.get("corridor", "Strait of Hormuz"),
            severity=d.get("severity", 50),
            source=d.get("source", "manual"),
            category=d.get("category", "sanctions"),
            description=d.get("description", ""),
            confidence=d.get("confidence"),
            needs_review=d.get("needs_review")
        ))
    return result

@router.post("", response_model=EventResponse)
async def create_event(req: EventCreateRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Ingests a new risk event headline. Utilizes LLM classifier if auto-enrichment needed.
    """
    classified = await classify_event(req.title, req.description or "")
    
    event_id = f"evt_{uuid.uuid4().hex[:6]}"
    severity = req.severity if req.severity is not None else classified.get("severity", 50)
    confidence = classified.get("confidence", 1.0)
    needs_review = confidence < 0.5
    
    doc = {
        "_id": event_id,
        "title": req.title,
        "corridor": req.corridor or classified["corridor"],
        "severity": severity,
        "source": req.source or classified["source"],
        "category": req.category or classified["category"],
        "description": req.description or "",
        "confidence": confidence,
        "needs_review": needs_review
    }

    await db.risk_events.insert_one(doc)

    if not needs_review:
        from app.api.risk import get_risk
        # Trigger risk recomputation for the affected corridor
        try:
            await get_risk(entity_type="corridor", entity_id=doc["corridor"], db=db)
        except Exception:
            pass

    return EventResponse(
        id=event_id,
        title=doc["title"],
        corridor=doc["corridor"],
        severity=doc["severity"],
        source=doc["source"],
        category=doc["category"],
        description=doc["description"],
        confidence=doc.get("confidence"),
        needs_review=doc.get("needs_review")
    )
