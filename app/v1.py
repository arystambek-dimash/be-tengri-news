import json
import os
from fastapi import APIRouter, Query

from app.scraper import scrape

v1 = APIRouter()

json_file_path = os.path.join(os.path.dirname(__file__), '../scraped_data.json')


@v1.get("/news")
async def get_news(page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)):
    try:
        with open(json_file_path, 'r') as f:
            all_news = json.load(f)
    except FileNotFoundError:
        return []

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    paginated_news = all_news[start_index:end_index]

    return paginated_news


@v1.get("/scrape")
async def scrape_news():
    await scrape()
    return {"msg": "Scraping complete!", 'status': 200}
