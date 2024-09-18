import logging
from typing import Any

import requests

from app.utilities.config import settings


class NewsFetcher:
    def __init__(self) -> None:
        self.base_url = settings.bing_url
        self.api_key = settings.bing_token
        self.params = {
            "mkt": "en-IN",
            "freshness": "Day",
            "safeSearch": "Strict",
            "sortBy": "Date",
        }
        self.headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        logging.basicConfig(level=logging.INFO)

    def get_news(self) -> Any:
        """Fetch news from the API."""
        try:
            response = requests.get(
                f"{self.base_url}/news", headers=self.headers, params=self.params
            )
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request exception occurred: {req_err}")
        except KeyError as key_err:
            logging.error(f"Key error: {key_err}")
        except Exception as err:
            logging.error(f"An unexpected error occurred: {err}")
