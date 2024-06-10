import os
from datetime import timedelta

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

months_uk = ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня", "серпня", "вересня", "жовтня",
             "листопада", "грудня"]


async def send_tweet(tweet):
    date_tweet = f'<b>Дата</b>: <i>{format_date(tweet.date)}</i>'
    author_text = f"<b>Автор</b>: <a href='https://twitter.com/{tweet.author.screen_name}'>{tweet.author.name}</a> - {tweet.author.screen_name}"
    tweet_text = f"<b>Текст</b>: {tweet.text}"
    text = f"{date_tweet}\n\n{author_text}\n\n{tweet_text}"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Посилання на твіт', url=tweet.url))

    return await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        reply_markup=builder.as_markup(),
        disable_web_page_preview=True
    )


def format_date(date):
    kyiv_time = date + timedelta(hours=3)
    return f"{kyiv_time.day} {months_uk[kyiv_time.month - 1]} {kyiv_time.year} о {kyiv_time.hour}:{kyiv_time.minute:02}"
