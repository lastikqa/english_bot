languages = ['af', 'am', 'ar', 'as', 'az', 'ba', 'bg', 'bho', 'bn', 'bo', 'brx', 'bs', 'ca', 'cs', 'cy', 'da', 'de',
             'doi', 'dsb', 'dv', 'el', 'es', 'et', 'eu', 'fa', 'fi', 'fil', 'fj', 'fo', 'fr', 'fr-CA', 'ga', 'gl',
             'gom', 'gu', 'ha', 'he', 'hi', 'hne', 'hr', 'hsb', 'ht', 'hu', 'hy', 'id', 'ig', 'ikt', 'is', 'it', 'iu',
             'iu-Latn', 'ja', 'ka', 'kk', 'km', 'kmr', 'kn', 'ko', 'ks', 'ku', 'ky', 'ln', 'lo', 'lt', 'lug', 'lv',
             'lzh', 'mai', 'mg', 'mi', 'mk', 'ml', 'mn-Cyrl', 'mn-Mong', 'mr', 'ms', 'mt', 'mww', 'my', 'nb', 'ne',
             'nl', 'nso', 'nya', 'or', 'otq', 'pa', 'pl', 'prs', 'ps', 'pt', 'pt-PT', 'ro', 'ru', 'run', 'rw', 'sd',
             'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr-Cyrl', 'sr-Latn', 'st', 'sv', 'sw', 'ta', 'te', 'th', 'ti',
             'tk', 'tlh-Latn', 'tn', 'to', 'tr', 'tt', 'ty', 'ug', 'uk', 'ur', 'uz', 'vi', 'xh', 'yo', 'yua', 'yue',
             'zh-Hans', 'zh-Hant', 'zu', "cn"]

about_the_bot_keyboard = {"Bot Commands": "/bot_commands", "Guess Words": "/guess_words",
                          "Constructor Games": "/constructor_games", "About The Rating": "/rating"}

bot_commands = r"""_\!setnicname 'Nickname'_ \- to set your nickname

_\!setidiom 'stir up a hornet's nest: provoke trouble'_ \- to add idioms

_\!setlanguage 'de'_ \- to set your language \( 'de' \- German language\. use language codes\) """


guess_words = r"""**_Guess Word game_**

You need to choose rights translation for words"""


constructor_games = r"""**_Words Constructor_**

You need to create a right word from its own letters

Of course it is a random order of the letters


**_Phrase Constructor_**

You need to create a right sentence from its own words

Of course it is a random order of the words

The sentence can be 'your language' to english or english to 'your language'"""


rating = """The word can be 'your language' to english or english to your language

_Remember the more your wins in a row the higher your rating_

_If u wins 3 times in a row u get 3 as your score_

_But if u get fail and after the fail u win

_u still have 3 as your score until u get 4 or more in a row"""