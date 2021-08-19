# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module for keeping control who PM you."""

import os
from sqlalchemy.exc import IntegrityError
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import User
from userbot.events import register
from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    COUNT_PM,
    LASTMSG,
    LOGS,
    ALIVE_LOGO,
    PM_AUTO_BAN,
    CUSTOM_PMPERMIT_TEXT,
    DEFAULTUSER,
)


PM_PERMIT_PIC = os.environ.get(
    "PM_PERMIT_PIC",
    None) or "https://telegra.ph/file/78db3f8bc07d3c4a42c4f.mp4"
if PM_PERMIT_PIC is None:
    WARN_PIC = ALIVE_LOGO
else:
    WARN_PIC = str(PM_PERMIT_PIC)

COUNT_PM = {}
LASTMSG = {}

# ========================= CONSTANTS ============================

CUSTOM_MIDDLE_PMP = str(
    CUSTOM_PMPERMIT_TEXT) if CUSTOM_PMPERMIT_TEXT else f"│Karena Saya Akan Otomatis Memblokir\n│Anda, Tunggu Sampai {DEFAULTUSER}\n│Menerima Pesan Anda, Terimakasih.\n"
DEF_UNAPPROVED_MSG = (
    "◄┈─╼━━━━━━━━━━━━━━━━━━╾─┈╮\n"
    "ㅤ  “𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐓𝐡𝐞 𝐏𝐫𝐢𝐯𝐚𝐜𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞.”\n"
    "╭┈─╼━━━━━━━━━━━━━━━━━━╾─┈╯\n"
    "│❗𝘿𝙄𝙇𝘼𝙍𝘼𝙉𝙂 𝙈𝙀𝙇𝘼𝙆𝙐𝙆𝘼𝙉 𝙎𝙋𝘼𝙈❗\n│\n"
    f"{CUSTOM_MIDDLE_PMP}│\n"
    "╰┈─────────────────────┈─➤\n"
    "▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n"
    "┣[○› `PESAN OTOMATIS`\n"
    f"┣[○› `BY` © @LynxUserbot\n"
    "▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱")

# ================================================================


@register(incoming=True, disable_edited=True, disable_errors=True)
async def permitpm(event):
    """Prohibits people from PMing you without approval.\
        Will block retarded nibbas automatically."""
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not (await event.get_sender()).bot
    ):
        try:
            from userbot.modules.sql_helper.globals import gvarstatus
            from userbot.modules.sql_helper.pm_permit_sql import is_approved
        except AttributeError:
            return
        apprv = is_approved(event.chat_id)
        notifsoff = gvarstatus("NOTIF_OFF")

        # Use user custom unapproved message
        getmsg = gvarstatus("unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
            WARN_PIC = getmsg
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG
            WARN_PIC = PM_PERMIT_PIC
        # This part basically is a sanity check
        # If the message that sent before is Unapproved Message
        # then stop sending it again to prevent FloodHit
        if not apprv and event.text != UNAPPROVED_MSG:
            if event.chat_id in LASTMSG:
                prevmsg = LASTMSG[event.chat_id]
                # If the message doesn't same as previous one
                # Send the Unapproved Message again
                if event.text != prevmsg:
                    async for message in event.client.iter_messages(
                        event.chat_id, from_user="me", search=UNAPPROVED_MSG, file=WARN_PIC
                    ):
                        await message.delete()
                    await event.reply(f" {WARN_PIC} \n\n {UNAPPROVED_MSG} ")
                LASTMSG.update({event.chat_id: event.text})
            else:
                await event.reply(f" {WARN_PIC} \n\n {UNAPPROVED_MSG} ")
                LASTMSG.update({event.chat_id: event.text})

            if notifsoff:
                await event.client.send_read_acknowledge(event.chat_id)
            if event.chat_id not in COUNT_PM:
                COUNT_PM.update({event.chat_id: 1})
            else:
                COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1

            if COUNT_PM[event.chat_id] > 5:
                await event.respond(
                    "`Anda Telah Di Blokir Karna Melakukan Spam Pesan`\n"
                    "`Ke Room Chat Saya`\n"
                    "`Bye...`"
                )

                try:
                    del COUNT_PM[event.chat_id]
                    del LASTMSG[event.chat_id]
                except KeyError:
                    if BOTLOG:
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            "Mohon Maaf, Telah Terjadi Masalah Saat Menghitung Private Message, Mohon Restart Lynx !",
                        )
                    return LOGS.info("CountPM wen't rarted boi")

                await event.client(BlockRequest(event.chat_id))
                await event.client(ReportSpamRequest(peer=event.chat_id))

                if BOTLOG:
                    name = await event.client.get_entity(event.chat_id)
                    name0 = str(name.first_name)
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "["
                        + name0
                        + "](tg://user?id="
                        + str(event.chat_id)
                        + ")"
                        + " Telah Diblokir Karna Melakukan Spam Ke Room Chat",
                    )


