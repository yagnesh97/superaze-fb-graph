import logging
from typing import Any

import azure.functions as func

from app.bing_search_api.news_search import Bing
from app.graph_api.graph import Graph
from app.utilities.config import settings
from app.utilities.db import db

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


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


@app.route(route="FacebookPost", methods=[func.HttpMethod.POST])
def FacebookPost(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    func_token = req.headers.get("access-token")
    assert func_token == settings.token, "Invalid access token."

    fb = Facebook()
    post_id = fb.publish_post()

    return func.HttpResponse(
        f"Post published succeesfully! Post ID: {post_id}", status_code=200
    )
