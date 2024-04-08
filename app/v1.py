import json
from pathlib import Path
from fastapi import APIRouter, Query
from app.scraper import scrape

v1 = APIRouter()

json_file_path = Path(__file__).parent.parent / 'scraped_data.json'
cached_data = None


async def load_data():
    global cached_data
    try:
        with open(json_file_path, 'r') as f:
            cached_data = json.load(f)
    except FileNotFoundError:
        cached_data = []


@v1.get("/news")
async def get_news(page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)):
    global cached_data
    if cached_data is None:
        await load_data()

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    paginated_news = cached_data[start_index:end_index]
    return paginated_news


@v1.get("/search")
async def search_news(search_query: str = Query(), page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)):
    global cached_data
    if cached_data is None:
        await load_data()

    results = [news for news in cached_data if search_query in news.get('title', '')]
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_news = results[start_index:end_index]
    return paginated_news


@v1.get("/scrape")
async def scrape_news():
    await scrape()
    await load_data()
    return {"msg": "Scraping complete!", 'status': 200}
