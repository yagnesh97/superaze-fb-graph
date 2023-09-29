from typing import Any

from pymongo import MongoClient
from pymongo.database import Database

from app.utilities.config import settings


def get_db() -> Database[Any]:
    """Get MongoDB

    Returns:
        Database[Any]: Database connection object.
    """
    return MongoClient(settings.mongo_uri)[settings.mongo_db]


db = get_db()
