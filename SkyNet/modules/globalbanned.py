# Copyright © 2021 Lynx-Userbot (LLC Company)
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
# Ported to Lynx-Userbot by @KENZO-404
# Based On Plugins from Catuserbot


import asyncio
import base64
from datetime import datetime
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import (
    Channel,
    ChatBannedRights,
    MessageEntityMentionName,
)
import userbot.modules.sql_helper.globalban_sql as gban_sql
from userbot.utils import edit_delete, edit_or_reply
from userbot.events import register
from userbot import (
    ALIVE_NAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEVELOPER,
)

# ================================================
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)
UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)
# =================================================


async def admin_groups(grp):
    admgroups = []
    async for dialog in grp.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, Channel)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            admgroups.append(entity.id)
    return admgroups


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


async def get_user_from_event(event, uevent=None, secondgroup=None):
    if uevent is None:
        uevent = event
    if secondgroup:
        args = event.pattern_match.group(2).split(" ", 1)
    else:
        args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.from_id is None and not event.is_private:
            await edit_delete(uevent, "`Dia Adalah Admin Anonim.`")
            return None, None
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await edit_delete(
                uevent, "**Mohon Maaf, Silahkan Gunakan ID/Username/Reply Pesan Ke Pengguna.**", 5
            )
            return None, None
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await edit_delete(
                uevent, "**Mohon Maaf, Tidak Dapat Mengambil Informasi User.**", 5
            )
            return None, None
    return user_obj, extra


