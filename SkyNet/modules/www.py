# Copyright (C) 2021 GNU AFFERO GENERAL PUBLIC LICENSE.
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
#
# SkyNet Userbot
"""Userbot module containing commands related to the
   Information Superhighway (yes, Internet)."""

import asyncio
import time

from datetime import datetime
from telethon import functions

from speedtest import Speedtest
from SkyNet import CMD_HELP, StartTime, DEFAULTUSER
from SkyNet.events import register
from SkyNet.utils import humanbytes


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern=r"^\.sping$")
async def sping(pong):
    """For .ping command, ping the userbot from any chat."""
    await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("__Connecting to server.__")
    await pong.edit("__Connecting to server..__")
    await pong.edit("__Connecting to server...__")
    await pong.edit("__Connecting to server.__")
    await pong.edit("__Connecting to server..__")
    await pong.edit("__Connecting to server...__")
    await pong.edit("__Connecting to server.__")
    await pong.edit("__Connecting to server..__")
    await pong.edit("__Connecting to server...__")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**╭━━━━━━━━━━━━━━━━━╮** \n"
                    f"**          - 𝐍 𝐄 𝐓 𝐖 𝐎 𝐑 𝐊 -** \n"
                    f"**   ▰▱▰▱▰▱▰▱▰▱▰▱** \n"
                    f"**        • ꜱɪɢɴᴀʟ  :** `%sms` \n"
                    f"**        • ᴏᴡɴᴇʀ   :** `{DEFAULTUSER}` \n"
                    f"**╰━━━━━━━━━━━━━━━━━╯** \n" % (duration))


@register(outgoing=True, pattern=r"^\.lping$")
async def lping(pong):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("`Connecting to server...`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"█▀█ █▀█ █▄░█ █▀▀ █ \n"
                    f"█▀▀ █▄█ █░▀█ █▄█ ▄ \n\n"
                    f"Signal: "
                    f"`%sms` \n"
                    f"Uptime: "
                    f"`{uptime}` \n"
                    f"**`{DEFAULTUSER}`**" % (duration))


@register(outgoing=True, pattern=r"^\.xping$")
async def xping(pong):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭**\n"
                    f"➾ __Signal__    __:__  "
                    f"`%sms` \n"
                    f"➾ __Uptime__ __:__  "
                    f"`{uptime}` \n" % (duration))


@register(outgoing=True, pattern=r"^\.ping$")
async def ping(pong):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("__Connecting to data center.__")
    await pong.edit("__Connecting to data center..__")
    await pong.edit("__Connecting to data center...__")
    await pong.edit("⚡")
    await asyncio.sleep(2)
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit(f"**╭─━━━━━━━━━━━━━━━─╮** \n"
                    f"**       𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭** \n"
                    f"**╭─━━━━━━━━━━━━━━━─╯** \n"
                    f"**│⊙  Sɪɢɴᴀʟ   :** "
                    f"`%sms` \n"
                    f"**│⊙  Uᴘᴛɪᴍᴇ  :** "
                    f"`{uptime}` \n"
                    f"**│⊙  Oᴡɴᴇʀ   :** `{DEFAULTUSER}` \n"
                    f"**╰━━━━━━━━━━━━━━━━━╯**" % (duration))


# Port WeebProject
@register(outgoing=True, pattern=r"^\.speedtest$")
async def speedtst(spd):
    """For .speed command, use SpeedTest to check server speeds."""
    await spd.edit("`Running speed test...`")

    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    msg = (
        f"**Started at {result['timestamp']}**\n\n"
        "**Client**\n"
        f"**ISP :** `{result['client']['isp']}`\n"
        f"**Country :** `{result['client']['country']}`\n\n"
        "**Server**\n"
        f"**Name :** `{result['server']['name']}`\n"
        f"**Country :** `{result['server']['country']}`\n"
        f"**Sponsor :** `{result['server']['sponsor']}`\n\n"
        f"**Ping :** `{result['ping']}`\n"
        f"**Upload :** `{humanbytes(result['upload'])}/s`\n"
        f"**Download :** `{humanbytes(result['download'])}/s`"
    )

    await spd.delete()
    await spd.client.send_file(
        spd.chat_id,
        result["share"],
        caption=msg,
        force_document=False,
    )


@register(outgoing=True, pattern=r"^\.dc$")
async def neardc(event):
    """For .dc command, get the nearest datacenter information."""
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(
        f"Country : `{result.country}`\n"
        f"Nearest Datacenter : `{result.nearest_dc}`\n"
        f"This Datacenter : `{result.this_dc}`"
    )


@register(outgoing=True, pattern=r"^\.pong$")
async def pingme(pong):
    """For .ping command, ping the userbot from any chat."""
    start = datetime.now()
    await pong.edit("⚡")
    await asyncio.sleep(1)
    await pong.edit("😼")
    end = datetime.now()
    duration = (end - start).microseconds / 9000
    await pong.edit(f"**🙅 Oᴡɴᴇʀ : {DEFAULTUSER}**\n`%sms`" % (duration))


CMD_HELP.update({
    "speedtest": "✘ Pʟᴜɢɪɴ : `Speed Test`\
         \n\n⚡𝘾𝙈𝘿⚡: `.ping` | `.lping` | `.xping` | `.sping`\
         \n↳ : Untuk Menunjukkan Ping Bot Anda.\
         \n\n⚡𝘾𝙈𝘿⚡: `.pong`\
         \n↳ : Sama Seperti Perintah Ping.\
         \n\n⚡𝘾𝙈𝘿⚡: `.speedtest`\
         \n↳ : Untuk Menunjukkan Kecepatan Jaringan Anda.\
         \n\n⚡𝘾𝙈𝘿⚡: `.dc`\
         \n↳ : Menemukan Server Dari Datacenter Kamu."})
