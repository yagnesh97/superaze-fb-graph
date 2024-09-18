import logging
from typing import Any

import requests

from app.utilities.config import settings


class SocialMediaPoster:
    def __init__(self) -> None:
        self.base_url = settings.graph_url
        self.access_token = settings.graph_token
        logging.basicConfig(level=logging.INFO)

    def create_post(self, page_id: int, message: str, link: str) -> Any:
        """Create a social media post on the specified page."""
        try:
            response = requests.post(
                f"{self.base_url}/{page_id}/feed",
                params={
                    "access_token": self.access_token,
                    "message": message,
                    "link": link,
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request exception occurred: {req_err}")
        except Exception as err:
            logging.error(f"An unexpected error occurred: {err}")
