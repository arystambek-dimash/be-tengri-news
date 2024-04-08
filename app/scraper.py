import asyncio

import aiohttp
import requests
from bs4 import BeautifulSoup

from .utils import write_to_json

_url = 'https://tengrinews.kz/news/page/{index}/'
content_box_div_name = 'content_main_item'

_scraped_data = []


async def scrape_page(session, index):
    async with session.get(_url.format(index=index)) as response:
        html = await response.text()
        bs = BeautifulSoup(html, 'html.parser')
        articles = bs.find_all('div', class_=content_box_div_name)

        scraped_data = []
        for article in articles:
            details_url = article.find('a')['href']
            title = article.find('span', class_='content_main_item_title').get_text(strip=True).replace("\n",
                                                                                                        " ").strip()
            announce_tag = article.find('span', class_='content_main_item_announce')
            announce = announce_tag.get_text(strip=True) if announce_tag else None
            img = article.find('img', class_='content_main_item_img')['src']
            sub_box = article.find('div', class_='content_main_item_meta')
            publish_date = sub_box.find('span').get_text(strip=True) if sub_box else None

            article_dict = {
                'details_url': 'https://tengrinews.kz/' + details_url,
                'title': title,
                'announce': announce,
                'img': 'https://tengrinews.kz/' + img,
                'publish_date': publish_date
            }
            print(publish_date)
            scraped_data.append(article_dict)

        return scraped_data


async def scrape():
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_page(session, index) for index in range(100)]
        results = await asyncio.gather(*tasks)
        scraped_data = [article for result in results for article in result]

    await write_to_json(scraped_data)
    return scraped_data
