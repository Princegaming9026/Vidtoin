import time
import random
import string
import os
import asyncio
import internetarchive

def parse_caption(caption):
    lines = caption.split("\n")
    data = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip().lower()] = value.strip()
    return data

def generate_identifier(title):
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    timestamp = int(time.time())
    return f"{title.replace(' ','_')}_{timestamp}_{random_id}"

async def upload_to_archive(identifier, file_path, title, category, description):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: internetarchive.upload(
        identifier,
        files=[file_path],
        metadata={
            "title": title,
            "mediatype": "movies",
            "collection": category,
            "description": description
        }
    ))

def cleanup_file(path):
    if os.path.exists(path):
        os.remove(path)
