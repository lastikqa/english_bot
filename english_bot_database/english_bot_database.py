import sqlite3
from config import database_name


class EnglishBotDatabase:
    def __init__(self, user_id):
        self.user_id = user_id
        self.database_name = database_name

    @staticmethod
    def creating_users_db():
        """the function just creates 'sqlite3' database to save some information about users """
        connect = sqlite3.connect(database_name)
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    user_id INTEGER,
                    first_name TEXT,
                    translation TEXT,
                    user_language TEXT,
                    game TEXT,
                    question TEXT,
                    answer TEXT,
                    user_answer TEXT,
                    variants TEXT,
                    user_variants TEXT,
                    user_score INTEGER,
                    counter_user_score INTEGER,
                    media_data BLOB
                    )
                """)

        connect.commit()
        connect.close()

    def creating_object_user_in_db(self, first_name: str):
        """Create a new object in db. the function gets user id from telegram and username"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Users (user_id, first_name,  translation, user_language, game, '
                       'question, answer, user_answer, variants, user_variants, '
                       'user_score, counter_user_score, media_data) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, first_name, "en", "ru", "", "", "", "", "", "", 0, 0, None))
        connect.commit()
        connect.close()

    def looking_for_user_in_db(self) -> bool:
        """This function gets user id from telegram and returns True if the one in database
        and False if the one does not exist in database"""
        user_id: int = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM Users WHERE user_id=?', (user_id,))
        user = cursor.fetchall()
        connect.close()
        if len(user) > 0:
            return True
        else:
            return False

    def checking_user_game(self) -> str | None:
        """the function checks game which user is playing and returns the name of the game"""
        user_id: int = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT game FROM Users WHERE user_id=?', (user_id,))
        game = cursor.fetchone()
        connect.close()
        try:
            return game[0]
        except TypeError:
            return None

    def updating_answer(self, answer: str):
        """the function updated  answer for the game"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET answer = ? WHERE user_id = ?', (answer, user_id))
        connect.commit()
        connect.close()

    def updating_question(self, question: str):
        """the function updated question for tge game"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET question = ? WHERE user_id = ?', (question, user_id))
        connect.commit()
        connect.close()

    def checking_question(self) -> str:
        """the function checks question for user"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT question FROM Users WHERE user_id=?', (user_id,))
        question = cursor.fetchone()
        connect.close()
        try:
            return question[0]
        except TypeError:
            return ""

    def updating_user_game(self, game: str = None):
        """the function updates user game"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET game = ? WHERE user_id = ?', (game, user_id))
        connect.commit()
        connect.close()

    def updating_user_translation(self, translation):
        """the function updates user translation"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET translation = ? WHERE user_id = ?', (translation, user_id))
        connect.commit()
        connect.close()

    def checking_user_translation(self):
        """the function checks user translation"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT translation FROM Users WHERE user_id=?', (user_id,))
        translation = cursor.fetchone()
        connect.close()
        try:
            return translation[0]
        except TypeError:
            return None

    def checking_variants_for_user(self):
        """the function checks user variants"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT variants FROM Users WHERE user_id=?', (user_id,))
        variants = cursor.fetchone()
        connect.close()
        try:
            return variants[0].split()
        except TypeError:
            return None

    def updating_variants_for_user(self, variants: list):
        """the function updates variants """
        user_id = self.user_id
        variants = " ".join(variants)
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET variants = ? WHERE user_id = ?', (variants, user_id))
        connect.commit()
        connect.close()

    def checking_answer(self) -> str:
        """the function checks game which user is playing and returns the name of the game"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT answer FROM Users WHERE user_id=?', (user_id,))
        answer = cursor.fetchone()
        connect.close()
        try:
            return answer[0]
        except TypeError:
            return ""

    def updating_user_variants(self, var: list | None = None):
        user_id = self.user_id
        var = " ".join(var)
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET user_variants = ? WHERE user_id = ?', (var, user_id))
        connect.commit()
        connect.close()

    def checking_user_score(self) -> int:
        """the function check user score"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT user_score FROM Users WHERE user_id=?', (user_id,))
        user_score = cursor.fetchone()
        connect.close()
        return int(user_score[0])

    def updating_score_count(self, win: int = 0):
        """the function updates counter of user wins if win +=1, else win =0"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET counter_user_score = ? WHERE user_id = ?', (win, user_id))
        connect.commit()
        connect.close()

    def checking_counter_user_score(self) -> int:
        """the function check user score"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT counter_user_score FROM Users WHERE user_id=?', (user_id,))
        counter_user_score = cursor.fetchone()
        connect.close()
        return int(counter_user_score[0])

    def updating_user_score(self, counter: int):
        """the function updates user_score in database"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET user_score = ? WHERE user_id = ?', (counter, user_id))
        connect.commit()
        connect.close()

    def checking_user_answer(self) -> str:
        """the function checks user answers and returns a str"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT user_answer FROM Users WHERE user_id=?', (user_id,))
        user_answer = cursor.fetchone()
        connect.close()
        if user_answer[0] is None:
            user_answer = ""
            return user_answer
        else:
            return user_answer[0]

    def updating_user_answer(self, user_answer: str | None = None):
        """the functions updates variant of user answer"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET user_answer = ? WHERE user_id = ?', (user_answer, user_id))
        connect.commit()
        connect.close()

    def checking_user_variants(self) -> list:
        """the function checks available variants for user and returns list of that """
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT user_variants FROM Users WHERE user_id=?', (user_id,))
        user_variants = cursor.fetchone()
        connect.close()
        if " " in user_variants[0]:
            user_variants = user_variants[0].split()
            return user_variants
        else:
            user_variants = list(user_variants)
            return user_variants

    def updating_user_rating(self, win: bool = True):
        """the function updates user rating"""

        if win is True:
            win = self.checking_counter_user_score() + 1
            self.updating_score_count(win=win)
        else:
            user_score = self.checking_user_score()
            counter_user_score = self.checking_counter_user_score()
            if counter_user_score > user_score:
                self.updating_user_score(counter=counter_user_score)
            self.updating_score_count()

    def updating_user_first_name(self, nickname: str):
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET first_name = ? WHERE user_id = ?', (nickname, user_id))
        connect.commit()
        connect.close()

    def getting_user_scores(self) -> tuple[tuple | str] | str:
        """the function gets user scores to show it to user"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('select first_name, user_score FROM Users order by user_score limit 5')
        user_scores = cursor.fetchall()
        cursor.execute('select first_name, user_score FROM Users where user_id = ?', (user_id,))
        current_user_score = cursor.fetchone()
        connect.close()
        text = "User Rating"
        for i in user_scores:
            text += "\n" + i[0] + " " + str(i[1])
        if current_user_score in user_scores:
            return text
        else:
            text += "\n" + current_user_score[0] + " " + str(current_user_score[-1])

    def updating_user_language(self, language: str):
        """the function updates user language"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET user_language = ? WHERE user_id = ?', (language, user_id))
        connect.commit()
        connect.close()

    def checking_user_language(self) -> int:
        """the function check user language"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT user_language FROM Users WHERE user_id=?', (user_id,))
        user_language = cursor.fetchone()
        connect.close()
        return user_language[0]

    def getting_user_media_data(self) -> int:
        """the function check user media data"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('SELECT media_data FROM Users WHERE user_id=?', (user_id,))
        media = cursor.fetchone()
        connect.close()
        return media[0]

    def updating_user_media_data(self, media: str | None = None):
        """the function updates user media data"""
        user_id = self.user_id
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute('UPDATE Users SET media_data = ? WHERE user_id = ?', (media, user_id))
        connect.commit()
        connect.close()
