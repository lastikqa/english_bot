from types import NoneType
import aiohttp
from bs4 import BeautifulSoup


class ContextEnglishApi:


    url = "https://www.merriam-webster.com/dictionary/"

    async def parse(self,word: str):
        url_word = word.replace(" ", "+")
        async with aiohttp.ClientSession() as session:
            async with session.get(ContextEnglishApi.url + url_word) as response:
                return await response.text()


    async def getting_context(self, word :str ):
        page = await self.parse(word)
        soup = BeautifulSoup(page, 'html.parser')

        sentences_soup = soup.find_all("span", "t has-aq")


        sentences = [sentence.text.strip() for sentence in sentences_soup]


        return sentences