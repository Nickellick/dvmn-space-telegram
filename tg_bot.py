import os

from dotenv import load_dotenv
import telegram


def main():
    load_dotenv()
    api_key = os.getenv('DVMN_TG_BOT_API_KEY')
    bot = telegram.Bot(token=api_key)
    bot.send_photo(
        chat_id='@edtestchan',
        photo=open('images/epic_2023-01-11 00:13:03.png', 'rb')
    )


if __name__ == '__main__':
    main()
