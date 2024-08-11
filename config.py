import os
from dotenv import load_dotenv

database_name = os.path.dirname(os.path.abspath(__file__)) + "\\" + "english_bot_database.db"
load_dotenv()

'''instead of "os.getenv("token")" u can use token="your_token" or u can add '.env' 
file with token="your_token" and put into the root off the project'''

token = os.getenv("token")

''' to set a service that provides translation '''

translator = 'google'
