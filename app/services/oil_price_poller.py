import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.oil_price_service import OilPriceService

logger = logging.getLogger("uvicorn.error")

class OilPricePoller:
    def __init__(self, db: AsyncIOMotorDatabase, poll_interval_hours: int = 24):
        self.db = db
        self.interval = poll_interval_hours * 3600
        self._task: Optional[asyncio.Task] = None
        self._running = False
        self.stats: Dict[str, Any] = {
            "last_poll_time": None,
            "poll_count": 0,
            "last_price": None,
            "last_status": "initialized"
        }

    async def start(self):
        """Start the background 24-hour daily price refresh task."""
        self._running = True
        self._task = asyncio.create_task(self._poll_loop())
        logger.info(f"Daily OilPricePoller started (interval: {self.interval}s / 24h).")

    async def stop(self):
        """Gracefully terminate the poller task."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Daily OilPricePoller stopped.")

    async def _poll_loop(self):
        # Initial stabilization pause
        await asyncio.sleep(3)
        while self._running:
            try:
                await self.poll_once()
            except Exception as e:
                logger.error(f"Error during daily oil price sync: {e}")
                self.stats["last_status"] = f"error: {str(e)}"
            
            # Sleep for 24 hours
            await asyncio.sleep(self.interval)

    async def poll_once(self) -> Optional[Dict[str, Any]]:
        """
        Executes a single daily refresh cycle.
        """
        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")

        logger.info(f"Checking real-time Brent crude oil prices for {today_str}...")
        res = await OilPriceService.sync_and_store_daily_price(self.db)
        if res:
            self.stats["last_poll_time"] = now.isoformat()
            self.stats["poll_count"] += 1
            self.stats["last_price"] = res.get("price")
            self.stats["last_status"] = "success"
            logger.info(f"OilPricePoller completed daily refresh. Current Brent price: ${res.get('price')}/bbl")
            return res
        else:
            self.stats["last_status"] = "fetch_failed"
            logger.warning("OilPricePoller failed to fetch fresh price; preserved existing database cache.")
            return None
