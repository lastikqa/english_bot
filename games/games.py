from english_bot_database.english_bot_database import EnglishBotDatabase
import requests
from bs4 import BeautifulSoup
import random
from gtts import gTTS
import translators as ts
from config import datebase_name
from api.context_english_api import ContextEnglishApi
from api.random_chuck_jokes_api import RandomChuckJokesApi
from data.file_manager import FileManager
database_name = datebase_name


class Games:
    def __init__(self, user_id, data):
        self.user_id = user_id
        self.game_data = FileManager(data)

    def getting_context(self, word: str) -> tuple[str, str]:
        """english words should be seen in its contexts. the function gets a word and return a sentence with the word
        and translation of the sentence into russian"""
        find_word = list(word)
        find_word = find_word[0]
        word_url = word.replace(" ", "+")
        page = requests.get(
            url=ContextEnglishApi.context_english_url + word_url,
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
        translation = self.getting_absolute_translation()
        translation = ts.translate_text(context, to_language=translation)
        return context, translation

    def gusesing_game(self, user_id):
        database = EnglishBotDatabase(user_id)
        database.checking_user_game(user_id=user_id)
        translation = database.checking_user_translation(user_id=self.user_id)
        user_language = database.checking_user_language(user_id=self.user_id)
        answer, variants = self.getting_data_guessing_game()
        question = ts.translate_text(answer, to_language=user_language)
        if translation == "en":
            variants = [ts.translate_text(i, to_language=user_language) for i in variants]
            answer, question = question, answer
        database.updating_answer(answer=answer, user_id=user_id)
        database.updating_variants_for_user(user_id=user_id, variants=variants)
        database.updating_question(user_id=user_id, question=question)

        return question, variants

    def getting_data_guessing_game(self, constructor=None):
        parts_of_speech = self.game_data.reading_json()

        if constructor == "phrase":
            parts_of_speech = self.game_data.getting_random_object_from_json()
            word = random.choice([i for i in parts_of_speech[1]])
            answer, question = self.getting_context(word)
            return question, answer

        elif constructor == 'word':
            parts_of_speech = self.game_data.getting_random_object_from_json()
            word = random.choice([i for i in parts_of_speech[1]])
            return word

        else:
            user_game = EnglishBotDatabase.checking_user_game(user_id=self.user_id)
            variants_of_words = []
            list_of_words = [i for i in parts_of_speech[user_game]]
            for _ in range(9):
                variants_of_words.append(random.choice(list_of_words))

            answer = random.choice(variants_of_words)

        return answer, variants_of_words

    def constructor_phrases(self, user_id: int, language):
        database = EnglishBotDatabase(user_id)
        question, answer = self.getting_data_guessing_game(constructor="phrase")
        if language == "en":
            question, answer = answer, question
        variants = answer.split()
        variants = random.sample(variants, len(variants))
        database.updating_answer(user_id, answer=answer)
        database.updating_variants_for_user(user_id, variants=variants)
        database.updating_user_variants(user_id, variants)
        database.updating_question(user_id=user_id, question=question)
        return variants, question

    def word_constructor(self, user_id: int) -> tuple | str:
        """the function splits the word into a  lists with its letters into a random order
        that is used to make inline keyboards"""
        database = EnglishBotDatabase(user_id)
        database.updating_user_game(user_id, game="word_constructor")
        answer = self.getting_data_guessing_game(constructor="word")
        translation = self.getting_absolute_translation()
        question = ts.translate_text(answer, to_language=translation)
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

    def getting_absolute_translation(self):
        translation = (EnglishBotDatabase.checking_user_translation(user_id=self.user_id),
                       EnglishBotDatabase.checking_user_language(user_id=self.user_id))
        for i in translation:
            if i != 'en':
                translation = i
        return translation
