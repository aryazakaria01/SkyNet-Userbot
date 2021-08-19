# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module containing commands for keeping notes."""

from userbot import BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from asyncio import sleep


@register(outgoing=True, pattern=r"\.notes$")
async def notes_active(event):
    """For .notes command, list all of the notes saved in a chat."""
    try:
        from userbot.modules.sql_helper.notes_sql import get_notes
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    message = "`There are no saved notes in this chat`"
    notes = get_notes(event.chat_id)
    for note in notes:
        if message == "`There are no saved notes in this chat`":
            message = "Notes saved in this chat:\n"
        message += "`#{}`\n".format(note.keyword)
    await event.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(event):
    """For .clear command, clear note with the given name."""
    try:
        from userbot.modules.sql_helper.notes_sql import rm_note
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    notename = event.pattern_match.group(1)
    if rm_note(event.chat_id, notename) is False:
        return await event.edit("`Couldn't find note:` **{}**".format(notename))
    else:
        return await event.edit(
            "`Successfully deleted note:` **{}**".format(notename))


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_note(event):
    """For .save command, saves notes in a chat."""
    try:
        from userbot.modules.sql_helper.notes_sql import add_note
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#NOTE\
            \nCHAT ID: {event.chat_id}\
            \nKEYWORD: {keyword}\
            \n\nThe following message is saved as the note's reply data for the chat, please do NOT delete it !!"
            )
            msg_o = await event.client.forward_messages(entity=BOTLOG_CHATID,
                                                        messages=msg,
                                                        from_peer=event.chat_id,
                                                        silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Saving media as data for the note requires the BOTLOG_CHATID to be set.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Note {} successfully. Use` #{} `to get it`"
    if add_note(str(event.chat_id), keyword, string, msg_id) is False:
        return await event.edit(success.format('updated', keyword))
    else:
        return await event.edit(success.format('added', keyword))


@register(pattern=r"#\w*",
          disable_edited=True,
          disable_errors=True,
          ignore_unsafe=True)
async def incom_note(event):
    """Notes logic."""
    try:
        if not (await event.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.notes_sql import get_note
            except AttributeError:
                return
            notename = event.text[1:]
            note = get_note(event.chat_id, notename)
            message_id_to_reply = event.message.reply_to_msg_id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note:
                if note.f_mesg_id:
                    msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                            ids=int(
                                                                note.f_mesg_id))
                    await event.client.send_message(event.chat_id,
                                                    msg_o.mesage,
                                                    reply_to=message_id_to_reply,
                                                    file=msg_o.media)
                elif note.reply:
                    await event.client.send_message(event.chat_id,
                                                    note.reply,
                                                    reply_to=message_id_to_reply)
    except AttributeError:
        pass


@register(outgoing=True, pattern=r"\.rmbotnotes (.*)")
async def kick_marie_notes(event):
    """For .rmbotnotes command, allows you to kick all Marie(or her clones) notes from a chat."""
    bot_type = event.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        await event.edit("`That bot is not yet supported!`")
        return
    await event.edit("```Will be kicking away all Notes!```")
    await sleep(3)
    resp = await event.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type == "marie":
            await event.reply("/clear %s" % (i.strip()))
        if bot_type == "rose":
            i = i.replace('`', '')
            await event.reply("/clear %s" % (i.strip()))
        await sleep(0.3)
    await event.respond(
        "```Successfully purged bots notes yaay!```\n Gimme cookies!")
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID, "I cleaned all Notes at " + str(event.chat_id))


CMD_HELP.update({
    "notes": "✘ Pʟᴜɢɪɴ : Notes"
    "\n\n#<notename>"
    "\n**Usage :** Gets the Specified Note."
    "\n\n⚡𝘾𝙈𝘿⚡: `.save` <Notename> <Notedata> or reply to a message with .save <Notename>"
    "\n↳ : Saves the replied message as a note with the notename. (Works with pics, docs, and stickers too!)"
    "\n\n⚡𝘾𝙈𝘿⚡: `.notes`"
    "\n↳ : Gets all saved notes in a chat."
    "\n\n⚡𝘾𝙈𝘿⚡: `.clear` <Notename>"
    "\n↳ : Deletes the specified note."
    "\n\n⚡𝘾𝙈𝘿⚡: `.rmbotnotes` <marie/rose>"
    "\n↳ : Removes All Notes of Admin Bots (Currently Supported: Marie, Rose and their clones.) in the chat."
})
