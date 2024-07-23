import json
import random
import os


class FileManager:

    def __init__(self, filename):
        self.filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + filename

    def reading_json(self):
        with open(self.filename, "r") as file:
            return json.load(file)

    def writing_json(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def creating_key_list(self) -> list:
        data = self.reading_json()
        key_list = [key for key in data]
        return key_list

    def getting_random_key_from_key_list(self) -> str:
        key_list = self.creating_key_list()
        random_key = random.choice(key_list)
        return random_key

    def getting_random_object_from_json(self) -> tuple[str, str | list]:
        random_key = self.getting_random_key_from_key_list()
        json_data = self.reading_json()
        return random_key, json_data[random_key]

    def updating_json(self, text: str):
        json_object = self.reading_json()
        if "!setidiom" in text:
            text = text.replace("!setidiom", "")
            text = text.split(":")
            json_object[str(text[0].strip())] = str(text[1].strip())

        self.writing_json(json_object)
