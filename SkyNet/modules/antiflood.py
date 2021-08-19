# Copyright © 2021 Lynx-Userbot All Rights Reserved.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Credits: Based Plugins From ( @Catuserbot )
# Ported by KENZO for Lynx-Userbot

import asyncio
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from userbot.utils.checker import is_admin
from userbot.modules.sql_helper import antiflood_sql as sql
from userbot.events import register
from userbot import bot, CMD_HELP
from userbot.utils import edit_or_reply


CHAT_FLOOD = sql.__load_flood_settings()

# Warn Mode for Anti Flood
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True
)

me = bot.get_me()
uid = me.id


@register(incoming=True, disable_edited=True, disable_errors=True)
async def _(event):
    if not CHAT_FLOOD:
        return
    admin_c = await is_admin(event.client, event.chat_id, event.client.uid)
    if not admin_c:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message=f"""**Automatic AntiFlooder**
@admin \n[👤USER](tg://user?id={event.message.sender_id}) is Flooding This Chat.
`{str(e)}`""",
            reply_to=event.message.id,
        )
        await asyncio.sleep(4)
        await no_admin_privilege_message.edit(
            "This is useless SPAM dude. Stop this, enjoy the chat buddy."
        )
    else:
        await event.client.send_message(
            entity=event.chat_id,
            message=f"""**Automatic AntiFlooder**
[👤USER](tg://user?id={event.message.sender_id}) has been automatically restricted
because he reached the defined flood limit.""",
            reply_to=event.message.id,
        )


@register(outgoing=True, pattern="^\\.setflood(?: |$)(.*)", groups_only=True)
async def _(event):
    "To Setup Antiflood in a Group to Prevent SPAM"
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "`Updating Flood Settings!`")
    await asyncio.sleep(2)
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(f"Antiflood Updated to {input_str} in The Current Chat")
    except Exception as e:
        await event.edit(str(e))


CMD_HELP.update({"antiflood": "✘ Pʟᴜɢɪɴ : Anti Flood"
                 "\n\n⚡𝘾𝙈𝘿⚡: `.setflood <Count>`"
                 "\n↳ : It Warns The User if He Spams The Chat and if You Are an Admin with Proper Rights Then it Mutes Him in That Group."
                 "\n\n**Example:** `.setflood 5`"
                 "\n\n**Note:** To Stop Antiflood, Setflood with High Value Like 999999."})
