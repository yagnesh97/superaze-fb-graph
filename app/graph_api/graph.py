import logging
from typing import Any

import requests

from app.utilities.config import settings


class Graph:
    def fetch_page_id(self) -> Any:
        try:
            r = requests.get(
                f"{settings.graph_url}/me",
                params={"access_token": settings.graph_token},
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTPError: {err}")
        except Exception as err:
            logging.error(f"Exception: {err}")
        else:
            data = r.json()
            if data["name"] == settings.page_name:
                return data["id"]

    def create_post(self, page_id: str, message: str, link: str) -> Any:
        try:
            r = requests.post(
                f"{settings.graph_url}/{page_id}/feed",
                params={
                    "access_token": settings.graph_token,
                    "message": message,
                    "link": link,
                },
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTPError: {err}")
        except Exception as err:
            logging.error(f"Exception: {err}")
        else:
            data = r.json()
            return data
