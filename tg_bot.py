import os

from dotenv import load_dotenv
import telegram


def main():
    load_dotenv()
    api_key = os.getenv('DVMN_TG_BOT_API_KEY')
    bot = telegram.Bot(token=api_key)
    bot.send_message(chat_id='@edtestchan', text='Hello, World!')


if __name__ == '__main__':
    main()
