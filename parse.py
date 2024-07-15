from itertools import chain
from typing import Dict, Union
from urllib.parse import urlparse
import requests
from omegaconf import OmegaConf
from pyppeteer import launch
from bs4 import BeautifulSoup


config = OmegaConf.load("config.yaml")


class HTMLParser:
    def __init__(self, vendor: str) -> None:
        self.config = config[vendor].to_dict()
        self.browser = None
        self.page = None
        self.urls = dict()

    async def initialize_browser(self):
        self.browser = await launch(headless=True, args=["--no-sandbox"])

    async def close_browser(self) -> None:
        if self.browser:
            await self.browser.close()

    async def get_page(self, url: str):
        if self.browser:
            page = await self.browser.newPage()
            await page.goto(url)
            content = await page.content()
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content = response.content.decode("utf-8")
            else:
                response.raise_for_status()
        self.page = BeautifulSoup(content, "html.parser")

    async def get_all_urls(self, url: str = None, base_url: str = None):
        elements = list()
        url = url or str(self.config["base"]["url"])
        await self.get_page(url)
        elements.extend(
            chain.from_iterable(
                self.page.select(path) for path in self.config["base"]["path"]
            )
        )
        for element in elements:
            text = element.text.strip()
            link = element.get("href")
            if text and link:
                if not link.startswith("http"):
                    base_url = (
                        base_url
                        or urlparse(self.config["base"]["url"])
                        ._replace(path="")
                        .geturl()
                    )
                    link = base_url + link
                self.urls[text] = link

    async def get_page_content(self, config: Dict[str, Union[list, str, dict]]):
        if "path" in config:
            data = ""
            for path in config.get("path"):
                if path and config.get("terminator"):
                    element = self.page.select_one(path)
                    terminating_element = self.page.select_one(config.get("terminator"))
                    while element:
                        if element == terminating_element:
                            break
                        data += "\n\n" + element.text.strip()
                        element = element.find_next()

                elif path and not config.get("terminator"):
                    for element in self.page.select(path):
                        data += "\n\n" + element.text.strip()
            return data.strip()
        elif isinstance(config, dict):
            data = dict()
            for key, value in config.items():
                data[key] = await self.get_page_content(value)
            return data
        else:
            return ""

    async def get_content(self, url: str):
        self.data = dict()
        await self.get_page(url)
        for key, value in self.config.get("content").items():
            self.data[key] = await self.get_page_content(value)
