# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot Module For Getting Information About The Server. """


import asyncio
from git import Repo
from telethon.errors.rpcerrorlist import MediaEmptyError
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove
from telethon import __version__, version
import platform
import sys
from datetime import datetime
import psutil
from userbot.events import register
from userbot import (
    ALIVE_LOGO,
    ALIVE_NAME,
    BOT_VER,
    CMD_HELP,
    DEFAULTUSER,
    UPSTREAM_REPO_BRANCH,
    INSTAGRAM_ALIVE,
    bot
)


# ================= CONSTANT =================
repo = Repo()
# ============================================


modules = CMD_HELP


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

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


@register(outgoing=True, pattern=r"^\.spc")
async def psu(event):
    uname = platform.uname()
    softw = "💻 **Informasi Sistem**\n"
    softw += f"`Sistem   : {uname.system}`\n"
    softw += f"`Rilis    : {uname.release}`\n"
    softw += f"`Versi    : {uname.version}`\n"
    softw += f"`Mesin    : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Waktu Hidup: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "📉 **Informasi CPU**\n"
    cpuu += "`Physical cores   : " + \
        str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + \
        str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "📉 **CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`Semua Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "📊 **Memori Digunakan**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "📁 **Bandwith Digunakan**\n"
    bw += f"`Unggah  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "⚙️ **Informasi Mesin**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@register(outgoing=True, pattern=r"^\.botver$")
async def bot_ver(event):
    """For .botver command, get the bot version."""
    if not event.text[0].isalpha() and event.text[0] not in (
            "/", "#", "@", "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await event.edit(
                "`SkyNet Version: " f"{verout}" "` \n" "`Revision: " f"{revout}" "`"
            )
        else:
            await event.edit(
                "Shame that you don't have git, you're running - 'v1.beta.4' anyway!"
            )


@register(outgoing=True, pattern=r"^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    if pip.text[0].isalpha() or pip.text[0] in ("/", "#", "@", "!"):
        return
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("`Mencari...`")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output Terlalu Besar, Dikirim Sebagai File`")
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )
    else:
        await pip.edit("Gunakan `.help pip` Untuk Melihat Contoh")


@register(outgoing=True, pattern=r"^\.(?:sky|xon)\s?(.)?")
async def ireallyalive(event):
    """For .sky command, check if the bot is running."""
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    logo = ALIVE_LOGO
    output = (
        f"`Robot` **is running on** `{repo.active_branch.name}`\n"
        "`====================================`\n"
        f"💻 `OS          :` Debian GNU/{uname.system} 10 {uname.machine}\n"
        f"💻 `Kernel      :` {uname.release}\n"
        f"💻 `CPU         :` Intel Xeon E5-2670 @ {cpufreq.current:.2f}Ghz\n"
        f"🐍 `Python      :` v. {python_version()}\n"
        f"⚙️ `Telethon    :` v. {version.__version__}\n"
        f"👨‍💻 `User        :` {DEFAULTUSER}\n"
        "`====================================`\n"
        f" Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\n License : GNU AFFERO GENERAL PUBLIC LICENSE v3.0")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await bot.send_file(event.chat_id, logo, caption=output)
            await event.delete()
        except MediaEmptyError:
            await event.edit(
                output + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
    else:
        await alive.edit(output)


@register(outgoing=True, pattern=r"^\.(?:alive|on)\s?(.)?")
async def amireallyalive(alive):
    await bot.get_me()
    uptime = await get_readable_time((time.time() - StartTime))
    logo = ALIVE_LOGO
    output = (
        f"**ㅤㅤ  ╭─━━═━═━═━═━━─╮**\n"
        f"**       ⊏┊[𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭](t.me/CyberSupportGroup) ⊨〛💨 **\n"
        f"**ㅤㅤ  ╰─━━═━═━═━═━━─╯**\n"
        f"╭╼════════════════════╾╮\n"
        f"│    ⇱  𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 𝐌𝐲 𝐏𝐫𝐨𝐟𝐢𝐥𝐞 ⇲ \n"
        f"┟╼════════════════════╾┤\n"
        f"╟◈ 👤  `User     :` {DEFAULTUSER}\n"
        f"╟◈ ⚙️  `Telethon :` v. {version.__version__}\n"
        f"╟◈ 🐍  `Python   :` v. {python_version()}\n"
        f"╟◈ 👾  `Bot Ver  :` v. {BOT_VER}\n"
        f"╟◈ 🛠️  `Branch   :` {UPSTREAM_REPO_BRANCH}\n"
        f"╟◈ 💻  `System   :` Ubuntu 20.10\n"
        f"╟◈ 📂  `Plugins  :` {len(modules)}\n"
        f"┞╼════════════════════╾┤\n"
        f"├◈ **Don't forget to support our**\n"
        f"│    **userbot, how to press below.**\n"
        f"╰╼════════════════════╾╯\n"
        f"| [𝗥𝗲𝗽𝗼](https://aryazakaria01.github.io/SkyNet-Userbot) | [𝗦𝗸𝘆𝗡𝗲𝘁-𝗧𝗲𝗮𝗺](t.me/CyberSupportGroup) | "
        f"[𝗠𝘆 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺]({INSTAGRAM_ALIVE}) | ")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await bot.send_file(alive.chat_id, logo, caption=output)
            await alive.delete()
        except MediaEmptyError:
            await alive.edit(
                output + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
    else:
        await alive.edit(output)


@register(outgoing=True, pattern=r"^\.dealiveu")
async def amireallyaliveuser(username):
    """For .dealiveu command, change the username in the .alive command."""
    message = username.text
    output = ".dealiveu [new user without brackets] nor can it be empty"
    if not (message == ".dealiveu" or message[7:8] != " "):
        username = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = username
        return DEFAULTUSER * DEFAULTUSER
        output = "Successfully changed user to " + username + "!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    """For .resetalive command, reset the username in the .alive command."""
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update({
    "system": "✘ Pʟᴜɢɪɴ : System Stats"
    "\n\n⚡𝘾𝙈𝘿⚡: `.sysd`"
    "\n↳ : Shows system information using neofetch."
    "\n\n⚡𝘾𝙈𝘿⚡: `.db`"
    "\n↳ : Shows database related info."
    "\n\n⚡𝘾𝙈𝘿⚡: `.spc`"
    "\n↳ : Show system specification.",
    "alive": "✘ Pʟᴜɢɪɴ : Alive"
    "\n\n⚡𝘾𝙈𝘿⚡: `.sky` or `.xon` | `.alive` or `.on`"
    "\n↳ : To see whether your bot is working or not."
    "\n\n⚡𝘾𝙈𝘿⚡: `.dealiveu` <New Username>"
    "\n↳ : Changes the 'user' in alive to the text you want."
    "\n\n⚡𝘾𝙈𝘿⚡: `.restalive`"
    "\n↳ : Resets the User to Default.",
    "botversion": "✘ Pʟᴜɢɪɴ : Robot Version"
    "\n\n⚡𝘾𝙈𝘿⚡: `.botver`"
    "\n↳ : Shows the userbot version."
    "\n\n⚡𝘾𝙈𝘿⚡: `.pip` <module(s)>"
    "\n↳ : Does a search of pip modules(s)."
})
