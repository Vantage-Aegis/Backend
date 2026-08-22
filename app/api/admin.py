import uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Header
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from bson.errors import InvalidId
from bson import ObjectId

from app.database import get_db
from app.services.twin_service import propagate_disruption
from app.config import get_settings

router = APIRouter(prefix="/api/admin", tags=["Admin"])

class LoginRequest(BaseModel):
    password: str

LOCAL_ADMIN_SESSIONS = {}

async def get_admin_user(authorization: Optional[str] = Header(None), db: AsyncIOMotorDatabase = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    
    session = None
    try:
        session = await db.admin_sessions.find_one({"token": token})
    except Exception:
        pass
        
    if not session:
        session = LOCAL_ADMIN_SESSIONS.get(token)
        
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    if session["expires_at"] < datetime.now(timezone.utc).isoformat():
        raise HTTPException(status_code=401, detail="Token expired")
        
    return "admin"

@router.post("/login")
async def login(req: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    settings = get_settings()
    if req.password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token = str(uuid.uuid4())
    expires = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
    
    session_doc = {
        "token": token,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": expires
    }
    
    LOCAL_ADMIN_SESSIONS[token] = session_doc
    try:
        await db.admin_sessions.insert_one(session_doc)
    except Exception:
        pass
    
    return {"token": token, "expires_at": expires}

@router.get("/approvals")
async def get_approvals(db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    approvals = await db.status_approvals.find({}).sort("created_at", -1).to_list(100)
    for a in approvals:
        a["_id"] = str(a["_id"])
    return approvals

@router.post("/approvals/{approval_id}/{action}")
async def process_approval(approval_id: str, action: str, db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    if action not in ["approve", "reject", "undo"]:
        raise HTTPException(status_code=400, detail="Invalid action")
        
    try:
        obj_id = ObjectId(approval_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    approval = await db.status_approvals.find_one({"_id": obj_id})
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
        
    if action == "approve":
        edge_ids = approval.get("affected_edges", [])
        severity = approval.get("severity", 5)
        is_reopen = approval.get("status") == "pending_reopen"
        
        for edge_id in edge_ids:
            route = await db.routes.find_one({"_id": edge_id})
            if route:
                if is_reopen:
                    target_status = route.get("previous_status", "active")
                    if target_status == "blocked":
                        target_status = "active"
                    await db.routes.update_one({"_id": edge_id}, {"$set": {"status": target_status}})
                else:
                    new_status = "blocked" if severity >= 5 else "degraded"
                    await db.routes.update_one({"_id": edge_id}, {"$set": {"status": new_status, "previous_status": route.get("status", "active")}})
        
        await db.status_approvals.update_one({"_id": obj_id}, {"$set": {"status": "approved", "updated_at": datetime.now(timezone.utc).isoformat()}})
        
    elif action == "reject":
        await db.status_approvals.update_one({"_id": obj_id}, {"$set": {"status": "rejected", "updated_at": datetime.now(timezone.utc).isoformat()}})
        
    elif action == "undo":
        current_app_status = approval.get("status")
        edge_ids = approval.get("affected_edges", [])
        
        if current_app_status == "rejected":
            orig_status = "pending_reopen" if "reopen" in approval.get("title", "").lower() or "clear:" in approval.get("title", "").lower() else "pending"
            await db.status_approvals.update_one({"_id": obj_id}, {"$set": {"status": orig_status, "updated_at": datetime.now(timezone.utc).isoformat()}})
        else:
            for edge_id in edge_ids:
                route = await db.routes.find_one({"_id": edge_id})
                if route:
                    prev = route.get("previous_status", "active")
                    if route.get("status") == "blocked" and prev == "blocked":
                        prev = "active"
                    await db.routes.update_one({"_id": edge_id}, {"$set": {"status": prev}})
                    
            await db.status_approvals.update_one({"_id": obj_id}, {"$set": {"status": "undone", "updated_at": datetime.now(timezone.utc).isoformat()}})

    return {"status": "success"}

@router.get("/config")
async def get_config(db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    config = await db.system_config.find_one({"_id": "main_config"})
    if not config:
        config = {
            "critical_severity_threshold": 80,
            "auto_approve_confidence_threshold": 0.95,
            "blacklisted_keywords": []
        }
    return config

@router.put("/config")
async def update_config(new_config: dict, db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    await db.system_config.update_one(
        {"_id": "main_config"},
        {"$set": new_config},
        upsert=True
    )
    return {"status": "success"}

@router.get("/system")
async def get_system_health(db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    state = await db.system_state.find_one({"_id": "news_poller"})
    return state or {"last_poll_time": None}

@router.delete("/news/{news_id}")
async def delete_news(news_id: str, db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    # Deleting from risk_events
    await db.risk_events.delete_one({"_id": news_id})
    return {"status": "success"}

@router.get("/entities")
async def get_entities(db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    corridors = await db.corridors.find({}).to_list(100)
    suppliers = await db.suppliers.find({}).to_list(100)
    ports = await db.ports.find({}).to_list(100)
    routes = await db.routes.find({}).to_list(100)

    # Determine status for corridors based on routes
    for c in corridors:
        c_routes = [r for r in routes if r.get("corridor_id") == c["_id"] or r.get("corridor") == c.get("name")]
        c["status"] = "blocked" if any(r.get("status") == "blocked" for r in c_routes) else "active"
        
    for s in suppliers:
        s_routes = [r for r in routes if r.get("supplier_id") == s["_id"] or r.get("supplier") == s.get("name")]
        s["status"] = "blocked" if any(r.get("status") == "blocked" for r in s_routes) else "active"
        
    for p in ports:
        p_routes = [r for r in routes if r.get("dest_port_id") == p["_id"] or r.get("dest_port") == p.get("name")]
        p["status"] = "blocked" if any(r.get("status") == "blocked" for r in p_routes) else "active"

    return {
        "corridors": [{"id": c["_id"], "name": c["name"], "status": c["status"]} for c in corridors],
        "suppliers": [{"id": s["_id"], "name": s["name"], "status": s["status"]} for s in suppliers],
        "ports": [{"id": p["_id"], "name": p.get("name", p.get("port", "Unknown")), "status": p["status"]} for p in ports]
    }

@router.post("/entities/{entity_type}/{entity_id}/toggle")
async def toggle_entity(entity_type: str, entity_id: str, db: AsyncIOMotorDatabase = Depends(get_db), _: str = Depends(get_admin_user)):
    routes = await db.routes.find({}).to_list(100)
    
    if entity_type == "corridor":
        affected_routes = [r for r in routes if r.get("corridor_id") == entity_id or str(r.get("corridor_id", "")) == entity_id]
    elif entity_type == "supplier":
        affected_routes = [r for r in routes if r.get("supplier_id") == entity_id or str(r.get("supplier_id", "")) == entity_id]
    elif entity_type == "port":
        affected_routes = [r for r in routes if r.get("dest_port_id") == entity_id or str(r.get("dest_port_id", "")) == entity_id]
    else:
        raise HTTPException(status_code=400, detail="Invalid entity type")
        
    # Determine new status based on current status of first affected route
    if not affected_routes:
        return {"status": "success", "message": "No routes found for this entity"}
        
    currently_blocked = any(r.get("status") == "blocked" for r in affected_routes)
    
    for r in affected_routes:
        if currently_blocked:
            # Unblock
            await db.routes.update_one({"_id": r["_id"]}, {"$set": {"status": r.get("previous_status", "active")}})
        else:
            # Block
            await db.routes.update_one({"_id": r["_id"]}, {"$set": {"status": "blocked", "previous_status": r.get("status", "active")}})
            
    # Also log an approval to keep a paper trail
    approval_doc = {
        "corridor_id": entity_id if entity_type == "corridor" else None,
        "corridor_name": f"{entity_type.capitalize()} Override",
        "title": f"Manual Admin Override: {'UNBLOCKED' if currently_blocked else 'BLOCKED'} {entity_id}",
        "severity": 0 if currently_blocked else 100,
        "confidence": 1.0,
        "affected_edges": [r["_id"] for r in affected_routes],
        "status": "approved",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    await db.status_approvals.insert_one(approval_doc)
            
    return {"status": "success", "blocked": not currently_blocked}
