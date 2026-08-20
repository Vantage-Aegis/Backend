import asyncio
import logging
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import httpx

from app.agents.event_classifier_agent import classify_event
from app.services.risk_engine import calculate_risk

logger = logging.getLogger("uvicorn.error")

USER_AGENT = "VantageResiliencePlatform/1.0 (Energy Security Analyst Intelligence Feed)"

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

    async def _fetch_gdelt_articles(self) -> List[Dict[str, str]]:
        """Attempt to fetch from GDELT DOC API v2"""
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": "oil OR crude OR tanker OR Hormuz OR Red Sea OR pipeline OR sanctions",
            "mode": "artlist",
            "maxrecords": 25,
            "format": "json"
        }
        headers = {"User-Agent": USER_AGENT}
        
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                articles = data.get("articles", [])
                return [{"title": a.get("title", ""), "url": a.get("url", "")} for a in articles if a.get("title")]
            else:
                logger.warning(f"GDELT API status {resp.status_code}, falling back to RSS feed.")
                return []

    async def _fetch_rss_articles(self) -> List[Dict[str, str]]:
        """Fallback live news fetcher using Google News RSS feed for crude oil/maritime supply chain"""
        url = "https://news.google.com/rss/search?q=oil+crude+tanker+Hormuz+Red+Sea+sanctions&hl=en-US&gl=US&ceid=US:en"
        headers = {"User-Agent": USER_AGENT}
        
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                try:
                    root = ET.fromstring(resp.text)
                    items = root.findall(".//item")
                    articles = []
                    for item in items[:25]:
                        title_elem = item.find("title")
                        link_elem = item.find("link")
                        if title_elem is not None and title_elem.text:
                            raw_title = title_elem.text.strip()
                            # Clean source suffix like "- Reuters" or "- Bloomberg"
                            title = raw_title.rsplit(" - ", 1)[0] if " - " in raw_title else raw_title
                            link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                            articles.append({"title": title, "url": link})
                    return articles
                except Exception as ex:
                    logger.error(f"Error parsing RSS XML: {ex}")
            return []

    async def poll_once(self):
        """Single poll iteration trying GDELT first, falling back to RSS"""
        now = datetime.now(timezone.utc)
        articles = []
        source_name = "gdelt_auto"

        # 1. Try GDELT
        try:
            articles = await self._fetch_gdelt_articles()
        except Exception as e:
            logger.warning(f"GDELT fetch failed: {e}")

        # 2. Fallback to RSS if GDELT returned 0 articles or rate-limited
        if not articles:
            try:
                articles = await self._fetch_rss_articles()
                source_name = "live_news_rss"
            except Exception as e:
                logger.error(f"RSS fetch failed: {e}")

        if not articles:
            logger.info("No live news articles fetched during poll iteration.")
            self.stats["last_poll_time"] = now.isoformat()
            self.stats["events_last_poll"] = 0
            return

        events_processed = 0

        for article in articles:
            url = article.get("url", "")
            title = article.get("title", "")

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
                "classifier_result": classified
            })

            # Store in risk_events collection
            event_id = f"evt_live_{uuid.uuid4().hex[:8]}"
            event_doc = {
                "_id": event_id,
                "title": title,
                "corridor": classified.get("corridor", "Strait of Hormuz"),
                "category": classified.get("category", "conflict"),
                "severity": classified.get("severity", 50),
                "source": source_name,
                "confidence": confidence,
                "needs_review": needs_review,
                "description": f"Live news article: {url}",
                "ingested_at": now.isoformat()
            }

            await self.db.risk_events.insert_one(event_doc)

            # Trigger risk recomputation if valid confidence
            if not needs_review:
                await self._recompute_risk(classified.get("corridor", "Strait of Hormuz"))

            events_processed += 1

        self.stats["total_processed"] += events_processed
        self.stats["last_poll_time"] = now.isoformat()
        self.stats["events_last_poll"] = events_processed

        logger.info(f"Live news poll complete: {events_processed} new events ingested (source: {source_name})")

    async def _recompute_risk(self, corridor_name: str):
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
        except Exception as e:
            logger.error(f"Risk recomputation failed for {corridor_name}: {e}")
