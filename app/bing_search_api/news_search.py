import requests
from app.utilities.config import settings
import logging

from typing import Any

class Bing:
    def fetch_news(self) -> dict[str, Any]:
        try:
            r = requests.get(
                f"{settings.bing_url}/news/search",
                headers={"Ocp-Apim-Subscription-Key": settings.bing_token},
                params={
                    "q": "",
                    "mkt": "en-IN",
                    "originalImg": True,
                    "freshness": "Day",
                    "safeSearch": "Strict",
                    "setLang": "en",
                    "cc": "IN",
                    "textDecorations": False,
                    "textFormat": "raw",
                    "sortBy": "Date"
                })
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTPError: {err}")
        except Exception as err:
            logging.error(f"Exception: {err}")
        else:
            data = r.json()
            value = data.get("value")
            if value:
                return value[0]
            return None
