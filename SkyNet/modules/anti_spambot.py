# Copyright © 2021 Lynx-Userbot ( LLC Company )
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Based Plugin on @Catuserbot ( @sandy1709 )
# Ported by KENZO

""" A module for helping ban group join spammers. """

from requests import get
from telethon.errors import ChatAdminRequiredError
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins

from userbot.modules.sql_helper.globalban_sql import get_gbanuser, is_gbanned
from userbot.utils import edit_or_reply
from userbot.events import register

from userbot import (
    ANTISPAMBOT_BAN,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    bot,
    spamwatch,
    logging,
)


LOGS = logging.getLogger(__name__)


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


async def admin_groups(grp):
    admgroups = []
    async for dialog in grp.client.iter_dialogs():
        entity = dialog.entity
        if (
            isinstance(entity, ChannelParticipantsAdmins)
            and entity.megagroup
            and (entity.creator or entity.admin_rights)
        ):
            admgroups.append(entity.id)
    return admgroups


def mentionuser(name, userid):
    return f"[{name}](tg://user?id={userid})"


if ANTISPAMBOT_BAN:

    @bot.on(ChatAction())
    async def anti_spambot(event):  # sourcery no-metrics
        if not event.user_joined and not event.user_added:
            return
        user = await event.client.get_entity(event.chat_id)
        admin = await admin_groups(event)
        if not admin:
            return
        lynxbanned = None
        adder = None
        ignore = None
        if event.user_added:
            try:
                adder = event.action_message.sender_id
            except AttributeError:
                return
        async for admin in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsAdmins
        ):
            if admin.id == adder:
                ignore = True
                break
        if ignore:
            return
        if is_gbanned(user.id):
            lynxgban = get_gbanuser(user.id)
            if lynxgban.reason:
                hmm = await event.reply(
                    f"👤 [USER](tg://user?id={user.id}) was gbanned by you for the reason: `{lynxgban.reason}`"
                )
            else:
                hmm = await event.reply(
                    f"👤 [USER](tg://user?id={user.id}) was gbanned by you"
                )
            try:
                await event.client.edit_permissions(
                    event.chat_id, user.id, view_messages=False
                )
                lynxbanned = True
            except Exception as e:
                LOGS.info(e)
        if spamwatch and not lynxbanned:
            ban = spamwatch.get_ban(user.id)
            if ban:
                hmm = await event.reply(
                    f"👤 [USER](tg://user?id={user.id}) was banned by spamwatch for the reason: `{ban.reason}`"
                )
                try:
                    await event.client.edit_permissions(
                        event.chat_id, user.id, view_messages=False
                    )
                    lynxbanned = True
                except Exception as e:
                    LOGS.info(e)
        if not lynxbanned:
            try:
                casurl = "https://api.cas.chat/check?user_id={}".format(
                    user.id)
                data = get(casurl).json()
            except Exception as e:
                LOGS.info(e)
                data = None
            if data and data["ok"]:
                reason = (
                    f"[Banned by Combot Anti Spam](https://cas.chat/query?u={user.id})"
                )
                hmm = await event.reply(
                    f"👤 [USER](tg://user?id={user.id}) was banned by Combat anti-spam service(CAS) for the reason check: {reason}"
                )
                try:
                    await event.client.edit_permissions(
                        event.chat_id, user.id, view_messages=False
                    )
                    lynxbanned = True
                except Exception as e:
                    LOGS.info(e)
        if BOTLOG and lynxbanned:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#ANTISPAMBOT\n"
                f"**User :** [CLICK HERE](tg://user?id={user.id})\n"
                f"**Chat :** {event.chat.title} (`{event.chat_id}`)\n"
                f"**Reason :** {hmm.text}",
            )


@register(outgoing=True, groups_only=True, pattern=r"^\.cascheck$")
async def caschecker(event):
    "Searches For CAS (Combot Antispam Service) Banned Users in Group and Shows You The List."
    text = ""
    lynxevent = await edit_or_reply(
        event,
        "`Checking any CAS (Combot Antispam Service) Banned Users Here, This May Take Several Minutes too...`",
    )
    try:
        info = await event.client.get_entity(event.chat_id)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in event.client.iter_participants(info.id):
            if banchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"👤 [USER](tg://user?id={user.id}) - `{user.id}`\n"
                else:
                    banned_users += f"Deleted Account - `{user.id}`\n"
            members_count += 1
        text = "**⚠️ WARNING ⚠️**\n\nFound `{}` of `{}` Users are CAS Banned:\n".format(
            cas_count, members_count)
        text += banned_users
        if not cas_count:
            text = "No CAS Banned users found!"
    except ChatAdminRequiredError:
        await lynxevent.edit("`CAS Check Failed: Admin Privileges are Required`")
        return
    except BaseException:
        await lynxevent.edit("`CAS Check Failed.`")
        return
    await lynxevent.edit(text)


@register(outgoing=True, groups_only=True, pattern=r"^\.spamcheck$")
async def caschecker(event):
    "Searches for Spamwatch Federation Banned Users in Group and Shows You The List"
    text = ""
    lynxevent = await edit_or_reply(
        event,
        "`Checking any Spamwatch Banned Users Here, This May Take Several Minutes too......`",
    )
    try:
        info = await event.client.get_entity(event.chat_id)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return
    try:
        cas_count, members_count = (0,) * 2
        banned_users = ""
        async for user in event.client.iter_participants(info.id):
            if spamchecker(user.id):
                cas_count += 1
                if not user.deleted:
                    banned_users += f"👤 [USER](tg://user?id={user.id}) - `{user.id}`\n"
                else:
                    banned_users += f"Deleted Account - `{user.id}`\n"
            members_count += 1
        text = "**⚠️ WARNING ⚠️**\nFound `{}` of `{}` users are SpamWatch Banned:\n".format(
            cas_count, members_count)
        text += banned_users
        if not cas_count:
            text = "No spamwatch Banned users found!"
    except ChatAdminRequiredError:
        await lynxevent.edit("`SpamWatch Check Failed: Admin Privileges are Required.`")
        return
    except BaseException:
        await lynxevent.edit("`SpamWatch Check Failed.`")
        return
    await lynxevent.edit(text)


def banchecker(user_id):
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    return bool(data and data["ok"])


def spamchecker(user_id):
    ban = None
    if spamwatch:
        ban = spamwatch.get_ban(user_id)
    return bool(ban)


CMD_HELP.update(
    {
        "anti_spambot": "✘ Pʟᴜɢɪɴ : Anti Spammer(s)"
        "\n\n⚡𝘾𝙈𝘿⚡: `.caschecker`"
        "\n↳ : To check the users who are banned in cas."
        "\n\n**Note:** When you use this cmd it will check every user in the group where you used whether"
        "he is banned in cas (combat antispam service) and will show there names if they are flagged in cas"
        "\n\n⚡𝘾𝙈𝘿⚡: `.spamcheck`"
        "\n↳ : To check the users who are banned in spamwatch."
        "\n\n**Note:** When you use this command it will check every user in the group where you used whether"
        "he is banned in spamwatch federation and will show there names if they are banned in spamwatch federation"
    }
)
