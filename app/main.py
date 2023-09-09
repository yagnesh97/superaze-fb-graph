from typing import Any
from bing_search_api.news_search import Bing
from graph_api.graph import Graph

class Superaze:
    def publish_post(self) -> dict[str, Any]:
        bing = Bing()
        news = bing.fetch_news()
        name = news["name"]
        description = news["description"]
        url = news["url"]
        provider_name = news["provider"][0]["name"]

        graph = Graph()
        page_id = graph.fetch_page_id()
        graph.create_post(page_id=page_id, message=f"{name}\n\n{description}\n\nCredits: {provider_name}", link=url)

if __name__ == "__main__":
    s = Superaze()
    s.publish_post()