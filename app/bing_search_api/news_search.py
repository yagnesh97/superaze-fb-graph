import logging
from typing import Any, Union

import requests

from app.utilities.config import settings


class Bing:
    def fetch_news(self) -> Any:
        try:
            params: dict[str, Union[str, bool]] = {
                "mkt": "en-IN",
                "freshness": "Day",
                "safeSearch": "Strict",
                "sortBy": "Date",
            }
            r = requests.get(
                f"{settings.bing_url}/news",
                headers={"Ocp-Apim-Subscription-Key": settings.bing_token},
                params=params,
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTPError: {err}")
        except Exception as err:
            logging.error(f"Exception: {err}")
        else:
            data = r.json()
            value = data["value"]
            return value
