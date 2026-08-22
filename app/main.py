from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection, get_db
from app.api import dashboard, suppliers, network, risk, scenarios, routes, reserves, recommendations, explain, events, prices, admin
from app.services.news_poller import GdeltNewsPoller
from app.services.oil_price_poller import OilPricePoller
from app.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB Atlas
    await connect_to_mongo()
    db_client = get_db()
    settings = get_settings()
    
    # Initialize and start GDELT News Poller
    if settings.ENABLE_GDELT_POLLING:
        poller = GdeltNewsPoller(db=db_client, poll_interval_minutes=settings.GDELT_POLL_INTERVAL_MINUTES)
        app.state.news_poller = poller
        await poller.start()
    else:
        app.state.news_poller = None

    # Initialize and start Daily Brent Oil Price Poller
    if settings.ENABLE_OIL_PRICE_POLLING:
        oil_poller = OilPricePoller(db=db_client, poll_interval_hours=settings.OIL_PRICE_POLL_INTERVAL_HOURS)
        app.state.oil_price_poller = oil_poller
        await oil_poller.start()
    else:
        app.state.oil_price_poller = None

    yield
    
    # Shutdown
    if hasattr(app.state, "oil_price_poller") and app.state.oil_price_poller:
        await app.state.oil_price_poller.stop()

    if hasattr(app.state, "news_poller") and app.state.news_poller:
        await app.state.news_poller.stop()
        
    # Shutdown: Close database pool
    await close_mongo_connection()

app = FastAPI(
    title="VANTAGE - Energy Supply Chain Resilience API",
    description="AI-Driven Energy Supply Chain Risk & Procurement Rerouting Engine for Import-Dependent Economies",
    version="1.0.0",
    lifespan=lifespan
)

# Configure robust CORS middleware for React/Vite Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(dashboard.router)
app.include_router(prices.router)
app.include_router(suppliers.router)
app.include_router(network.router)
app.include_router(risk.router)
app.include_router(scenarios.router)
app.include_router(routes.router)
app.include_router(reserves.router)
app.include_router(recommendations.router)
app.include_router(explain.router)
app.include_router(events.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "VANTAGE Energy Supply Chain Resilience API",
        "docs": "/docs",
        "health": "healthy"
    }
