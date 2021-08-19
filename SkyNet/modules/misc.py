# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import sys
import io
import sys
from random import randint
from time import sleep
from os import environ, execle
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import register
from userbot.utils import time_formatter


@register(outgoing=True, pattern=r"^\.random")
async def randomise(items):
    """For .random command, get a random item from the list of items."""
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        return await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
    index = randint(1, len(itemo) - 1)
    await items.edit(
        "**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`"
    )


@register(outgoing=True, pattern=r"^\.sleep ([0-9]+)$")
async def sleepybot(time):
    """For .sleep command, let the userbot snooze for a few second."""
    counter = int(time.pattern_match.group(1))
    await time.edit("`I am sulking and snoozing...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern=r"^\.shutdown$")
async def killthebot(event):
    """For .shutdown command, shut the bot down."""
    await event.edit("`Shutting down...`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#SHUTDOWN \n" "Bot shut down")
    await bot.disconnect()


@register(outgoing=True, pattern=r"^\.restart$")
async def killdabot(event):
    await event.edit("`i would be back in a moment`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#RESTART \n" "Restarting bot..."
        )
    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit(
        "Here's Something for You to Read :\n"
        "\n[⚡Lynx-Userbot⚡ Repo](https://zee.gl/lynx404)"
        "\n[Setup Guide - Basic](https://telegra.ph/How-to-host-a-Telegram-Userbot-11-02)"
        "\n[Special - Note](https://telegra.ph/Special-Note-11-02)")


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern=r"^\.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for _ in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """For .repo command, just returns the repo URL."""
    await wannasee.edit(
        "╭─━━━━━━━━━━━━━─╮\n"
        "                  ʀᴇᴘᴏ\n"
        "    [⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](https://zee.gl/lynx404)\n"
        "╭─━━━━━━━━━━━━━─╯\n"
        "│⊙ **Dᴇᴠᴇʟᴏᴘᴇʀ :** [👤DEV](https://zee.gl/KENZO404)\n"
        "╰━━━━━━━━━━━━━━━╯\n"
        "  𝗟𝗶𝗰𝗲𝗻𝘀𝗲 : [Raphielscape Public License 1.d](https://github.com/KENZO-404/Lynx-Userbot/blob/Lynx-Userbot/LICENSE)\n"
        "  **Cᴏᴘʏʀɪɢʜᴛ © 𝟤𝟢𝟤𝟣** @LynxUserbot"
    )


@register(outgoing=True, pattern=r"^\.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit("`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`",
        )


CMD_HELP.update({
    "random": "✘ Pʟᴜɢɪɴ : Random List\
    \n\n⚡𝘾𝙈𝘿⚡: `.random <item1> <item2> ... <itemN>`\
    \n↳ : Get a Random Item From The List of Items.",
    "sleep": "✘ Pʟᴜɢɪɴ : Sleep\
    \n\n⚡𝘾𝙈𝘿⚡: `.sleep <seconds>`\
    \n↳ : Let Yours Snooze for a Few Seconds.",
    "shutdown": "✘ Pʟᴜɢɪɴ : Shutdown\
    \n\n⚡𝘾𝙈𝘿⚡: `.shutdown`\
    \n↳ : Shutdown bot",
    "repo": "✘ Pʟᴜɢɪɴ : Repository\
    \n\n⚡𝘾𝙈𝘿⚡: `.repo`\
    \n↳ : Github Repo of this bot",
    "readme": "✘ Pʟᴜɢɪɴ : Read Me\
    \n\n⚡𝘾𝙈𝘿⚡: `.readme`\
    \n↳ : Provide Links to Setup The Userbot and it's modules.",
    "repeat": "✘ Pʟᴜɢɪɴ : Repeat\
    \n\n⚡𝘾𝙈𝘿⚡: `.repeat <no> <Text>`\
    \n↳ : Repeats The Text for a Number of Times. Don't Confuse This With Spam tho.",
    "restart": "✘ Pʟᴜɢɪɴ : Restart\
    \n\n⚡𝘾𝙈𝘿⚡: `.restart`\
    \n↳ : Restarts the bot !!",
    "raw": "✘ Pʟᴜɢɪɴ : RAW\
    \n\n⚡𝘾𝙈𝘿⚡: `.raw`\
    \n↳ : Get Detailed JSON-Like Formatted Data About Replied Message."
})
