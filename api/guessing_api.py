
class GuessingGameApi:
    url = "https://hosgeldi.com/eng/guess_new.php"

    headers = {
        'Host': 'hosgeldi.com',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://hosgeldi.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=1, i',
    }

    """g-verbs s-nouns  c-nums  p-adjectives  
    m-pronouns prepositions conjunction"""
    # rus means eng-rus
    # turk means rus-eng
    params_game = {
        'slovar': 'g',
        'first': 'rus',
        'rand': '0.11160402868355046',
    }

    cookies = {
        'FCNEC': '%5B%5B%22AKsRol9Gn13G8Ikqu5qCkcPltDM_'
                 'fUtc6Sj1CzzPWDGj4fmoSMMxe7D0ifJgfAByCrDTPwXl4e1QbR4pyIksTaKiQRFFKKZsF5F0jYP2Z7E03IprqsR1Z_'
                 'prXYJGGyCoNTesf3sxcdahEYD5REqW2Cry9gJtXln0qw%3D%3D%22%5D%5D',
    }




