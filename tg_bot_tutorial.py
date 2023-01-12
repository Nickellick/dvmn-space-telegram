import os

from dotenv import load_dotenv
import telegram

load_dotenv()
api_key = os.getenv('DVMN_TG_BOT_API_KEY')

bot = telegram.Bot(token=api_key)

# Checking credentials
print(bot.get_me())

# Fetching updates (including new messages)
updates = bot.get_updates()
print(updates[0])

# Writing back something to user
bot.send_message(text='Hi, User!', chat_id=132969533)
