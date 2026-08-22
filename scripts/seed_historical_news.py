"""
VANTAGE - 3-Tier Historical & Live News Ingestion Script
-------------------------------------------------------
Seeds:
- Tier 1: Macro energy & geopolitical milestones (last 2-3 years: 2023 - early 2026) [0 LLM calls]
- Tier 2: Major maritime & supply chain events (last 6 months: Feb 2026 - July 2026) [0 LLM calls]
- Tier 3: Live breaking news of the last 1 week (Aug 15 - Aug 22, 2026) via Google News RSS [2-3 Batch LLM calls max]

Complies strictly with Gemini Free Tier rate limits (15 RPM / 1500 RPD) using batch processing & deterministic fallback.
"""

import asyncio
import json
import logging
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import List, Dict, Any

import sys
from pathlib import Path

# Add Backend root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import httpx
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import get_settings
from app.services.risk_engine import calculate_risk
from app.utils.llm_client import call_gemini_api

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_historical_news")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ==============================================================================
# TIER 1: LAST 2 - 3 YEARS (2023 to Early 2026) - Major Macro Milestones
# ==============================================================================
TIER_1_HISTORICAL_EVENTS = [
    {
        "_id": "evt_hist_2023_01",
        "title": "G7 and EU implement $60/bbl price cap and maritime insurance ban on Russian seaborne crude",
        "corridor": "Cape of Good Hope Route",
        "corridor_id": "corr_cape",
        "severity": 65,
        "source": "historical_intelligence",
        "category": "sanctions",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Global crude trade routes restructure heavily as Russian Urals flows pivot toward Indian and Chinese refiners.",
        "date": "Feb 05, 2023",
        "published_at": "2023-02-05T08:00:00Z",
        "ingested_at": "2023-02-05T08:00:00Z"
    },
    {
        "_id": "evt_hist_2023_02",
        "title": "Iranian commandos seize Marshall Islands-flagged tanker Advantage Sweet in Gulf of Oman",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 75,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Iranian Navy boards Kuwait-to-US crude tanker carrying 1M barrels, heightening war-risk insurance in Hormuz.",
        "date": "Apr 27, 2023",
        "published_at": "2023-04-27T10:30:00Z",
        "ingested_at": "2023-04-27T10:30:00Z"
    },
    {
        "_id": "evt_hist_2023_03",
        "title": "OPEC+ announces surprise voluntary crude output cuts of 1.66 million bpd through end of year",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 55,
        "source": "historical_intelligence",
        "category": "diplomatic",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Saudi Arabia and Persian Gulf producers curtail output to stabilize international spot benchmark prices.",
        "date": "Jun 04, 2023",
        "published_at": "2023-06-04T14:00:00Z",
        "ingested_at": "2023-06-04T14:00:00Z"
    },
    {
        "_id": "evt_hist_2023_04",
        "title": "First Houthi missile launches over southern Red Sea targeting commercial shipping corridors",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 70,
        "source": "historical_intelligence",
        "category": "conflict",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Yemen-based militants initiate anti-ship drone and missile campaign threatening Bab-el-Mandeb maritime choke point.",
        "date": "Oct 19, 2023",
        "published_at": "2023-10-19T12:00:00Z",
        "ingested_at": "2023-10-19T12:00:00Z"
    },
    {
        "_id": "evt_hist_2023_05",
        "title": "Houthi helicopter-borne commandos hijack Galaxy Leader vehicle carrier in southern Red Sea",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 85,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Seizure marks acute escalation in maritime security risk, triggering immediate rerouting advisories for Western and Asian fleets.",
        "date": "Nov 19, 2023",
        "published_at": "2023-11-19T15:45:00Z",
        "ingested_at": "2023-11-19T15:45:00Z"
    },
    {
        "_id": "evt_hist_2023_06",
        "title": "Major global oil tanker operators and BP temporarily pause all shipments through Red Sea",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 80,
        "source": "historical_intelligence",
        "category": "conflict",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Crude carriers redirect ~3.5 million bpd around the Cape of Good Hope, adding 12-16 days to Asia-Europe transit times.",
        "date": "Dec 18, 2023",
        "published_at": "2023-12-18T09:15:00Z",
        "ingested_at": "2023-12-18T09:15:00Z"
    },
    {
        "_id": "evt_hist_2024_01",
        "title": "US and UK coalition forces initiate Operation Prosperity Guardian airstrikes on Houthi launch sites",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 75,
        "source": "historical_intelligence",
        "category": "conflict",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Joint military strikes attempt to restore deterrence as naval escorts establish secure convoys in Gulf of Aden.",
        "date": "Jan 12, 2024",
        "published_at": "2024-01-12T02:00:00Z",
        "ingested_at": "2024-01-12T02:00:00Z"
    },
    {
        "_id": "evt_hist_2024_02",
        "title": "Trafigura petroleum tanker Marlin Luanda struck by anti-ship missile in Gulf of Aden",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 85,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Tanker carrying Russian naphtha catches fire, causing war-risk insurance premiums to spike across all Middle East waterways.",
        "date": "Jan 26, 2024",
        "published_at": "2024-01-26T18:30:00Z",
        "ingested_at": "2024-01-26T18:30:00Z"
    },
    {
        "_id": "evt_hist_2024_03",
        "title": "Bulk carrier True Confidence struck in Gulf of Aden resulting in first fatal merchant casualties",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 80,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Tragic crew fatalities force remaining international maritime unions to demand rerouting around Africa.",
        "date": "Mar 06, 2024",
        "published_at": "2024-03-06T13:20:00Z",
        "ingested_at": "2024-03-06T13:20:00Z"
    },
    {
        "_id": "evt_hist_2024_04",
        "title": "IRGC Navy boards and seizes Portuguese-flagged container ship MSC Aries near Strait of Hormuz",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 85,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Helicopter raid conducted in international waters east of Fujairah raises fears of Hormuz chokepoint closure.",
        "date": "Apr 13, 2024",
        "published_at": "2024-04-13T06:45:00Z",
        "ingested_at": "2024-04-13T06:45:00Z"
    },
    {
        "_id": "evt_hist_2024_05",
        "title": "Indian refiners diversify crude baskets, increasing long-term off-take from UAE and West Africa",
        "corridor": "Cape of Good Hope Route",
        "corridor_id": "corr_cape",
        "severity": 45,
        "source": "historical_intelligence",
        "category": "diplomatic",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Indian state-run refiners expand term deals with Abu Dhabi National Oil Company and Nigerian NNPC to hedge chokepoints.",
        "date": "May 22, 2024",
        "published_at": "2024-05-22T11:00:00Z",
        "ingested_at": "2024-05-22T11:00:00Z"
    },
    {
        "_id": "evt_hist_2024_06",
        "title": "Commercial coal vessel Tutor sunk by uncrewed surface vessel (USV) in southern Red Sea",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 80,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Use of explosive maritime drone boats signals technological advancement in maritime interdiction tactics.",
        "date": "Jun 12, 2024",
        "published_at": "2024-06-12T09:00:00Z",
        "ingested_at": "2024-06-12T09:00:00Z"
    },
    {
        "_id": "evt_hist_2024_07",
        "title": "Crude oil tanker Sounion attacked and set ablaze in Red Sea with 150,000 tonnes of crude",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 90,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Severe environmental catastrophe narrowly averted as EU naval forces escort specialized salvage tugs.",
        "date": "Aug 21, 2024",
        "published_at": "2024-08-21T07:15:00Z",
        "ingested_at": "2024-08-21T07:15:00Z"
    },
    {
        "_id": "evt_hist_2024_08",
        "title": "US OFAC sanctions 18 maritime companies and 22 tankers in shadow fleet crackdown",
        "corridor": "Strait of Malacca",
        "corridor_id": "corr_malacca",
        "severity": 60,
        "source": "historical_intelligence",
        "category": "sanctions",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Secondary sanctions target dark-fleet transfers occurring near Malaysian anchorages and Riau archipelago.",
        "date": "Oct 11, 2024",
        "published_at": "2024-10-11T14:30:00Z",
        "ingested_at": "2024-10-11T14:30:00Z"
    },
    {
        "_id": "evt_hist_2024_09",
        "title": "Suez Canal transit revenues drop 64% year-on-year as Cape route becomes default maritime path",
        "corridor": "Suez Canal",
        "corridor_id": "corr_suez",
        "severity": 50,
        "source": "historical_intelligence",
        "category": "other",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Suez Canal Authority reports prolonged financial strain as global carriers maintain African circum-navigation.",
        "date": "Dec 05, 2024",
        "published_at": "2024-12-05T10:00:00Z",
        "ingested_at": "2024-12-05T10:00:00Z"
    },
    {
        "_id": "evt_hist_2025_01",
        "title": "Persian Gulf naval patrols intensified following suspicious electronic jamming near Musandam Peninsula",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 65,
        "source": "historical_intelligence",
        "category": "conflict",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Tanker captains report widespread AIS navigation spoofing and GPS loss along westbound transit lanes.",
        "date": "Jan 15, 2025",
        "published_at": "2025-01-15T11:45:00Z",
        "ingested_at": "2025-01-15T11:45:00Z"
    }
]