@register(disable_edited=True, outgoing=True, disable_errors=True)
async def auto_accept(event):
    """Will approve automatically if you texted them first."""
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if (
        event.is_private
        and event.chat_id != 777000
        and event.chat_id != self_user.id
        and not (await event.get_sender()).bot
    ):
        try:
            from userbot.modules.sql_helper.globals import gvarstatus
            from userbot.modules.sql_helper.pm_permit_sql import approve, is_approved
        except AttributeError:
            return

        # Use user custom unapproved message
        get_message = gvarstatus("unapproved_msg")
        if get_message is not None:
            UNAPPROVED_MSG = get_message
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG
            UNAPPROVED_MSG = PM_PERMIT_PC
        chat = await event.get_chat()
        if isinstance(chat, User):
            if is_approved(event.chat_id) or chat.bot:
                return
            async for message in event.client.iter_messages(
                event.chat_id, reverse=True, limit=1
            ):
                if (
                    message.text is not UNAPPROVED_MSG
                    and message.from_id == self_user.id
                ):
                    try:
                        approve(event.chat_id)
                    except IntegrityError:
                        return

                if is_approved(event.chat_id) and BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#AUTO-APPROVED\n"
                        + "👤 User : "
                        + f"[{chat.first_name}](tg://user?id={chat.id})",
                    )


@register(outgoing=True, pattern=r"^\.notifoff$")
async def notifoff(noff_event):
    """For .notifoff command, stop getting notifications from unapproved PMs."""
    try:
        from userbot.modules.sql_helper.globals import addgvar
    except AttributeError:
        return await noff_event.edit("`Running on Non-SQL mode!`")
    addgvar("NOTIF_OFF", True)
    await noff_event.edit("#NOTIF OFF ❌\n`Notifikasi Dari Pesan Pribadi Telah Dinonaktifkan.`")


@register(outgoing=True, pattern=r"^\.notifon$")
async def notifon(non_event):
    """For .notifoff command, get notifications from unapproved PMs."""
    try:
        from userbot.modules.sql_helper.globals import delgvar
    except AttributeError:
        return await non_event.edit("`Running on Non-SQL mode!`")
    delgvar("NOTIF_OFF")
    await non_event.edit("#NOTIF ON ☑️\n`Notifikasi Dari Pesan Pribadi Telah Diaktifkan.`")


