from types import NoneType
import aiohttp
from bs4 import BeautifulSoup


class ContextEnglishApi:
    cookies = {
        'preferredDictionaries': 'english-russian,english,british-grammar,english-polish',
        '_sp_id.7ecc': '6165b69d-3fe3-4ad6-8df4-454218221d63.1743952787.2.1744034321.1743952987.92a9edb3-48e7-40b9-a980-3299fdf7997d.04a1c77b-48c5-479a-9cc1-ed8d00388f7c.cbed7a2e-4f17-4152-b2c9-3e016f50f350.1744033895016.24',
        'amp-access': 'amp-9KVdyLTBGHcwg2udSyDM0g',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Apr+07+2025+18^%^3A58^%^3A42+GMT^%^2B0500+(^%^D0^%^95^%^D0^%^BA^%^D0^%^B0^%^D1^%^82^%^D0^%^B5^%^D1^%^80^%^D0^%^B8^%^D0^%^BD^%^D0^%^B1^%^D1^%^83^%^D1^%^80^%^D0^%^B3^%^2C+^%^D1^%^81^%^D1^%^82^%^D0^%^B0^%^D0^%^BD^%^D0^%^B4^%^D0^%^B0^%^D1^%^80^%^D1^%^82^%^D0^%^BD^%^D0^%^BE^%^D0^%^B5+^%^D0^%^B2^%^D1^%^80^%^D0^%^B5^%^D0^%^BC^%^D1^%^8F)&version=202407.2.0&browserGpcFlag=1&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1&AwaitingReconsent=false&geolocation=RU^%^3BSVE',
        'loginPopup': '7',
        'OptanonAlertBoxClosed': '2025-04-07T13:58:42.026Z',
        '_sp_ses.7ecc': '*',
        'XSRF-TOKEN': '84719bf9-50be-4f90-9404-b26943a1732c',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        # 'Cookie': 'preferredDictionaries=english-russian,english,british-grammar,english-polish; _sp_id.7ecc=6165b69d-3fe3-4ad6-8df4-454218221d63.1743952787.2.1744034321.1743952987.92a9edb3-48e7-40b9-a980-3299fdf7997d.04a1c77b-48c5-479a-9cc1-ed8d00388f7c.cbed7a2e-4f17-4152-b2c9-3e016f50f350.1744033895016.24; amp-access=amp-9KVdyLTBGHcwg2udSyDM0g; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Apr+07+2025+18^%^3A58^%^3A42+GMT^%^2B0500+(^%^D0^%^95^%^D0^%^BA^%^D0^%^B0^%^D1^%^82^%^D0^%^B5^%^D1^%^80^%^D0^%^B8^%^D0^%^BD^%^D0^%^B1^%^D1^%^83^%^D1^%^80^%^D0^%^B3^%^2C+^%^D1^%^81^%^D1^%^82^%^D0^%^B0^%^D0^%^BD^%^D0^%^B4^%^D0^%^B0^%^D1^%^80^%^D1^%^82^%^D0^%^BD^%^D0^%^BE^%^D0^%^B5+^%^D0^%^B2^%^D1^%^80^%^D0^%^B5^%^D0^%^BC^%^D1^%^8F)&version=202407.2.0&browserGpcFlag=1&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001^%^3A1^%^2CC0002^%^3A1^%^2CC0003^%^3A1^%^2CC0004^%^3A1&AwaitingReconsent=false&geolocation=RU^%^3BSVE; loginPopup=7; OptanonAlertBoxClosed=2025-04-07T13:58:42.026Z; _sp_ses.7ecc=*; XSRF-TOKEN=84719bf9-50be-4f90-9404-b26943a1732c',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
    }

    url = 'https://dictionary.cambridge.org/dictionary/english-russian/'

    async def parse(self,word: str):
        url_word = word.replace(" ", "+")
        async with aiohttp.ClientSession(headers=ContextEnglishApi.headers,
                                         cookies=ContextEnglishApi.cookies) as session:
            async with session.get(ContextEnglishApi.url + url_word) as response:
                return await response.text()


    async def getting_context(self, word :str ):
        page = await self.parse(word)

        soup = BeautifulSoup(page, 'html.parser')

        sentences_soup = soup.find_all("span", "deg")
        #print(sentences_soup)

        sentences = [sentence.text.strip() for sentence in sentences_soup if sentence.text != NoneType]
        return sentences