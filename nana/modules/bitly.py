from bitlyshortener import Shortener
from pyrogram import Filters
from asyncio import sleep

from nana import app, Command, bitly_token
from nana.helpers.expand import expand_url

__MODULE__ = "Link Shortner"
__HELP__ = """
This module will shortener your link

──「 **shorten url** 」──
-> `bitly (link)`
Shorten your url with bitly

──「 **expand url** 」──
-> `expand (link)`
Reply or parse arg of url to expand
"""


@app.on_message(Filters.me & Filters.command(["bitly"], Command))
async def bitly(_client, message):
    args = message.text.split(None, 1)
    shortener = Shortener(tokens=bitly_token, max_cache_size=8192)
    if len(args) == 1:
        await message.edit("Usage bitly (url)!")
        return
    if len(args) == 2:
        await message.edit("Processing")
        urls = [args[1]]
        shortlink = shortener.shorten_urls(urls)
        await message.edit("Here Your link\n{}".format(shortlink[0]),
                                                       disable_web_page_preview=True
                                                       )


@app.on_message(Filters.command("expand", Command) & Filters.me)
async def expand(_client, message):
    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None

    if url:
        expanded = await expand_url(url)
        if expanded:
            await message.edit(
                f"<b>Shortened URL</b>: {url}\n<b>Expanded URL</b>: {expanded}", disable_web_page_preview=True
            )
            return
        else:
            await message.edit(
                "`i Cant expand this url :p`"
            )
            await sleep(3)
            await message.delete()
    else:
        await message.edit("Nothing to expand")
