#!/user/bin/python3

from telethon import TelegramClient, events
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from os import getenv
from requests import get

if not __name__ == "__main__":
    exit()

load_dotenv(find_dotenv())

api_id = getenv("TELEGRAM_API_ID")
api_hash = getenv("TELEGRAM_API_HASH")
phone = getenv("TELEGRAM_PHONE_NO")
session = Path(__file__).parent.absolute().as_posix() + '/' + getenv("TELEGRAM_SESSION_FILE")

client = TelegramClient(session, api_id, api_hash, sequential_updates = True)

@client.on(events.NewMessage(incoming = True, pattern = '.+trump.+'))
async def respond_with_trump_quote(event):
    if not event.is_private:
        return

    sender = await event.client.get_entity(event.from_id)
    if sender.bot:
        return

    response = get("https://api.whatdoestrumpthink.com/api/v1/quotes/random")
    if not response.status_code == 200:
        return

    quote_data = response.json()
    await event.message.respond(quote_data["message"] + "\n- Donald John Trump, 45th President of the USA")


@client.on(events.NewMessage(incoming = True, pattern = '^RIP$'))
async def respond_thanks(event):
    if not event.is_private:
        return

    sender = await event.client.get_entity(event.from_id)
    if sender.bot:
        return

    await event.message.respond("Danke 😊")

client.start(phone)
client.run_until_disconnected()

