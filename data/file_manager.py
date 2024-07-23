import json
import random
import os


class FileManager:

    def __init__(self, filename):
        self.filename = os.path.abspath(os.getcwd()+"\\data\\"+filename)

    def reading_json(self):
        with open(self.filename, "r") as file:
            return json.load(file)

    def creating_key_list(self):
        data = self.reading_json()
        key_list = [key for key in data]
        return key_list

    def getting_random_key_from_key_list(self):
        key_list = self.creating_key_list()
        random_key = random.choice(key_list)
        return random_key

    def getting_random_object_from_json(self):
        random_key = self.getting_random_key_from_key_list()
        json_data = self.reading_json()
        return random_key, json_data[random_key]




