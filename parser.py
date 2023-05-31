from bs4 import BeautifulSoup
import aiohttp
import config
import random
import re

class HTTPget:
    url = ""
    headers = dict()
    def __init__(self, url: str, headers: dict = dict()):
        self.url = url
        self.headers = headers
    
    async def get_html(self, query: str) -> str:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=self.url + query, headers=self.headers)
            if not response.ok:
                return ''
            else:
                return await response.text(encoding='UTF-8')

yandex_get = HTTPget(config.yandex_url, config.headers)
lexica_get = HTTPget(config.lexica_url, config.headers)
tenor_get = HTTPget(config.tenor_url, config.headers)
cover_get = HTTPget(config.cover_url, config.headers)

async def get_imgs_yandex(query: str) -> list[str]:
    html = await yandex_get.get_html(query)
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    imgs_htmls = soup.find_all(class_="serp-item__thumb justifier__thumb")
    img_array = []
    for img in imgs_htmls:
        img_array.append("https:" + img.get("src"))
    random.shuffle(img_array)
    return img_array[:5]

async def get_imgs_lexica(query: str) -> list[str]:
    html = await lexica_get.get_html(query)
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    img_array = soup.find(property="og:image").get('content').split('&images=')[1:]
    random.shuffle(img_array)
    return img_array[:5]

async def get_imgs_tenor(query: str) -> list[str]:
    html = await tenor_get.get_html(query)
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    # print(html)
    imgs_htmls = soup.find_all(class_="Gif")
    img_array = []
    for img in imgs_htmls:
        if img.find_next().get("src") != None:
            img_array.append(img.find_next().get("src"))
    random.shuffle(img_array)
    return img_array[:1]

async def get_videos_cover(query: str) -> list[str]:
    html = await cover_get.get_html(query)
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    vids_htmls = soup.find_all(class_="acu-video-player__video")
    vid_array = []
    for vid in vids_htmls:
        if vid.get("src") != None:
            vid_array.append(vid.get("src"))
    random.shuffle(vid_array)
    return vid_array[:1]