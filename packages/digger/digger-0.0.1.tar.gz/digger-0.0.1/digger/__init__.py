import asyncio
from collections import Counter, defaultdict

import aiohttp
import jieba
from bs4 import BeautifulSoup


class Digger:
    def __init__(self):
        self._tokenizer = jieba.Tokenizer()
        self._words = set()

    def specify_words(self, words):
        self._words.update(words)
        for w in words:
            self._tokenizer.add_word(w)

    def __call__(self, urls, merge_result=False):
        items = []
        errors = []

        async def request(url):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        html = await response.text()
            except aiohttp.ClientError as e:
                errors.append(dict(url=url, message=repr(e)))
            else:
                soup = BeautifulSoup(html, features="html.parser")
                text = soup.get_text()
                seg = jieba.cut(text)
                for w, n in Counter(seg).items():
                    if (not self._words) or (w in self._words):
                        items.append(dict(url=url, word=w, count=n))

        async def main():
            await asyncio.gather(*[request(url) for url in urls])

        asyncio.run(main())

        if merge_result:
            counter = defaultdict(int)
            for item in items:
                counter[item['word']] += item['count']
            items = [dict(word=k, count=v) for k, v in counter.items()]

        return dict(items=items, errors=errors)
