# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# @Qulec tarafından yazılmıştır.
# Thanks @Spechide.

import logging

from userbot import BOT_USERNAME, BOT_TOKEN
from userbot.events import register
from telethon.errors.rpcerrorlist import BotInlineDisabledError


logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.WARNING)


@register(outgoing=True, pattern=r"^\.helpme")
async def yardim(event):
    lynxbotusername = BOT_USERNAME
    if lynxbotusername and BOT_TOKEN:
        try:
            results = await event.client.inline_query(
                lynxbotusername,
                "@LynxRobot"
            )
        except BotInlineDisabledError:
            return await event.edit("`Bot can't be used in inline mode.\nMake sure to turn on inline mode!`")
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=False
        )
        await event.delete()
    else:
        return await event.edit("`The bot doesn't work! Please set the Bot Token and Username correctly.`"
                                "\n`The module has been stopped.`")


@register(outgoing=True, pattern=r"^\.alynx")
async def alyynx(event):
    botusername = BOT_USERNAME
    if botusername and BOT_TOKEN:
        try:
            resullt = await event.client.inline_query(
                botusername,
                "@LynxAliveRobot"
            )
        except BotInlineDisabledError:
            return await event.edit("`Bot can't be used in inline mode.\nMake sure to turn on inline mode!`")
        await resullt[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=False
        )
        await event.delete()
    else:
        return await event.edit("`The bot doesn't work! Please set the Bot Token and Username correctly.`"
                                "\n`The module has been stopped.`")
