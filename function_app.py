import logging
from typing import Any

import azure.functions as func

from app.bing_search_api.news_search import Bing
from app.graph_api.graph import Graph
from app.utilities.db import db

app = func.FunctionApp()


class Facebook:
    def publish_post(self) -> Any:
        bing = Bing()
        news_list = bing.fetch_news()

        for news in news_list:
            result = db.facebook_news.update_one(
                {"url": news["url"]},
                {"$setOnInsert": {"url": news["url"]}},
                upsert=True,
            )
            # Check if an upsert occurred (i.e., a new document was inserted)
            if result.upserted_id:
                break

        name = news["name"]
        description = news["description"]
        url = news["url"]
        provider_name = news["provider"][0]["name"]

        graph = Graph()
        page_id = graph.fetch_page_id()
        data = graph.create_post(
            page_id=page_id,
            message=f"{name}\n\n{description}\n\nCredits: {provider_name}",
            link=url,
        )
        return data["id"]


@app.schedule(
    schedule="0 0 * * * *", arg_name="timer", run_on_startup=True, use_monitor=False
)
def FacebookPost(timer: func.TimerRequest) -> None:
    if timer.past_due:
        logging.info("The timer is past due!")

    fb = Facebook()
    post_id = fb.publish_post()

    logging.info(f"Post published succeesfully! Post ID: {post_id}")
    logging.info("Python timer trigger function executed.")
