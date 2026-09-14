import asyncio
from urllib.parse import unquote

import aiohttp
from flask import current_app

from yacut.constants import DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL


def get_headers():
    return {
        'Authorization': f'OAuth {current_app.config["DISK_TOKEN"]}'
    }


async def get_upload_link(session, path):
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=get_headers(),
        params={
            'path': path,
            'overwrite': 'True',
        },
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']


async def upload_to_disk(session, upload_link, file_data):
    async with session.put(
        upload_link,
        data=file_data,
    ) as response:
        response.raise_for_status()

        location = unquote(response.headers['Location'])

        if location.startswith('/disk'):
            location = location[len('/disk'):]

        return location


async def get_download_link(session, path):
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=get_headers(),
        params={'path': path},
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']


async def upload_file(session, filename, file_data):
    path = f'app:/{filename}'

    upload_link = await get_upload_link(session, path)

    location = await upload_to_disk(
        session,
        upload_link,
        file_data,
    )

    download_link = await get_download_link(
        session,
        location,
    )

    return filename, download_link


async def upload_files(files):
    async with aiohttp.ClientSession() as session:
        tasks = [
            upload_file(
                session,
                filename,
                file_data,
            )
            for filename, file_data in files
        ]

        return await asyncio.gather(*tasks)
