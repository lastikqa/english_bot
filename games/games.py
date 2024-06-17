import time

from english_bot_database.english_bot_database import EnglishBotDatabase
import requests
from bs4 import BeautifulSoup
import random
from gtts import gTTS
import translators as ts
from api.guessing_api import GuessingGameApi
from config import datebase_name
from api.context_english_api import ContextEnglishApi
from api.random_chuck_jokes_api import RandomChuckJokesApi

database_name = datebase_name


class Games:
    def __init__(self, user_id, user_param):
        self.user_id = user_id
        self.user_param = user_param

    def gusesing_game(self, user_id, user_param):
        database = EnglishBotDatabase(user_id)
        database.updating_user_game(user_id=user_id, game=user_param)
        translation = database.checking_user_translation(user_id=user_id)
        question, answer, variants = self.getting_data_guessing_game(translation=translation, user_param=user_param)
        database.updating_answer(answer=answer, user_id=user_id)
        database.updating_variants_for_user(user_id=user_id, variants=variants)
        database.updating_question(user_id=user_id, question=question)
        return question, variants

    @staticmethod
    def getting_data_guessing_game(user_param: str, headers=GuessingGameApi.headers,
                                   params: str = GuessingGameApi.params,
                                    translation: str = "rus") -> tuple:
        """getting the guessind word game data"""
        params["slovar"] = user_param
        params["first"] = translation
        params["rand"] = random.random()
        response = requests.get('https://hosgeldi.com/eng/guess_new.php', params=params,
                                cookies=GuessingGameApi.cookies, headers=headers).json()
        question = response["question"]
        answer = response["answer"]
        variants = list(response["variants"])
        return question, answer, variants

    def getting_constcuctor_games(self, translation: str = "rus", user_param: str = "v",
                                  params: str = GuessingGameApi.params,
                                  headers=GuessingGameApi.headers):

        params["slovar"] = user_param
        params["first"] = translation
        params["rand"] = random.random()
        try:
            response = requests.get(GuessingGameApi.url, params=params, cookies=GuessingGameApi.cookies,
                                    headers=headers).json()
        except requests.JSONDecodeError:
            time.sleep(5)

            response = requests.get(GuessingGameApi.url, params=params, cookies=GuessingGameApi.cookies,
                                    headers=headers).json()
        question = response["answer"]
        answer = response["question"]
        variants = self.random_constructor_variants(answer=answer)
        return question, answer, variants

    @staticmethod
    def random_constructor_variants(answer: str) -> list:
        """the function gets strings and splits them into lists
        and return the lists with random words of letters of the string"""

        if " " in answer:
            answer = answer.split()
        else:
            answer = list(answer)
        variants = []
        while len(variants) != len(answer):
            item = answer[random.randrange(0, len(answer))]
            if item not in variants:
                variants.append(item)
        return variants

    def constructor_games(self, user_id, user_param):
        database = EnglishBotDatabase(user_id)
        database.updating_user_game(user_id, game=user_param)
        question, answer, variants = self.getting_constcuctor_games(user_param=user_param)
        database.updating_answer(user_id, answer=answer)
        database.updating_variants_for_user(user_id, variants=variants)
        database.updating_user_variants(user_id, variants)
        database.updating_question(user_id=user_id, question=question)
        return variants, question

    def word_constructor(self, user_id: int) -> tuple | str:
        user_param = random.choice(["g", "c", "s", "p"])
        database = EnglishBotDatabase(user_id)
        database.updating_user_game(user_id, game="word_constructor")
        question, answer, variants = self.getting_data_guessing_game(user_param=user_param, translation="turk")
        variants = answer
        if " " in variants:
            variants = variants.replace(" ", "_")
            variants = random.sample(variants, len(variants))
        else:
            variants = random.sample(variants, len(variants))
        database.updating_answer(answer=answer, user_id=user_id)
        database.updating_variants_for_user(user_id=user_id, variants=variants)
        database.updating_user_variants(user_id, variants)
        database.updating_question(user_id=user_id, question=question)
        return question, variants

    @staticmethod
    def getting_jokes(user_id):
        database = EnglishBotDatabase(user_id)
        joke = requests.get(RandomChuckJokesApi.chuck_url).json()
        joke = joke["joke"]
        database.updating_answer(user_id=user_id, answer=joke)
        return joke

    @staticmethod
    def getting_translation(user_id: int) -> str:
        database = EnglishBotDatabase(user_id)
        answer = database.checking_answer(user_id)
        translation = ts.translate_text(answer, to_language='ru')
        return translation

    @staticmethod
    def getting_audio(user_id, text: str) -> str:
        audio = gTTS(text=text, lang="en", slow=False)
        audio.save(f"{user_id}.mp3")
        name_audio = f"{user_id}.mp3"
        return name_audio

    @staticmethod
    def getting_dictionaries_data(dictionary: dict, key_list: list) -> tuple:
        """I made a list with keys of my dictionaries  and get random item of my list as a key to the dicts """
        key = random.choice(key_list)
        random_dictionary_values = dictionary[key]

        return key, random_dictionary_values

    @staticmethod
    def getting_context(word: str) -> tuple:
        """english words should be seen in its contexts. the function gets a word and return a sentence with the word
        and translation of the sentence into russian"""
        find_word = list(word)
        find_word = find_word[0]
        word_url = word.replace(" ", "+")
        page = requests.get(url=ContextEnglishApi.context_english_url+word_url,
                          headers=ContextEnglishApi.context_english_headers,
                          cookies=ContextEnglishApi.context_english_cookies)
        soup = BeautifulSoup(page.text, "html.parser")
        sentences_soup = soup.findAll('span', class_="text")
        sentences = []
        for sentence in sentences_soup:
            sentence = sentence.text
            sentences.append(sentence.strip())
        sentences = sentences[31::]
        context = random.choice(sentences)
        while find_word not in context:
            context = random.choice(sentences)
        translation = ts.translate_text(context, to_language='ru')
        return context, translation