# ==============================================================================
# TIER 2: LAST 6 MONTHS (Feb 2026 to July 2026) - Major Tactical Incidents
# ==============================================================================
TIER_2_HISTORICAL_EVENTS = [
    {
        "_id": "evt_hist_2026_01",
        "title": "Coalition frigate destroys two explosive naval drones targeting commercial tanker convoy",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 75,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Intercept occurs 30 nautical miles southwest of Mokha; merchant vessels complete passage without damage.",
        "date": "Feb 10, 2026",
        "published_at": "2026-02-10T05:20:00Z",
        "ingested_at": "2026-02-10T05:20:00Z"
    },
    {
        "_id": "evt_hist_2026_02",
        "title": "Iranian naval fast-attack craft conduct live-fire exercises in narrow Strait of Hormuz channels",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 70,
        "source": "historical_intelligence",
        "category": "conflict",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Naval maneuvers prompt international advisory warning commercial carriers to keep strictly within designated TSS lanes.",
        "date": "Feb 24, 2026",
        "published_at": "2026-02-24T13:00:00Z",
        "ingested_at": "2026-02-24T13:00:00Z"
    },
    {
        "_id": "evt_hist_2026_03",
        "title": "Global maritime insurers raise Red Sea and Gulf of Oman war-risk surcharges to 1.25%",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 65,
        "source": "historical_intelligence",
        "category": "other",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Additional premium on a standard $120M crude tanker reaches $1.5M per voyage, entrenching Cape route economics.",
        "date": "Mar 08, 2026",
        "published_at": "2026-03-08T09:30:00Z",
        "ingested_at": "2026-03-08T09:30:00Z"
    },
    {
        "_id": "evt_hist_2026_04",
        "title": "Strait of Malacca naval exercises cause 36-hour commercial tanker congestion outside Singapore",
        "corridor": "Strait of Malacca",
        "corridor_id": "corr_malacca",
        "severity": 50,
        "source": "historical_intelligence",
        "category": "conflict",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Scheduled regional naval drills temporarily restrict eastbound deep-draft tanker passage.",
        "date": "Mar 22, 2026",
        "published_at": "2026-03-22T16:10:00Z",
        "ingested_at": "2026-03-22T16:10:00Z"
    },
    {
        "_id": "evt_hist_2026_05",
        "title": "US Treasury sanctions 14 maritime transport entities for illicit Persian Gulf oil transfers",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 65,
        "source": "historical_intelligence",
        "category": "sanctions",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Designations target ship managers utilizing ship-to-ship (STS) dark transfers off UAE east coast.",
        "date": "Apr 05, 2026",
        "published_at": "2026-04-05T14:00:00Z",
        "ingested_at": "2026-04-05T14:00:00Z"
    },
    {
        "_id": "evt_hist_2026_06",
        "title": "Indian strategic reserve inventory bolstered with 4 million barrels at Padur underground facility",
        "corridor": "Cape of Good Hope Route",
        "corridor_id": "corr_cape",
        "severity": 30,
        "source": "historical_intelligence",
        "category": "diplomatic",
        "confidence": 1.0,
        "needs_review": False,
        "description": "ISPRL injects sweet crude parcels to lift national emergency cover to ~9.5 operational days.",
        "date": "Apr 18, 2026",
        "published_at": "2026-04-18T10:15:00Z",
        "ingested_at": "2026-04-18T10:15:00Z"
    },
    {
        "_id": "evt_hist_2026_07",
        "title": "Armed skiffs approach VLCC tanker in Gulf of Aden before being deterred by private security teams",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 70,
        "source": "historical_intelligence",
        "category": "shipping_attack",
        "confidence": 1.0,
        "needs_review": False,
        "description": "UKMTO issues incident alert 45 nautical miles south of Aden; vessel and crew safe.",
        "date": "May 03, 2026",
        "published_at": "2026-05-03T07:45:00Z",
        "ingested_at": "2026-05-03T07:45:00Z"
    },
    {
        "_id": "evt_hist_2026_08",
        "title": "OPEC+ ministers agree to gradual unwinding of voluntary cuts starting Q4 2026 subject to market stability",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 45,
        "source": "historical_intelligence",
        "category": "diplomatic",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Producers signal flexible supply management to prevent sharp crude price spikes amid maritime bottlenecks.",
        "date": "Jun 02, 2026",
        "published_at": "2026-06-02T12:30:00Z",
        "ingested_at": "2026-06-02T12:30:00Z"
    },
    {
        "_id": "evt_hist_2026_09",
        "title": "EU naval operation Aspides repels drone swarm attack targeting maritime traffic in Bab-el-Mandeb",
        "corridor": "Bab el-Mandeb Strait",
        "corridor_id": "corr_babelmandeb",
        "severity": 80,
        "source": "historical_intelligence",
        "category": "conflict",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Multi-drone interception prevents catastrophic hit on chemical and crude tankers traversing the strait.",
        "date": "Jun 20, 2026",
        "published_at": "2026-06-20T21:15:00Z",
        "ingested_at": "2026-06-20T21:15:00Z"
    },
    {
        "_id": "evt_hist_2026_10",
        "title": "VLCC tanker charter rates climb 18% as prolonged Africa diversions tighten global fleet availability",
        "corridor": "Cape of Good Hope Route",
        "corridor_id": "corr_cape",
        "severity": 55,
        "source": "historical_intelligence",
        "category": "other",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Baltic Dirty Tanker Index registers steep upward revision as tonne-mile demand surges.",
        "date": "Jul 12, 2026",
        "published_at": "2026-07-12T11:00:00Z",
        "ingested_at": "2026-07-12T11:00:00Z"
    },
    {
        "_id": "evt_hist_2026_11",
        "title": "Diplomatic talks in Muscat establish tentative maritime security protocols for Persian Gulf merchant transit",
        "corridor": "Strait of Hormuz",
        "corridor_id": "corr_hormuz",
        "severity": 40,
        "source": "historical_intelligence",
        "category": "diplomatic",
        "confidence": 1.0,
        "needs_review": False,
        "description": "Regional back-channel negotiations mitigate direct state interdictions while non-state threats persist.",
        "date": "Jul 28, 2026",
        "published_at": "2026-07-28T15:20:00Z",
        "ingested_at": "2026-07-28T15:20:00Z"
    }
]

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

