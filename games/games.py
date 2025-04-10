from english_bot_database.english_bot_database import EnglishBotDatabase

import random
import aiohttp
from api.context_english_api import ContextEnglishApi
from api.random_chuck_jokes_api import RandomChuckJokesApi
from data.file_manager import FileManager
from useful_functuons.text_converter import converting_text_to_audio
from useful_functuons.translation import translation_text


class Games:
    def __init__(self, user_id, data):
        self.user_id = user_id
        self.game_data = FileManager(data)
        self.database = EnglishBotDatabase(user_id)

    async def getting_context(self, word: str) -> tuple[str, str]:
        """english words should be seen in its contexts. the function gets a word and return a sentence with the word
        and translation of the sentence into russian"""
        api = ContextEnglishApi()
        sentences = await api.getting_context(word)
        print(sentences)
        context = random.choice(sentences)
        translation = await self.getting_absolute_translation()
        translation = translation_text(context, to_language=translation)
        return context, translation

    async def guessing_game(self):
        await self.database.checking_user_game()
        translation = await self.database.checking_user_translation()
        user_language = await self.database.checking_user_language()
        answer, variants, level = await self.getting_data_guessing_game()
        question = translation_text(answer, to_language=user_language)
        if translation != "en":
            variants = [translation_text(i, to_language=translation) for i in variants]
            question = translation_text(answer, to_language=translation)
            answer, question = question, answer
        await self.database.updating_answer(answer=answer)
        await self.database.updating_variants_for_user(variants=variants)
        await self.database.updating_question(question=question)
        audio = await self.giving_audio()

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
            user_game = await self.database.checking_user_game()
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
        await self.database.updating_answer(answer=answer)
        await self.database.updating_variants_for_user(variants=variants)
        await self.database.updating_user_variants(variants)
        await self.database.updating_question(question=question)
        audio = await self.giving_audio()
        return variants, question, audio

    async def word_constructor(self) -> tuple | str:
        """the function splits the word into a  lists with its letters into a random order
        that is used to make inline keyboards"""
        await self.database.updating_user_game(game="word_constructor")
        answer = await self.getting_data_guessing_game(constructor="word")
        translation = await self.getting_absolute_translation()
        question = translation_text(answer, to_language=translation)
        variants = answer
        if " " in variants:
            variants = variants.replace(" ", "_")
            variants = random.sample(variants, len(variants))
        else:
            variants = random.sample(variants, len(variants))

        await self.database.updating_answer(answer=answer)
        await self.database.updating_variants_for_user(variants=variants)
        await self.database.updating_user_variants(variants)
        await self.database.updating_question(question=question)
        audio = await self.giving_audio()
        return question, variants, audio

    @staticmethod
    async def getting_jokes():
        async with aiohttp.ClientSession() as session:
            async with session.get(RandomChuckJokesApi.chuck_url) as response:
                return await response.json()

    async def getting_absolute_translation(self):
        translation = (await self.database.checking_user_translation(),
                       await self.database.checking_user_language())
        for i in translation:
            if i != 'en':
                translation = i
        return translation

    async def giving_audio(self):
        games = ['verbs', 'prepositions', 'numbers', 'nouns', 'pronouns', 'adjectives', 'conjunctions']
        user_game = await self.database.checking_user_game()

        translation = await self.database.checking_user_translation()
        if user_game in games:
            if translation == "en":
                word = await self.database.checking_answer()
            else:
                word = await self.database.checking_question()
        elif user_game == 'v' and translation == 'en':
            word = await self.database.checking_question()
        else:
            word = await self.database.checking_answer()
        audio_bytes = converting_text_to_audio(word)
        await self.database.updating_user_media_data(media=audio_bytes)
        return audio_bytes
