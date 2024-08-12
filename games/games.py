from english_bot_database.english_bot_database import EnglishBotDatabase
from bs4 import BeautifulSoup
import random
import aiohttp
from config import database_name
from api.context_english_api import ContextEnglishApi
from api.random_chuck_jokes_api import RandomChuckJokesApi
from data.file_manager import FileManager
from useful_functuons.text_converter import converting_text_to_audio
from useful_functuons.translation import translation_text
database_name = database_name


class Games:
    def __init__(self, user_id, data):
        self.user_id = user_id
        self.game_data = FileManager(data)
        self.database = EnglishBotDatabase(user_id)

    async def getting_context(self, word: str) -> tuple[str, str]:
        """english words should be seen in its contexts. the function gets a word and return a sentence with the word
        and translation of the sentence into russian"""
        find_word = list(word)
        find_word = find_word[0]
        word_url = word.replace(" ", "+")

        async def rec(w: str):
            async with aiohttp.ClientSession(headers=ContextEnglishApi.context_english_headers,
                                             cookies=ContextEnglishApi.context_english_cookies) as session:
                async with session.get(ContextEnglishApi.context_english_url + w) as response:
                    return await response.text()

        page = await rec(word_url)

        soup = BeautifulSoup(page, "html.parser")
        sentences_soup = soup.findAll('span', class_="text")
        sentences = []
        for sentence in sentences_soup:
            sentence = sentence.text
            sentences.append(sentence.strip())
        sentences = sentences[31::]
        context = random.choice(sentences)
        while find_word not in context:
            context = random.choice(sentences)
        translation = self.getting_absolute_translation()
        translation = translation_text(context, to_language=translation)
        return context, translation

    async def guessing_game(self):
        self.database.checking_user_game()
        translation = self.database.checking_user_translation()
        user_language = self.database.checking_user_language()
        answer, variants, level = await self.getting_data_guessing_game()
        question = translation_text(answer, to_language=user_language)
        if translation != "en":
            variants = [translation_text(i, to_language=translation) for i in variants]
            question = translation_text(answer, to_language=translation)
            answer, question = question, answer
        self.database.updating_answer(answer=answer)
        self.database.updating_variants_for_user(variants=variants)
        self.database.updating_question(question=question)
        audio = self.giving_audio()

        return question, variants, level, audio

    async def getting_data_guessing_game(self, constructor=None):
        parts_of_speech = self.game_data.reading_json()

        if constructor == "phrase":
            parts_of_speech = self.game_data.getting_random_object_from_json()
            word = random.choice([i for i in parts_of_speech[1]])
            answer, question = await self.getting_context(word)
            return question, answer

        elif constructor == 'word':
            parts_of_speech = self.game_data.getting_random_object_from_json()
            word = random.choice([i for i in parts_of_speech[1]])
            return word

        else:
            user_game = self.database.checking_user_game()
            variants_of_words = []
            list_of_words = [i for i in parts_of_speech[user_game]]
            for _ in range(9):
                variants_of_words.append(random.choice(list_of_words))

            answer = random.choice(variants_of_words)

            level = parts_of_speech[user_game][answer]["level"]
        return answer, variants_of_words, level

    async def constructor_phrases(self, language):
        question, answer = await self.getting_data_guessing_game(constructor="phrase")
        if language == "en":
            question, answer = answer, question
        variants = answer.split()
        variants = random.sample(variants, len(variants))
        self.database.updating_answer(answer=answer)
        self.database.updating_variants_for_user(variants=variants)
        self.database.updating_user_variants(variants)
        self.database.updating_question(question=question)
        audio = self.giving_audio()
        return variants, question, audio

    async def word_constructor(self) -> tuple | str:
        """the function splits the word into a  lists with its letters into a random order
        that is used to make inline keyboards"""
        self.database.updating_user_game(game="word_constructor")
        answer = await self.getting_data_guessing_game(constructor="word")
        translation = self.getting_absolute_translation()
        question = translation_text(answer, to_language=translation)
        variants = answer
        if " " in variants:
            variants = variants.replace(" ", "_")
            variants = random.sample(variants, len(variants))
        else:
            variants = random.sample(variants, len(variants))

        self.database.updating_answer(answer=answer)
        self.database.updating_variants_for_user(variants=variants)
        self.database.updating_user_variants(variants)
        self.database.updating_question(question=question)
        audio = self.giving_audio()
        return question, variants, audio

    @staticmethod
    async def getting_jokes():
        async with aiohttp.ClientSession() as session:
            async with session.get(RandomChuckJokesApi.chuck_url) as response:
                return await response.json()

    def getting_absolute_translation(self):
        translation = (self.database.checking_user_translation(),
                       self.database.checking_user_language())
        for i in translation:
            if i != 'en':
                translation = i
        return translation

    def giving_audio(self):
        games = ['verbs', 'prepositions', 'numbers', 'nouns', 'pronouns', 'adjectives', 'conjunctions']
        user_game = self.database.checking_user_game()

        translation = self.database.checking_user_translation()
        if user_game in games:
            if translation == "en":
                word = self.database.checking_answer()
            else:
                word = self.database.checking_question()
        elif user_game == 'v' and translation == 'en':
            word = self.database.checking_question()
        else:
            word = self.database.checking_answer()
        audio_bytes = converting_text_to_audio(word)
        self.database.updating_user_media_data(media=audio_bytes)
        return audio_bytes
