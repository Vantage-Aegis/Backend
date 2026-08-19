from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import logging
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

db_instance = Database()

async def connect_to_mongo():
    settings = get_settings()
    logger.info(f"Connecting to MongoDB Atlas Cluster database: {settings.DATABASE_NAME}")
    db_instance.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db_instance.db = db_instance.client[settings.DATABASE_NAME]
    logger.info("Successfully connected to MongoDB Atlas.")

async def close_mongo_connection():
    if db_instance.client:
        logger.info("Closing MongoDB connection.")
        db_instance.client.close()
        logger.info("MongoDB connection closed.")

def get_db() -> AsyncIOMotorDatabase:
    if db_instance.db is None:
        raise RuntimeError("Database connection not initialized. Please call connect_to_mongo() first.")
    return db_instance.db
