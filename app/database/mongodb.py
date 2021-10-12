from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger

from app.core.config import settings

logger.debug("Connecting to mongodb...")
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_url)
db: AsyncIOMotorDatabase = client[settings.mongodb_db_name]
logger.debug("Connected!")

# async def mongodb_connect():
#     global _client
#     global _db
#     logger.debug("Connecting to mongodb...")
#     client = AsyncIOMotorClient(settings.mongodb_url)
#     db = client[settings.mongodb_db_name]
#     logger.debug(db)
#     logger.debug("Connected!")


async def mongodb_disconnect():
    global client
    client.close()