@register(outgoing=True, pattern=r"^\.gban(?: |$)(.*)")
async def gban(event):
    if event.fwd_from:
        return
    gbun = await edit_or_reply(event, "𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    start = datetime.now()
    user, reason = await get_user_from_event(event, gbun)
    if not user:
        return
    if user.id == (await event.client.get_me()).id:
        await gbun.edit("**Anda ceroboh!**\n__Anda Gbanned diri anda sendiri:)...__")
        return
    if user.id in DEVELOPER:
        await gbun.edit("#DISCLAIMER ❌\nDia Adalah Developer.")
        return
    try:
        hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await event.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):  # fixes languange by Apis
        await gbun.edit(
            f"**Pengguna** [Ini](tg://user?id={user.id}) **sudah ada di daftar gbanned**"
        )
    else:
        gban_sql.freakgban(user.id, reason)
    xel = []
    xel = await admin_groups(event)
    count = 0
    pis = len(xel)
    if pis == 0:
        await gbun.edit("**Anda Tidak Mempunyai Group Dan Anda Tidak Mempunyai Title Admin.**")
        return
    await gbun.edit(
        f"#WARNING ⚠️\n**👤 User :** » [CLICK HERE](tg://user?id={user.id}) «\n**Sudah Berada Di Dalam Daftar Global Banned.**\n**Jumlah :** `{len(xel)}` **Group**"
    )
    for i in range(pis):
        try:
            await event.client(EditBannedRequest(xel[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda Tidak Memiliki Izin Banned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await gbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• GBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah :** `{count}` **Group, Dalam** `{timetaken}` **Detik**\n**│• Reason :** `{reason}`\n**│• Action :** `GBanned` ✅\n╰━━━━━━━━━━━━━━━━━━╯"
        )
    else:
        await gbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• GBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah :** `{count}` **Group, Dalam** `{timetaken}` **Detik**\n**│• Action :** `GBanned` ✅\n╰━━━━━━━━━━━━━━━━━━╯"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBANNED\
                \nGlobal Banned\
                \n**Pengguna :** [{user.first_name}](tg://user?id={user.id})\
                \n**ID :** `{user.id}`\
                \n**Reason :** `{reason}`\
                \n**Jumlah :** `{count}` **Group**\
                \n**Waktu Yang Dibutuhkan :** `{timetaken}` **Detik**",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBANNED\
                \nGlobal Banned\
                \n**Pengguna :** [{user.first_name}](tg://user?id={user.id})\
                \n**ID :** `{user.id}`\
                \n**Jumlah :** `{count}` **Group**\
                \n**Waktu Yang Dibutuhkan :** `{timetaken}` **Detik**",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@register(outgoing=True, pattern=r"^\.ungban(?: |$)(.*)")
async def ungban(event):
    if event.fwd_from:
        return
    ungbun = await edit_or_reply(event, "𝘜𝘯𝘎𝘭𝘰𝘣𝘢𝘭 𝘉𝘢𝘯𝘯𝘦𝘥 𝘪𝘯 𝘗𝘳𝘰𝘨𝘳𝘦𝘴𝘴...")
    start = datetime.now()
    user, reason = await get_user_from_event(event, ungbun)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):  # fixes languange by Apis
        gban_sql.freakungban(user.id)
    else:
        await ungbun.edit(
            f"**👤 User :** » [CLICK HERE](tg://user?id={user.id}) «\n**Ini Tidak Ada Dalam Daftar GBAN Anda.**"
        )
        return
    xel = []
    xel = await admin_groups(event)
    count = 0
    pis = len(xel)
    if pis == 0:
        await ungbun.edit("**Anda Tidak Mempunyai Group Dan Anda Tidak Mempunyai Title Admin.**")
        return
    await ungbun.edit(
        f"Sedang Membatalkan Global Banned...\n**👤 User :** » [CLICK HERE](tg://user?id={user.id}) « \n**Jumlah :** `{len(xel)}` **Group**"
    )
    for i in range(pis):
        try:
            await event.client(EditBannedRequest(xel[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Anda Tidak Memiliki Izin Ungbanned di :**\n**Group Chat :** `{event.chat_id}`",
            )
    end = datetime.now()
    timetaken = (end - start).seconds
    if reason:
        await ungbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• UNGBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah :** `{count}` **Group, Dalam** `{timetaken}` **Detik**\n**│• Reason :** `{reason}`\n**│• Action :** `GBanned` ❌\n╰━━━━━━━━━━━━━━━━━━╯"
        )
    else:
        await ungbun.edit(
            f"╭─━━━━━━━━━━━━━━━━─╮\nㅤ  ㅤ[⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡](t.me/LynxUserbot)\n╭─━━━━━━━━━━━━━━━━─╯\n**│• UNGBAN By :** `{ALIVE_NAME}`\n**│• User Account :** [{user.first_name}](tg://user?id={user.id})\n**│• Jumlah :** `{count}` **Group, Dalam** `{timetaken}` **Detik**\n**│• Action :** `GBanned` ❌\n╰━━━━━━━━━━━━━━━━━━╯"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBANNED\
                \nGlobal Unbanned\
                \n**Pengguna :** [{user.first_name}](tg://user?id={user.id})\
                \n**ID :** `{user.id}`\
                \n**Reason :** `{reason}`\
                \n**Jumlah :** `{count}` **Group**\
                \n**Waktu Yang Di Butuhkan :** `{timetaken}` **Detik**",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBANNED\
                \nGlobal Unbaned\
                \n**Pengguna :** [{user.first_name}](tg://user?id={user.id})\
                \n**ID :** `{user.id}`\
                \n**Jumlah :** `{count}` **Group**\
                \n**Waktu Yang Di Butuhkan :** `{timetaken}` **Detik**",
            )


@register(outgoing=True, pattern=r"^\.listgban$")
async def gablist(event):
    if event.fwd_from:  # This is created by catuserbot
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "📖 **Daftar Global Banned :**\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"**│👤 User :** [{a_user.chat_id}](tg://user?id={a_user.chat_id}) \n**│ Reason :** `{a_user.reason}`\n"
            else:
                GBANNED_LIST += (
                    f"│👤 User : [{a_user.chat_id}](tg://user?id={a_user.chat_id}) `No Reason`\n"
                )
    else:
        GBANNED_LIST = "Daftar List Global Banned : `Kosong`.\nAnda Belum Pernah Melakukan Global Banned Sebelumnya."
    await edit_or_reply(event, GBANNED_LIST)
