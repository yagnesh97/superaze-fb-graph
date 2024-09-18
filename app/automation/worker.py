from datetime import datetime, timezone
from typing import Any

from app.automation.bing_news import NewsFetcher
from app.automation.facebook import SocialMediaPoster
from app.automation.genai import AIResponseGenerator
from app.utilities.config import settings
from app.utilities.db import db


class NewsAutomation:
    def __init__(self) -> None:
        self.now = datetime.now(timezone.utc)
        self.news = None
        self.news_id = None
        self.title = ""
        self.description = ""
        self.url = ""
        self.provider_name = ""
        self.hashtags = ""
        self.ai_response: Any = {}
        self.updates: dict[str, Any] = {}

    def refine_hashtags(
        self, hashtags: list[str | None]
    ) -> tuple[list[str], list[str]]:
        """Refines hashtags by stripping and sorting."""
        tags_wo_hash = [
            tag.replace("#", "").strip() for tag in hashtags if tag and tag.strip()
        ]
        tags_w_hash = ["#" + tag for tag in tags_wo_hash]
        return sorted(tags_w_hash), sorted(tags_wo_hash)

    def fetch_news(self) -> bool:
        """Fetch news and insert the first new one into the database."""
        news_fetcher = NewsFetcher()
        news = news_fetcher.get_news()

        for news_item in news:
            result = db.facebook_news.update_one(
                {"url": news_item["url"]},
                {
                    "$set": {"updated_date": self.now},
                    "$setOnInsert": {
                        "title": news_item["name"],
                        "description": news_item["description"],
                        "url": news_item["url"],
                        "source": news_item["provider"][0]["name"],
                        "created_date": self.now,
                        "published": False,
                    },
                },
                upsert=True,
            )

            if result.upserted_id:
                self.news = news_item
                self.news_id = result.upserted_id
                return True  # New news inserted and found
        return False  # No new news found

    def apply_ai_response(self) -> None:
        """Fetch and apply AI-generated content."""
        if not self.news:
            return

        self.title = self.news["name"]
        self.description = self.news["description"]
        self.url = self.news["url"]
        self.provider_name = self.news["provider"][0]["name"]

        ai_generator = AIResponseGenerator()
        self.ai_response = ai_generator.get_ai_response(
            title=self.title, description=self.description
        )
        if self.ai_response:
            self.title = self.ai_response.get("title", self.title).strip()
            self.description = self.ai_response.get(
                "description", self.description
            ).strip()

            hashtags = self.ai_response.get("hashtags", [])
            if isinstance(hashtags, list) and hashtags:
                tags_w_hash, tags_wo_hash = self.refine_hashtags(hashtags)
                self.hashtags = " ".join(tags_w_hash)

            # Accumulate updates to be made to the database
            self.updates.update(
                {
                    "ai_title": self.title,
                    "ai_description": self.description,
                    "ai_hashtags": tags_wo_hash,
                }
            )

    def create_social_media_post(self) -> Any | None:
        """Create a social media post and prepare final database update."""
        message = (
            f"{self.title}\n\n{self.description}\n\n"
            f"Credits: {self.provider_name}\n\n{self.hashtags}"
        ).strip()

        poster = SocialMediaPoster()
        post_data = poster.create_post(
            page_id=settings.page_id,
            message=message,
            link=self.url,
        )

        if post_data and post_data.get("id"):
            # Prepare final update for the post status
            self.updates["published"] = True
            return post_data["id"]
        return None

    def run(self) -> Any:
        """Run the entire automation process."""
        if self.fetch_news():
            self.apply_ai_response()
            post_id = self.create_social_media_post()

            if self.updates:
                # Perform single database update with all accumulated changes
                db.facebook_news.update_one(
                    {"_id": self.news_id},
                    {"$set": self.updates},
                )
            return post_id

        return None
