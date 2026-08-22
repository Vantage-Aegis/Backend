import asyncio
import logging
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
import httpx

from app.agents.event_classifier_agent import classify_event
from app.services.risk_engine import calculate_risk
from app.services.twin_service import propagate_disruption

logger = logging.getLogger("uvicorn.error")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

IRRELEVANT_KEYWORDS = [
    "cooking oil", "olive oil", "palm oil", "essential oil", "hair oil", 
    "mustard oil", "vegetable oil", "canola oil", "coconut oil", "nursing home", 
    "medicaid", "fifa", "world cup", "soccer", "football", "baseball", 
    "basketball", "cricket", "nfl", "nba", "movie", "hollywood", "actor", "actress"
]

def is_relevant_headline(title: str) -> bool:
    if not title or len(title) < 8:
        return False
    t_lower = title.lower()
    for kw in IRRELEVANT_KEYWORDS:
        if kw in t_lower:
            return False
    return True

class GdeltNewsPoller:
    def __init__(self, db, poll_interval_minutes: int = 15):
        self.db = db
        self.interval = poll_interval_minutes * 60
        self._task: Optional[asyncio.Task] = None
        self._running = False
        self.stats = {"total_processed": 0, "last_poll_time": None, "events_last_poll": 0}

    async def start(self):
        """Start the background polling loop"""
        self._running = True
        self._task = asyncio.create_task(self._poll_loop())
        logger.info(f"Live news poller started (interval: {self.interval}s)")

    async def stop(self):
        """Graceful shutdown"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Live news poller stopped.")

    async def _poll_loop(self):
        # Brief initial delay to let MongoDB connections stabilize
        await asyncio.sleep(2)
        while self._running:
            try:
                await self.poll_once()
            except Exception as e:
                logger.error(f"News poll error: {e}")
            await asyncio.sleep(self.interval)

    async def _fetch_gdelt_articles(self) -> List[Dict[str, Any]]:
        """Attempt to fetch from GDELT DOC API v2 with resilient timeout and 429 handling"""
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "(\"crude oil\" OR \"oil tanker\" OR \"Strait of Hormuz\" OR \"Red Sea\" OR \"oil sanctions\")",
            "mode": "artlist",
            "maxrecords": 25,
            "format": "json",
            "timespan": "24h"
        }
        headers = {"User-Agent": USER_AGENT}
        
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(url, params=params, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    articles = data.get("articles", [])
                    res = []
                    for a in articles:
                        title = a.get("title", "")
                        if title and is_relevant_headline(title):
                            seen_date = a.get("seendate")
                            pub_dt = None
                            if seen_date and len(seen_date) >= 8:
                                try:
                                    pub_dt = datetime.strptime(seen_date[:8], "%Y%m%d").replace(tzinfo=timezone.utc)
                                except Exception:
                                    pass
                            res.append({
                                "title": title,
                                "url": a.get("url", ""),
                                "pub_dt": pub_dt or datetime.now(timezone.utc),
                                "source": "GDELT"
                            })
                    return res
                elif resp.status_code == 429:
                    logger.info("GDELT API rate-limited (429), switching to live Google News RSS feed.")
                    return []
                else:
                    logger.warning(f"GDELT API returned status {resp.status_code}, falling back to RSS feed.")
                    return []
        except (httpx.TimeoutException, httpx.RequestError) as e:
            logger.info(f"GDELT API unreachable/timed out ({type(e).__name__}), falling back to RSS feed.")
            return []

    async def _fetch_rss_articles(self, days: int = 2) -> List[Dict[str, Any]]:
        """Fallback live news fetcher using Google News RSS feed with strict recency operators"""
        from email.utils import parsedate_to_datetime

        query = "(%22crude+oil%22+OR+%22oil+tanker%22+OR+%22Strait+of+Hormuz%22+OR+%22Red+Sea%22+OR+%22Bab+el-Mandeb%22+OR+%22oil+sanctions%22+OR+%22Russian+oil%22+OR+%22Iranian+oil%22)"
        url = f"https://news.google.com/rss/search?q={query}+when:{days}d&hl=en-US&gl=US&ceid=US:en"
        headers = {"User-Agent": USER_AGENT}
        
        try:
            async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    try:
                        root = ET.fromstring(resp.text)
                        items = root.findall(".//item")
                        articles = []
                        for item in items[:30]:
                            title_elem = item.find("title")
                            link_elem = item.find("link")
                            pub_elem = item.find("pubDate")
                            if title_elem is not None and title_elem.text:
                                raw_title = title_elem.text.strip()
                                title = raw_title.rsplit(" - ", 1)[0] if " - " in raw_title else raw_title
                                if not is_relevant_headline(title):
                                    continue
                                link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                                pub_dt = datetime.now(timezone.utc)
                                if pub_elem is not None and pub_elem.text:
                                    try:
                                        pub_dt = parsedate_to_datetime(pub_elem.text.strip())
                                    except Exception:
                                        pass
                                articles.append({
                                    "title": title,
                                    "url": link,
                                    "pub_dt": pub_dt,
                                    "source": "Live News"
                                })
                        return articles
                    except Exception as ex:
                        logger.error(f"Error parsing RSS XML: {ex}")
        except Exception as ex:
            logger.error(f"Error requesting RSS feed: {ex}")
        return []

    async def poll_once(self):
        """Single poll iteration trying GDELT first, falling back to RSS"""
        now = datetime.now(timezone.utc)
        articles = []
        source_name = "GDELT"

        # Check downtime from system_state
        state = await self.db.system_state.find_one({"_id": "news_poller"})
        last_poll = state.get("last_poll_time") if state else None
        
        rss_days = 2
        if last_poll:
            try:
                last_dt = datetime.fromisoformat(last_poll)
                diff = now - last_dt
                if diff.days > 2:
                    rss_days = min(7, diff.days + 1)
                    logger.info(f"Downtime detected ({diff.days} days). Backfilling news with when:{rss_days}d")
            except Exception:
                pass
                
        # 1. Try GDELT (with 24h timespan)
        try:
            articles = await self._fetch_gdelt_articles()
        except Exception as e:
            logger.warning(f"GDELT fetch failed: {e}")

        # 2. Fallback to RSS
        if not articles:
            try:
                articles = await self._fetch_rss_articles(days=rss_days)
                source_name = "Live News"
            except Exception as e:
                logger.error(f"RSS fetch ({rss_days}d) failed: {e}")

        # 3. Fallback to RSS (last 7 days) if returned nothing
        if not articles and rss_days < 7:
            try:
                articles = await self._fetch_rss_articles(days=7)
                source_name = "Live News (7d)"
            except Exception as e:
                logger.error(f"RSS fetch (7d) failed: {e}")

        if not articles:
            logger.info("No live news articles fetched during poll iteration.")
            await self.db.system_state.update_one({"_id": "news_poller"}, {"$set": {"last_poll_time": now.isoformat()}}, upsert=True)
            self.stats["last_poll_time"] = now.isoformat()
            self.stats["events_last_poll"] = 0
            return

        events_processed = 0

        for article in articles:
            url = article.get("url", "")
            title = article.get("title", "")
            pub_dt = article.get("pub_dt", now)

            if not title or len(title) < 5:
                continue

            # Deduplicate by URL or title
            existing = await self.db.processed_articles.find_one({
                "$or": [{"url": url}, {"title": title}]
            })
            if existing:
                continue

            # Classify headline via Gemini LLM agent (or fallback)
            try:
                classified = await classify_event(title, "")
            except Exception as e:
                logger.error(f"Classification failed for '{title[:30]}...': {e}")
                continue

            confidence = classified.get("confidence", 0.9)
            needs_review = confidence < 0.5

            # Store in processed_articles
            await self.db.processed_articles.insert_one({
                "url": url,
                "title": title,
                "processed_at": now.isoformat(),
                "published_at": pub_dt.isoformat() if hasattr(pub_dt, "isoformat") else str(pub_dt),
                "classifier_result": classified
            })

            # Store in risk_events collection
            event_id = f"evt_live_{uuid.uuid4().hex[:8]}"
            date_str = pub_dt.strftime("%b %d, %Y") if hasattr(pub_dt, "strftime") else now.strftime("%b %d, %Y")
            event_doc = {
                "_id": event_id,
                "title": title,
                "corridor": classified.get("corridor", "Strait of Hormuz"),
                "category": classified.get("category", "conflict"),
                "severity": classified.get("severity", 50),
                "source": article.get("source", source_name),
                "confidence": confidence,
                "needs_review": needs_review,
                "description": f"Live news article: {url}",
                "ingested_at": now.isoformat(),
                "published_at": pub_dt.isoformat() if hasattr(pub_dt, "isoformat") else str(pub_dt),
                "date": date_str
            }

            await self.db.risk_events.insert_one(event_doc)

            # Trigger risk recomputation if valid confidence
            if not needs_review:
                await self._recompute_risk(classified.get("corridor", "Strait of Hormuz"), confidence, title)

            events_processed += 1

        await self.db.system_state.update_one({"_id": "news_poller"}, {"$set": {"last_poll_time": now.isoformat()}}, upsert=True)
        self.stats["total_processed"] += events_processed
        self.stats["last_poll_time"] = now.isoformat()
        self.stats["events_last_poll"] = events_processed

        logger.info(f"Live news poll complete: {events_processed} new events ingested (source: {source_name})")

    async def _recompute_risk(self, corridor_name: str, last_confidence: float = 0.9, last_title: str = ""):
        """Trigger risk recalculation for the affected corridor"""
        try:
            corridor = await self.db.corridors.find_one({"name": corridor_name})
            if not corridor:
                return

            base_risk = corridor.get("base_risk", 50.0)
            share_pct = corridor.get("share_of_india_imports_pct", 30.0)

            events = await self.db.risk_events.find({"corridor": corridor_name}).to_list(100)
            avg_severity = sum(e.get("severity", 50) for e in events) / len(events) if events else base_risk

            result = calculate_risk({
                "shipping_disruption": base_risk,
                "geopolitical_tension": avg_severity,
                "corridor_dependency": share_pct * 1.5
            }, entity_type="corridor")

            await self.db.risk_scores.update_one(
                {"entity_type": "corridor", "entity_id": corridor["_id"]},
                {"$set": {
                    "score": result["score"],
                    "category": result["category"],
                    "factors": result["factors"],
                    "computed_at": datetime.now(timezone.utc).isoformat()
                }},
                upsert=True
            )
            
            # Check against admin threshold
            config = await self.db.system_config.find_one({"_id": "main_config"}) or {}
            threshold = config.get("critical_severity_threshold", 80)
            auto_conf = config.get("auto_approve_confidence_threshold", 0.95)
            
            if avg_severity >= threshold:
                # Deduplication logic: Check if there's already an approval for this corridor in the last 24h
                cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
                existing = await self.db.status_approvals.find_one({
                    "corridor_id": corridor["_id"],
                    "created_at": {"$gte": cutoff},
                    "status": {"$in": ["pending", "auto_applied", "approved"]}
                })
                
                if not existing:
                    logger.info(f"Critical severity {avg_severity} reached for {corridor_name}. Generating status approval.")
                    
                    routes = await self.db.routes.find({}).to_list(100)
                    refineries = await self.db.refineries.find({}).to_list(100)
                    suppliers = await self.db.suppliers.find({}).to_list(100)
                    
                    affected = propagate_disruption(corridor_id=corridor["_id"], severity=int(avg_severity/20), routes=routes, refineries=refineries, suppliers=suppliers)
                    
                    status = "auto_applied" if last_confidence >= auto_conf else "pending"
                    
                    approval_doc = {
                        "corridor_id": corridor["_id"],
                        "corridor_name": corridor_name,
                        "title": last_title,
                        "severity": avg_severity,
                        "confidence": last_confidence,
                        "affected_edges": affected.get("edges", []),
                        "status": status,
                        "created_at": datetime.now(timezone.utc).isoformat(),
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                    
                    res = await self.db.status_approvals.insert_one(approval_doc)
                    
                    if status == "auto_applied":
                        logger.info(f"Auto-applying disruption to routes due to high confidence ({last_confidence}).")
                        edge_ids = affected.get("edges", [])
                        for edge_id in edge_ids:
                            route = next((r for r in routes if r["_id"] == edge_id), None)
                            if route:
                                new_status = "blocked" if avg_severity >= 90 else "degraded"
                                await self.db.routes.update_one({"_id": edge_id}, {"$set": {"status": new_status, "previous_status": route.get("status", "active")}})
                                
            else:
                # Automated reopening logic: if severity is low but routes are blocked
                routes = await self.db.routes.find({"$or": [{"corridor_id": corridor["_id"]}, {"corridor": corridor_name}]}).to_list(100)
                blocked_routes = [r["_id"] for r in routes if r.get("status") in ["blocked", "degraded"]]
                
                if blocked_routes:
                    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
                    existing = await self.db.status_approvals.find_one({
                        "corridor_id": corridor["_id"],
                        "created_at": {"$gte": cutoff},
                        "status": "pending_reopen"
                    })
                    
                    if not existing:
                        logger.info(f"Severity dropped to {avg_severity} for {corridor_name}. Generating reopen approval.")
                        approval_doc = {
                            "corridor_id": corridor["_id"],
                            "corridor_name": corridor_name,
                            "title": f"CLEAR: {last_title}" if last_title else f"CLEAR: Safety restored for {corridor_name}",
                            "severity": avg_severity,
                            "confidence": last_confidence,
                            "affected_edges": blocked_routes,
                            "status": "pending_reopen",
                            "created_at": datetime.now(timezone.utc).isoformat(),
                            "updated_at": datetime.now(timezone.utc).isoformat()
                        }
                        await self.db.status_approvals.insert_one(approval_doc)

        except Exception as e:
            logger.error(f"Risk recomputation failed for {corridor_name}: {e}")
