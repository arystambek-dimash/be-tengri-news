import aiofiles
import json


async def write_to_json(data):
    try:
        with open('scraped_data.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(e)