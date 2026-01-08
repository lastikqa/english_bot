import os
from dotenv import load_dotenv

database_name = os.path.join(os.path.dirname(os.path.abspath(__file__)) , "english_bot_database.db")
load_dotenv()

'''instead of "os.getenv("token")" u ca n use token="your_token" or u can add '.env' 
file with token="your_token" and put into the root off the project'''

token = os.getenv("token")


if token is None:
    raise ValueError(
        "❌ ERROR: Token was not found\n\n"
        "📝 Raad:\n"
        "1. Make a file .env in the root of the project\n"
        "2. Add string: token=YOUR_BOT_TOKEN\n"
        "3. Replace YOUR_BOT_TOKEN  to a reale one from @BotFather\n\n"
        "🔗 Example the .env file:\n"
        "token=6994871499:AACDR-j87L4u_FWTTKAKHlqcY7v1WStbtmY"
    )

''' to set a service that provides translations '''

translator = 'google'