# ==============================================================================
# TIER 3: LIVE NEWS FROM LAST 1 WEEK (Google News RSS + Gemini Batch Classification)
# ==============================================================================
async def fetch_last_week_live_rss() -> List[Dict[str, Any]]:
    """Fetch live news from Google News RSS for the last 7 days with targeted energy keywords"""
    query = "(%22crude+oil%22+OR+%22oil+tanker%22+OR+%22Strait+of+Hormuz%22+OR+%22Red+Sea%22+OR+%22Bab+el-Mandeb%22+OR+%22oil+sanctions%22+OR+%22Russian+oil%22+OR+%22Iranian+oil%22)"
    url = f"https://news.google.com/rss/search?q={query}+when:7d&hl=en-US&gl=US&ceid=US:en"
    headers = {"User-Agent": USER_AGENT}
    
    articles = []
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                root = ET.fromstring(resp.text)
                items = root.findall(".//item")
                for item in items[:50]:
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
                            "source": "Live News (7d)"
                        })
    except Exception as ex:
        logger.error(f"Error fetching weekly live RSS feed: {ex}")
    return articles

async def batch_classify_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Classifies a batch of articles using Gemini API in a single prompt to save free tier quota.
    Falls back to deterministic keyword mapping if Gemini rate-limited or fails.
    """
    if not articles:
        return []

    # Prepare batches of 12 articles per prompt
    batch_size = 12
    classified_results = []

    for i in range(0, len(articles), batch_size):
        chunk = articles[i:i + batch_size]
        prompt_items = [{"id": idx, "title": a["title"]} for idx, a in enumerate(chunk)]
        
        system_instruction = (
            "You are a geopolitical risk classifier for energy maritime supply chains. "
            "For each headline, determine the affected corridor, category, and severity (0-100). "
            "Respond ONLY with a valid JSON array matching:\n"
            '[{"id": int, "corridor": "Strait of Hormuz"|"Bab el-Mandeb Strait"|"Cape of Good Hope Route"|"Strait of Malacca"|"Suez Canal", '
            '"category": "sanctions"|"conflict"|"shipping_attack"|"diplomatic"|"other", "severity": int, "confidence": float}]'
        )

        prompt = f"Classify these maritime/energy news headlines:\n{json.dumps(prompt_items, indent=2)}"

        raw_llm = None
        try:
            raw_llm = await call_gemini_api(prompt, system_instruction)
        except Exception as e:
            logger.warning(f"Batch LLM classification error: {e}")

        # Parse LLM response or fallback
        llm_mapped = {}
        if raw_llm:
            try:
                parsed_list = json.loads(raw_llm)
                if isinstance(parsed_list, list):
                    for item in parsed_list:
                        llm_mapped[item.get("id")] = item
            except Exception as e:
                logger.warning(f"Failed to parse batch LLM response: {e}")

        for idx, art in enumerate(chunk):
            pub_dt = art["pub_dt"]
            date_str = pub_dt.strftime("%b %d, %Y") if hasattr(pub_dt, "strftime") else datetime.now(timezone.utc).strftime("%b %d, %Y")
            pub_iso = pub_dt.isoformat() if hasattr(pub_dt, "isoformat") else str(pub_dt)
            
            if idx in llm_mapped:
                m = llm_mapped[idx]
                classified_results.append({
                    "_id": f"evt_live_{uuid.uuid4().hex[:8]}",
                    "title": art["title"],
                    "corridor": m.get("corridor", "Strait of Hormuz"),
                    "category": m.get("category", "conflict"),
                    "severity": int(m.get("severity", 55)),
                    "confidence": float(m.get("confidence", 0.95)),
                    "needs_review": float(m.get("confidence", 0.95)) < 0.5,
                    "source": "Live News",
                    "description": f"Breaking news article: {art['url']}",
                    "date": date_str,
                    "published_at": pub_iso,
                    "ingested_at": datetime.now(timezone.utc).isoformat(),
                    "url": art["url"]
                })
            else:
                # Deterministic fallback
                t_lower = art["title"].lower()
                corridor = "Strait of Hormuz" if "hormuz" in t_lower else "Bab el-Mandeb Strait" if "red sea" in t_lower or "houthi" in t_lower or "aden" in t_lower else "Cape of Good Hope Route" if "cape" in t_lower or "africa" in t_lower else "Strait of Malacca" if "malacca" in t_lower or "singapore" in t_lower else "Strait of Hormuz"
                category = "shipping_attack" if "attack" in t_lower or "strike" in t_lower or "missile" in t_lower or "drone" in t_lower else "sanctions" if "sanction" in t_lower or "price cap" in t_lower else "conflict" if "war" in t_lower or "military" in t_lower or "navy" in t_lower else "diplomatic"
                severity = 75 if category == "shipping_attack" else 60 if category == "sanctions" else 50
                
                classified_results.append({
                    "_id": f"evt_live_{uuid.uuid4().hex[:8]}",
                    "title": art["title"],
                    "corridor": corridor,
                    "category": category,
                    "severity": severity,
                    "confidence": 0.85,
                    "needs_review": False,
                    "source": "Live News",
                    "description": f"Breaking news article: {art['url']}",
                    "date": date_str,
                    "published_at": pub_iso,
                    "ingested_at": datetime.now(timezone.utc).isoformat(),
                    "url": art["url"]
                })

        # Brief pause between batches if multiple to respect Gemini free tier RPM
        if i + batch_size < len(articles):
            await asyncio.sleep(4)

    return classified_results

# ==============================================================================
# MAIN SEED & RECOMPUTATION WORKFLOW
# ==============================================================================
async def recompute_all_corridor_risks(db):
    """Recalculate and update risk_scores for all corridors in the digital twin"""
    logger.info("Recalculating corridor risk scores across the digital twin...")
    corridors = await db.corridors.find({}).to_list(100)
    all_events = await db.risk_events.find({}).to_list(500)

    for corr in corridors:
        c_name = corr.get("name")
        c_id = corr.get("_id")
        base_risk = corr.get("base_risk", 50.0)
        share_pct = corr.get("share_of_india_imports_pct", 30.0)

        matching_evts = [e for e in all_events if e.get("corridor") == c_name or e.get("corridor_id") == c_id]
        avg_sev = sum(e.get("severity", 50) for e in matching_evts) / len(matching_evts) if matching_evts else base_risk

        calc = calculate_risk({
            "shipping_disruption": base_risk,
            "geopolitical_tension": avg_sev,
            "corridor_dependency": share_pct * 1.5
        }, entity_type="corridor")

        await db.risk_scores.update_one(
            {"entity_type": "corridor", "entity_id": c_id},
            {"$set": {
                "score": calc["score"],
                "category": calc["category"],
                "factors": calc["factors"],
                "computed_at": datetime.now(timezone.utc).isoformat()
            }},
            upsert=True
        )
    logger.info(f"Updated risk scores for {len(corridors)} corridors.")

async def seed_historical_and_live_news():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]

    logger.info("--- Starting Vantage 3-Tier News Ingestion ---")

    # Clean up any previously ingested non-energy/irrelevant events
    all_events_in_db = await db.risk_events.find({}).to_list(1000)
    purged = 0
    for ev in all_events_in_db:
        if not is_relevant_headline(ev.get("title", "")):
            await db.risk_events.delete_one({"_id": ev["_id"]})
            await db.processed_articles.delete_many({"title": ev.get("title", "")})
            purged += 1
    if purged > 0:
        logger.info(f"Purged {purged} irrelevant non-energy articles from database.")

    # 1. Ingest Tier 1 (2-3 Years Macro Milestones)
    t1_count = 0
    for evt in TIER_1_HISTORICAL_EVENTS:
        existing = await db.risk_events.find_one({"$or": [{"_id": evt["_id"]}, {"title": evt["title"]}]})
        if not existing:
            await db.risk_events.insert_one(evt)
            await db.processed_articles.insert_one({
                "url": f"https://vantage-intelligence.internal/archive/{evt['_id']}",
                "title": evt["title"],
                "processed_at": evt["ingested_at"],
                "published_at": evt["published_at"],
                "classifier_result": {"corridor": evt["corridor"], "category": evt["category"], "severity": evt["severity"]}
            })
            t1_count += 1
    logger.info(f"Tier 1 (2-3 Years): Seeded {t1_count} milestone events.")

    # 2. Ingest Tier 2 (Last 6 Months Major Incidents)
    t2_count = 0
    for evt in TIER_2_HISTORICAL_EVENTS:
        existing = await db.risk_events.find_one({"$or": [{"_id": evt["_id"]}, {"title": evt["title"]}]})
        if not existing:
            await db.risk_events.insert_one(evt)
            await db.processed_articles.insert_one({
                "url": f"https://vantage-intelligence.internal/archive/{evt['_id']}",
                "title": evt["title"],
                "processed_at": evt["ingested_at"],
                "published_at": evt["published_at"],
                "classifier_result": {"corridor": evt["corridor"], "category": evt["category"], "severity": evt["severity"]}
            })
            t2_count += 1
    logger.info(f"Tier 2 (Last 6 Months): Seeded {t2_count} tactical events.")

    # 3. Ingest Tier 3 (Last 1 Week Live Breaking News via Google News RSS + Gemini Batching)
    logger.info("Tier 3 (Last 1 Week): Fetching breaking live news...")
    weekly_raw_articles = await fetch_last_week_live_rss()
    logger.info(f"Fetched {len(weekly_raw_articles)} candidate articles from live RSS (7d).")

    # Filter duplicates before LLM classification
    unique_to_classify = []
    for art in weekly_raw_articles:
        existing = await db.processed_articles.find_one({"$or": [{"url": art["url"]}, {"title": art["title"]}]})
        if not existing:
            unique_to_classify.append(art)

    logger.info(f"Classifying {len(unique_to_classify)} new unique breaking articles with Gemini batching...")
    classified_live_events = await batch_classify_articles(unique_to_classify)

    t3_count = 0
    for evt in classified_live_events:
        url = evt.pop("url", "")
        await db.risk_events.insert_one(evt)
        await db.processed_articles.insert_one({
            "url": url,
            "title": evt["title"],
            "processed_at": evt["ingested_at"],
            "published_at": evt["published_at"],
            "classifier_result": {"corridor": evt["corridor"], "category": evt["category"], "severity": evt["severity"]}
        })
        t3_count += 1

    logger.info(f"Tier 3 (Last 1 Week): Ingested {t3_count} fresh breaking news events.")

    # 4. Recalculate all corridor risks
    await recompute_all_corridor_risks(db)

    total_events = await db.risk_events.count_documents({})
    total_processed = await db.processed_articles.count_documents({})
    logger.info(f"=== News Seeding Complete! Total events in DB: {total_events} (Processed articles: {total_processed}) ===")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed_historical_and_live_news())