@register(outgoing=True, pattern=r"^\.approve(?:$| )(.*)")
async def approvepm(apprvpm):
    """For .approve command, give someone the permissions to PM you."""
    try:
        from userbot.modules.sql_helper.globals import gvarstatus
        from userbot.modules.sql_helper.pm_permit_sql import approve
    except AttributeError:
        return await apprvpm.edit("`Running on Non-SQL mode!`")

    if apprvpm.reply_to_msg_id:
        reply = await apprvpm.get_reply_message()
        replied_user = await apprvpm.client.get_entity(reply.sender_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    elif apprvpm.pattern_match.group(1):
        inputArgs = apprvpm.pattern_match.group(1)
        if inputArgs.isdigit():
            inputArgs = int(inputArgs)
        try:
            user = await apprvpm.client.get_entity(inputArgs)
        except BaseException:
            return await apprvpm.edit("`Invalid username/ID.`")
        if not isinstance(user, User):
            return await apprvpm.edit("`You're not referring to a user.`")
        uid = user.id
        name0 = str(user.first_name)
    else:
        aname = await apprvpm.client.get_entity(apprvpm.chat_id)
        if not isinstance(aname, User):
            return await apprvpm.edit("`You're not referring to a user.`")
        name0 = str(aname.first_name)
        uid = apprvpm.chat_id

    # Get user custom msg
    getmsg = gvarstatus("unapproved_msg")
    if getmsg is not None:
        UNAPPROVED_MSG = getmsg
    else:
        UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

    async for message in apprvpm.client.iter_messages(
        apprvpm.chat_id, from_user="me", search=UNAPPROVED_MSG
    ):
        await message.delete()

    try:
        approve(uid)
    except IntegrityError:
        return await apprvpm.edit("`User may already be approved.`")

    await apprvpm.edit(f"[{name0}](tg://user?id={uid}) `approved to PM!`")

    if BOTLOG:
        await apprvpm.client.send_message(
            BOTLOG_CHATID,
            "#APPROVED\n" + "👤 User : " + f"[{name0}](tg://user?id={uid})",
        )


@register(outgoing=True, pattern=r"^\.disapprove(?:$| )(.*)")
async def disapprovepm(disapprvpm):
    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove
    except BaseException:
        return await disapprvpm.edit("`Running on Non-SQL mode!`")

    if disapprvpm.reply_to_msg_id:
        reply = await disapprvpm.get_reply_message()
        replied_user = await disapprvpm.client.get_entity(reply.sender_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        dissprove(aname)
        uid = replied_user.id
    elif disapprvpm.pattern_match.group(1):
        inputArgs = disapprvpm.pattern_match.group(1)
        if inputArgs.isdigit():
            inputArgs = int(inputArgs)
        try:
            user = await disapprvpm.client.get_entity(inputArgs)
        except BaseException:
            return await disapprvpm.edit("`Invalid username/ID.`")
        if not isinstance(user, User):
            return await disapprvpm.edit("`This can be done only with users.`")
        uid = user.id
        dissprove(uid)
        name0 = str(user.first_name)
    else:
        dissprove(disapprvpm.chat_id)
        aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
        if not isinstance(aname, User):
            return await disapprvpm.edit("`You're not reffering to a User`")
        name0 = str(aname.first_name)
        uid = disapprvpm.chat_id

    await disapprvpm.edit(f"[{name0}](tg://user?id={uid}) `disaproved to PM!`")

    if BOTLOG:
        await disapprvpm.client.send_message(
            BOTLOG_CHATID,
            "#DISAPPROVED\n" + "👤 User : " + f"[{name0}](tg://user?id={uid})",
        )


@register(outgoing=True, pattern=r"^\.block$")
async def blockpm(block):
    """For .block command, block people from PMing you!"""
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client.get_entity(reply.sender_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        await block.client(BlockRequest(replied_user.id))
        await block.edit("`You've been blocked!`")
        uid = replied_user.id
    else:
        await block.client(BlockRequest(block.chat_id))
        aname = await block.client.get_entity(block.chat_id)
        if not isinstance(aname, User):
            return await block.edit("`You're not referring to a User`")
        await block.edit("`You've been blocked!`")
        name0 = str(aname.first_name)
        uid = block.chat_id

    try:
        from userbot.modules.sql_helper.pm_permit_sql import dissprove

        dissprove(uid)
    except AttributeError:
        pass

    if BOTLOG:
        await block.client.send_message(
            BOTLOG_CHATID,
            "#BLOCKED\n" + "👤 User : " + f"[{name0}](tg://user?id={uid})",
        )


@register(outgoing=True, pattern=r"^\.unblock$")
async def unblockpm(unblock):
    """For .unblock command, let people PMing you again!"""
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client.get_entity(reply.sender_id)
        name0 = str(replied_user.first_name)
        await unblock.client(UnblockRequest(replied_user.id))
        await unblock.edit("`You have been unblocked.`")
        uid = replied_user.id
        if BOTLOG:
            await unblock.client.send_message(
                BOTLOG_CHATID,
                f"#UNBLOCKED\n" + "👤 User : " + f"[{name0}](tg://user?id={uid})",
            )
    elif unblock.is_group and not unblock.reply_to_msg_id:
        await unblock.edit("`Please reply to user you want to unblock`")
        return
    else:
        await unblock.edit("`User already unblocked`")


@register(outgoing=True, pattern=r"^\.(set|get|reset) pm_msg(?: |$)(\w*)")
async def add_pmsg(cust_msg):
    """Set your own Unapproved message"""
    if not PM_AUTO_BAN:
        return await cust_msg.edit("**Mohon Maaf, Anda Harus Menyetel** `PM_AUTO_BAN` **Ke** `True`\n Silahkan Lakukan set var.\nUsage : `.set var PM_AUTO_BAN True`")
    try:
        import userbot.modules.sql_helper.globals as sql
    except AttributeError:
        await cust_msg.edit("`Running on Non-SQL mode!`")
        return

    await cust_msg.edit("`Sedang Memproses...`")
    conf = cust_msg.pattern_match.group(1)

    custom_message = sql.gvarstatus("unapproved_msg")

    if conf.lower() == "set":
        message = await cust_msg.get_reply_message()
        status = "Pesan"

        # check and clear user unapproved message first
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            status = "Pesan"

        if message:
            msg = message.message  # get the plain text
            sql.addgvar("unapproved_msg", msg)
        else:
            return await cust_msg.edit("`Mohon Balas Ke Pesan`")

        await cust_msg.edit("#SETTINGS ☑️\n`Pesan Berhasil Disimpan Ke Room Chat.`")

        if BOTLOG:
            await cust_msg.client.send_message(
                BOTLOG_CHATID, f"**{status} PM Yang Tersimpan Dalam Room Chat Anda :** \n\n{msg}"
            )

    if conf.lower() == "reset":
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            await cust_msg.edit("#DELETE ☑️\n`Anda Telah Menghapus Pesan Custom PM Ke Default.`")
        else:

            await cust_msg.edit("`Pesan PM Anda Sudah Default Sejak Awal.`")

    if conf.lower() == "get":
        if custom_message is not None:
            await cust_msg.edit(
                f"**Ini Adalah Pesan PM Yang Sekarang Dikirimkan Ke Room Chat Anda :**\n\n{custom_message}"
            )
        else:
            await cust_msg.edit(
                "*Anda Belum Menyetel Pesan PM*\n"
                f"Masih Menggunakan Pesan PM Default : \n\n`{DEF_UNAPPROVED_MSG}`"
            )


CMD_HELP.update(
    {
        "pmpermit": "✘ Pʟᴜɢɪɴ : Private Message Permite"
        "\n\n⚡𝘾𝙈𝘿⚡: `.approve`"
        "\n↳ : Menerima Pesan Seseorang Dengan Cara Balas Pesannya Atau Tag dan Juga Untuk Dilakukan Di PM."
        "\n\n⚡𝘾𝙈𝘿⚡: `.disapprove`"
        "\n↳ : Menolak Pesan Seseorang Dengan Cara Balas Pesannya Atau Tag dan Juga Untuk Dilakukan Di PM."
        "\n\n⚡𝘾𝙈𝘿⚡: `.block`"
        "\n↳ : Memblokir Orang Di PM."
        "\n\n⚡𝘾𝙈𝘿⚡: `.unblock`"
        "\n↳ : Membuka Blokir."
        "\n\n⚡𝘾𝙈𝘿⚡: `.notifoff`"
        "\n↳ : Menonaktifkan Notifikasi Pesan Yang Belum Diterima."
        "\n\n⚡𝘾𝙈𝘿⚡: `.notifon`"
        "\n↳ : Mengaktifkan Notifikasi Pesan Yang Belum Diterima."
        "\n\n⚡𝘾𝙈𝘿⚡: `.set pm_msg` <Reply Message>"
        "\n↳ : Menyetel Pesan Pribadimu Untuk Orang Yang Pesannya Belum Diterima."
        "\n\n⚡𝘾𝙈𝘿⚡: `.get pm_msg`"
        "\n↳ : Mendapatkan Custom Pesan PM-Mu."
        "\n\n⚡𝘾𝙈𝘿⚡: `.reset pm_msg`"
        "\n↳ : Menghapus Pesan PM ke Default."
        "\n\nPesan Pribadi Yang Belum Diterima Saat Ini Tidak Dapat Disetel"
        "\nke Teks Format. Seperti : Bold, Underline, Link, dll."
        "\nPesan Akan Terkirim Secara Normal."})
