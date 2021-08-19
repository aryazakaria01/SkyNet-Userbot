# Copyright (C) 2020 Frizzy.
# All rights reserved.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.ttvid(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if "vm." and ".com" not in d_link:
        await event.edit("`Mohon Maaf, Link Tidak Support. Silahkan Cari Link Lain.`\n**Contoh:** `vm.tiktok.com`")
    else:
        await event.edit("```Video Sedang Diproses...```")
    chat = "@ttsavebot"
    async with bot.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit(f"#Kesalahan ❌\n`Mohon Buka Blokir` @ttsavebot `Lalu Tekan /start Dan Coba Lagi !`")
            return
        await bot.send_file(event.chat_id, video, video_note=True)
        await event.client.delete_messages(conv.chat_id,
                                           [msg_start.id, r.id, msg.id, details.id, video.id])
        await event.delete()


CMD_HELP.update(
    {
        "tiktok": "✘ Pʟᴜɢɪɴ : Tiktok"
        "\n\n⚡𝘾𝙈𝘿⚡: `.ttvid <Link>`"
        "\n↳ : Download Video Tiktok Tanpa Watermark."
        "\n\nSources `@ttsavebot`"
    }
)
