# Copyright (C) 2019 GNU AFFERO GENERAL PUBLIC LICENSE LLC.
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# Credits Logs @BianSepang , @KenHV
# Ported @Badboyanim
"""Userbot initialization."""


import signal
import os
import time
import re
import io
import random
import spamwatch as spam_watch

from datetime import datetime
from time import sleep
import platform
import psutil
from platform import python_version, uname
from telethon import TelegramClient, version
from sys import version_info
import sys
import asyncio
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from math import ceil

from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
from telethon.sync import custom, events
from telethon.sessions import StringSession
from telethon import Button, functions, types
from telethon.utils import get_display_name
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged

load_dotenv("config.env")

StartTime = time.time()

CMD_LIST = {}
# for later purposes
CMD_HELP = {}
INT_PLUG = ""
LOAD_PLUG = {}

# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info("You MUST have a python version of at least 3.8."
              "Multiple features depend on this. Bot quitting.")
    quit(1)

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    quit(1)

# Telegram App KEY and HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID") or 0)

# Userbot logging feature switch.
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# Custom Module
CUSTOM_PMPERMIT_TEXT = os.environ.get("CUSTOM_PMPERMIT_TEXT", None)

# Pm Permit Img
PM_PERMIT_PIC = os.environ.get(
    "PM_PERMIT_PIC",
    None) or "https://telegra.ph/file/49ce66ba7e0fa0ce99210.png"

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Heroku Credentials for updater.
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)

# JustWatch Country
WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY", "ID")

# Github Credentials for updater and Gitupload.
GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)

# Custom (forked) repo URL for updater.
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/aryazakaria01/SkyNet-Userbot")
UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH", "SkyNet-Userbot")

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL", None)

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# DEVELOPER and SUDO_USERS
DEVELOPER = 1345333945, 1448477501, 1682708454, 1276135372, 1415971020
SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}

# Chrome Driver and Headless Google Chrome Binaries
CHROME_DRIVER = os.environ.get("CHROME_DRIVER") or "/usr/bin/chromedriver"
GOOGLE_CHROME_BIN = os.environ.get(
    "GOOGLE_CHROME_BIN") or "/usr/bin/google-chrome"

# set to True if you want to log PMs to your PM_LOGGR_BOT_API_ID
NC_LOG_P_M_S = bool(os.environ.get("NC_LOG_P_M_S", False))
# send .get_id in any channel to forward all your NEW PMs to this group
PM_LOGGER_GROUP_ID = int(
    os.environ.get("PM_LOGGER_GROUP_ID")
    or os.environ.get("PM_LOGGR_BOT_API_ID")
    or 0
)

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Lydia API
LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)

# set blacklist_chats where you do not want userbot's features
UB_BLACK_LIST_CHAT = os.environ.get("UB_BLACK_LIST_CHAT", None)

# Anti Spambot Config
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Antispambot BAN
ANTISPAMBOT_BAN = os.environ.get("ANTISPAMBOT_BAN", False)

# Dapatkan Spamwatch API ke @SpamWatchBot di Telegram
SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)

if SPAMWATCH_API:
    ur_token = SPAMWATCH_API
    spamwatch = spam_watch.Client(ur_token)
else:
    spamwatch = None

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

# Default .alive Name
ALIVE_NAME = os.environ.get("ALIVE_NAME", None)

# Time & Date - Country and Time Zone
COUNTRY = str(os.environ.get("COUNTRY", "ID"))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Clean Welcome
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Zipfile Module
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY", "./zips")

# Bot Name
TERM_ALIAS = os.environ.get("TERM_ALIAS", None)

# Bot Version
BOT_VER = os.environ.get("BOT_VER", "0.3.1")

# Default .alive Username
ALIVE_USERNAME = os.environ.get("ALIVE_USERNAME", None)

# Sticker Custom Pack Name
S_PACK_NAME = os.environ.get("S_PACK_NAME", None)

# Default .alive Logo
ALIVE_LOGO = os.environ.get(
    "ALIVE_LOGO",
    None) or "https://telegra.ph/file/c627554ec78061b7e4f6b.jpg"

# Link Instagram for CMD Alive
INSTAGRAM_ALIVE = os.environ.get(
    "INSTAGRAM_ALIVE") or "instagram.com/geezingsupport"

# Inline Picture
INLINE_PICTURE = os.environ.get(
    "INLINE_PICTURE") or "resource/logo/SkyNetUserbot-Button.jpg"

L_PIC = str(INLINE_PICTURE)
if L_PIC:
    lynxlogo = L_PIC
else:
    lynxlogo = "resource/logo/SkyNetUserbot-Button.jpg"

INLINE_LOGO = os.environ.get(
    "INLINE_LOGO") or "https://telegra.ph/file/c627554ec78061b7e4f6b.jpg"

IN_PIC = str(INLINE_LOGO)
if IN_PIC:
    aliplogo = IN_PIC
else:
    aliplogo = "https://telegra.ph/file/c627554ec78061b7e4f6b.jpg"

# Last.fm Module
BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)

lastfm = None
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    try:
        lastfm = LastFMNetwork(
            api_key=LASTFM_API,
            api_secret=LASTFM_SECRET,
            username=LASTFM_USERNAME,
            password_hash=LASTFM_PASS)
    except Exception as lastfm:  # pylint: disable=C0321
        pass

# Google Drive Module
G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA", None)
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID", None)
G_DRIVE_INDEX_URL = os.environ.get("G_DRIVE_INDEX_URL", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
    "TMP_DOWNLOAD_DIRECTORY", "./downloads")

# Google Photos
G_PHOTOS_CLIENT_ID = os.environ.get("G_PHOTOS_CLIENT_ID", None)
G_PHOTOS_CLIENT_SECRET = os.environ.get("G_PHOTOS_CLIENT_SECRET", None)
G_PHOTOS_AUTH_TOKEN_ID = os.environ.get("G_PHOTOS_AUTH_TOKEN_ID", None)
if G_PHOTOS_AUTH_TOKEN_ID:
    G_PHOTOS_AUTH_TOKEN_ID = int(G_PHOTOS_AUTH_TOKEN_ID)

# Genius Lyrics  API
GENIUS = os.environ.get("GENIUS_ACCESS_TOKEN", None)

# IMG Stuff
IMG_LIMIT = os.environ.get("IMG_LIMIT", None)

CMD_HELP = {}

# Quotes API Token
QUOTES_API_TOKEN = os.environ.get("QUOTES_API_TOKEN", None)

# Wolfram Alpha API
WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)

# Deezloader
DEEZER_ARL_TOKEN = os.environ.get("DEEZER_ARL_TOKEN", None)

# Photo Chat - Get this value from http://antiddos.systems
API_TOKEN = os.environ.get("API_TOKEN", None)
API_URL = os.environ.get("API_URL", "http://antiddos.systems")

# Inline bot helper
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Uptobox
USR_TOKEN = os.environ.get("USR_TOKEN_UPTOBOX", None)

# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.
if not os.path.exists("bin"):
    os.mkdir("bin")

binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown": "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py": "bin/cmrudl",
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)


# Logs
from .core.logger import logging
LOGS = logging.getLogger("userbot")

# PM_LOG
from userbot.modules.sql_helper.globals import gvarstatus
if PM_LOGGER_GROUP_ID == 0:
    if gvarstatus("PM_LOGGER_GROUP_ID") is None:
        PM_LOGGER_GROUP_ID = -100
    else:
        PM_LOGGER_GROUP_ID = int(gvarstatus("PM_LOGGER_GROUP_ID"))
elif str(PM_LOGGER_GROUP_ID)[0] != "-":
    PM_LOGGER_GROUP_ID = int("-" + str(PM_LOGGER_GROUP_ID))


# Signal


def shutdown_bot(signum, frame):
    LOGS.info("Received SIGTERM.")
    bot.disconnect()
    sys.exit(143)


signal.signal(signal.SIGTERM, shutdown_bot)


def migration_workaround():
    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar, gvarstatus
    except AttributeError:
        return None

    old_ip = gvarstatus("public_ip")
    new_ip = get("https://api.ipify.org").text

    if old_ip is None:
        delgvar("public_ip")
        addgvar("public_ip", new_ip)
        return None

    if old_ip == new_ip:
        return None

    sleep_time = 180
    LOGS.info(
        f"A change in IP address is detected, waiting for {sleep_time / 60} minutes before starting the bot."
    )
    sleep(sleep_time)
    LOGS.info("Starting bot...")

    delgvar("public_ip")
    addgvar("public_ip", new_ip)
    return None


# 'bot' variable
if STRING_SESSION:
    # pylint: disable=invalid-name
    session = StringSession(str(STRING_SESSION))
else:
    # pylint: disable=invalid-name
    session = "userbot"
try:
    # pylint: disable=invalid-name
    bot = TelegramClient(
        session=session,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"STRING_SESSION - {str(e)}")
    sys.exit()


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the private error log storage to work."
        )
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the userbot logging feature to work."
        )
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly.")
        quit(1)

with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID environment variable isn't a "
            "valid entity. Check your environment variables/config.env file.")
        quit(1)


from git import Repo


async def update_restart_msg(chat_id, msg_id):
    DEFAULTUSER = ALIVE_NAME or "Set `ALIVE_NAME` ConfigVar!"
    repo = Repo()
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    message = (
        f"**╭─━━━━━━━━━━━━━━━━━━━━━─╮**\n"
        f"**│ㅤㅤㅤ[𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭](t.me/Badboyanim)**\n"
        f"**│ ㅤis Back up and Running... 🐈**\n"
        f"**╭─━━━━━━━━━━━━━━━━━━━━━─╯**\n"
        f"**│** `OS       :` __Debian GNU/{uname.system} 10 {uname.machine}__\n"
        f"**│** `Kernel   :` __{uname.release}__\n"
        f"**│** `CPU      :` __Intel Xeon E5-2670 @ {cpufreq.current:.2f}Ghz__\n"
        f"**│** `Branch   :` __{repo.active_branch.name}__\n"
        f"**│** `Telethon :` __{version.__version__}__\n"
        f"**│** `Python   :` __{python_version()}__\n"
        f"**│** `User     :` __{DEFAULTUSER}__\n"
        f"**╰━━━━━━━━━━━━━━━━━━━━━━─╯**\n"
        f" Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\n License : GNU AFFERO GENERAL PUBLIC LICENSE v3.0")
    await bot.edit_message(chat_id, msg_id, message)
    return True

try:
    from userbot.modules.sql_helper.globals import delgvar, gvarstatus

    chat_id, msg_id = gvarstatus("restartstatus").split("\n")
    try:
        with bot:
            bot.loop.run_until_complete(
                update_restart_msg(
                    int(chat_id), int(msg_id)))
    except BaseException:
        pass
    delgvar("restartstatus")
except AttributeError:
    pass

# ------------------------------ Global Variables --------------------------------- #

COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
ENABLE_KILLME = True
LASTMSG = {}
lynx = bot
CMD_HELP = {}
ISAFK = False
AFKREASON = None
ZALG_LIST = {}
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node

# -------------------------------- InlineBot ------------------------------------- #


def alive_inline():
    repo = Repo()
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    text = f"`Robot` **is running on** `{repo.active_branch.name}`\
            \n`====================================`\
            \n💻 `OS          :` Debian GNU/{uname.system} 10 {uname.machine}\
            \n💻 `Kernel      :` {uname.release}\
            \n💻 `CPU         :` Intel Xeon E5-2670 @ {cpufreq.current:.2f}Ghz\
            \n🐍 `Python      :` v. {python_version()}\
            \n⚙️ `Telethon    :` v. {version.__version__}\
            \n👨‍💻 `User        :` {DEFAULTUSER}\
            \n`====================================`\
            \n Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\n License: GNU AFFERO GENERAL PUBLIC LICENSE v3.0"
    buttons = [
        (custom.Button.url(
            "𝗢𝘄𝗻𝗲𝗿",
            "https://t.me/Badboyanim",
        ),
            custom.Button.url(
            "𝗥𝗣𝗟 𝘃𝟭.𝗱🎖️",
            "https://github.com/aryazakaria01/SkyNet-Userbot/blob/SkyNet-Userbot/LICENSE",
        ),
        ),
        (custom.Button.inline(
            "Back to Settings",
            data="settings",
        ),
        ),
    ]
    return text, buttons


def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 3
    number_of_cols = 2
    global unpage
    unpage = page_number
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        custom.Button.inline("{} {} 」".format("「", x),
                             data="ub_modul_{}".format(x))
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols],
                     modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⋖╯Pʀᴇᴠ", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "ʙᴀᴄᴋ", data="{}_back({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "Nᴇxᴛ╰⋗", data="{}_next({})".format(prefix, modulo_page)
                )
            )
        ]
    return pairs

# -----------------------------------------Reg--------------------------------------- >


with lynx:
    try:
        lynx.tgbot = tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH,
            connection=ConnectionTcpAbridged,
            auto_reconnect=True,
            connection_retries=None).start(
            bot_token=BOT_TOKEN)

# -------------------------Flex------------------------------- >

        dugmeler = CMD_HELP
        me = bot.get_me()
        uid = me.id

        repo = Repo()
        uname = platform.uname()
        cpufreq = psutil.cpu_freq()

# ------------Replc--------------- >

        plugins = CMD_HELP

# --------------------------------- InlinePic -------------------------------------- #

        L_PIC = str(INLINE_PICTURE)
        if L_PIC:
            lynxlogo = L_PIC
        else:
            lynxlogo = "resource/logo/SkyNetUserbot-Button.jpg"

        IN_PIC = str(INLINE_LOGO)
        if IN_PIC:
            aliplogo = IN_PIC
        else:
            aliplogo = "https://telegra.ph/file/c627554ec78061b7e4f6b.jpg"

        AL_PIC = str(ALIVE_LOGO)
        if AL_PIC:
            alivvlogo = AL_PIC
        else:
            alivvlogo = ALIVE_LOGO

# ======================================== Inline Handler ======================================== #

        @lynx.tgbot.on(events.NewMessage(pattern=r"/start"))
        async def handler(event):
            if event.message.from_id != uid:
                u = await event.client.get_entity(event.chat_id)
                await event.reply(
                    f"Hai 👋 [{get_display_name(u)}](tg://user?id={u.id}) Selamat Datang di 𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭\nJika Kalian Datang Kesini dan Ingin Mengetahui SkyNet Lebih Lanjut,\nSilahkan Pilih **Menu Bantuan** Dibawah Ini.\n",
                    buttons=[
                        [
                            Button.url("📢 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 📢",
                                       "t.me/CyberMusicProject"),
                            Button.url("🚨 𝗠𝗲𝗻𝘂-𝗕𝗮𝗻𝘁𝘂𝗮𝗻 🚨",
                                       "https://telegra.ph/Bantuan-06-11")],
                        [Button.url("👤 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 👤",
                                    "t.me/Badboyanim")],
                    ]
                )

        @lynx.tgbot.on(events.NewMessage(pattern=r"/deploy"))
        async def handler(event):
            if event.message.from_id != uid:
                await event.reply(
                    f"𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭 Deploy to Heroku, Click Here 👇🏻",
                    buttons=[
                        [Button.url("⚒️ 𝗗𝗘𝗣𝗟𝗢𝗬 ⚒️", "https://github.com/aryazakaria01/SkyNet-Userbot")],
                        [Button.url("👥 𝗚𝗥𝗢𝗨𝗣 👥", "t.me/CyberSupportGroup")],
                    ],
                )

        @lynx.tgbot.on(events.NewMessage(pattern=r"/repo"))
        async def handler(event):
            if event.message.from_id != uid:
                u = await event.client.get_entity(event.chat_id)
                await event.message.get_sender()
                text = (
                    f"Haii 😼 [{get_display_name(u)}](tg://user?id={u.id}) My Name is 𝐒𝐤𝐲𝐍𝐞𝐭 🐈\n"
                    f"SkyNet Used For Fun On Telegram✨,\n"
                    f"and For Maintaining Your Group 🛠️.\n"
                    f"I was **Created by :** @Badboyanim For Various Userbots on Github.\n")
                await lynx.tgbot.send_file(event.chat_id, file=lynxlogo,
                                           caption=text,
                                           buttons=[
                                               [
                                                   custom.Button.url(
                                                       text="🇮🇩 𝗥𝗲𝗽𝗼𝘀𝗶𝘁𝗼𝗿𝘆 🇮🇩",
                                                       url="https://github.com/aryazakaria01"
                                                   )
                                               ]
                                           ]
                                           )

        @lynx.tgbot.on(events.NewMessage(pattern=r"/alive"))
        async def handler(event):
            if event.message.from_id != uid:
                axel = await event.client.get_entity(event.chat_id)
                await event.message.get_sender()
                text = (
                    f"`Robot` **is running on** `{repo.active_branch.name}`\n"
                    "`====================================`\n"
                    f"💻 `OS          :` Debian GNU/{uname.system} 10 {uname.machine}\n"
                    f"💻 `Kernel      :` {uname.release}\n"
                    f"💻 `CPU         :` Intel Xeon E5-2670 @ {cpufreq.current:.2f}Ghz\n"
                    f"🐍 `Python      :` v. {python_version()}\n"
                    f"⚙️ `Telethon    :` v. {version.__version__}\n"
                    f"👨‍💻 `User        :` [{get_display_name(axel)}](tg://user?id={axel.id})\n"
                    "`====================================`\n"
                    f" Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\n License: GNU AFFERO GENERAL PUBLIC LICENSE v3.0")
                await lynx.tgbot.send_file(event.chat_id, file=alivvlogo,
                                           caption=text,
                                           buttons=[
                                               [
                                                   Button.url("𝗢𝘄𝗻𝗲𝗿",
                                                              "https://t.me/Badboyanim"),
                                                   Button.url("𝗥𝗣𝗟 𝘃𝟭.𝗱🎖️",
                                                              "https://github.com/aryazakaria01/SkyNet-Userbot/blob/main/LICENSE")],
                                           ]
                                           )

        @lynx.tgbot.on(events.ChatAction)
        async def handler(event):
            if event.user_joined or event.user_added:
                u = await event.client.get_entity(event.chat_id)
                c = await event.client.get_entity(event.user_id)
                await event.reply(f" Welcome to [{get_display_name(u)}](tg://user?id={u.id})\n\n👤**User :** [{get_display_name(c)}](tg://user?id={c.id}) \n💳**ID :** `{c.id}`")

        @lynx.tgbot.on(events.NewMessage(pattern=r"/ping"))
        async def handler(event):
            if event.message.from_id != uid:
                start = datetime.now()
                end = datetime.now()
                ms = (end - start).microseconds / 1000
                await lynx.tgbot.send_message(
                    event.chat_id,
                    f"**PONG !!**\n `{ms}ms`",
                )

        @lynx.tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("@LynxRobot"):
                buttons = [
                    (Button.inline("Open Main Menu", data="open_menu"),),
                ]
                photo_bytesio = lynxlogo
                result = builder.photo(
                    photo_bytesio,
                    link_preview=False,
                    text=f"**Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\nLicense: GNU AFFERO GENERAL PUBLIC LICENSE v3.0**",
                    buttons=buttons,
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "Bantuan Dari 𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭",
                    text="Daftar Plugins",
                    buttons=[],
                    link_preview=True)
            else:
                result = builder.article(
                    "╔╡𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭╞╗",
                    text="""**Anda Bisa Membuat 𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭 Anda Sendiri\nDengan Cara :**__Tekan Dibawah Ini__ 👇""",
                    buttons=[
                        [
                            custom.Button.url(
                                "𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭",
                                "https://github.com/aryazakaria01/SkyNet-Userbot"),
                            custom.Button.url(
                                "Dᴇᴠᴇʟᴏᴘᴇʀ",
                                "t.me/CyberSupportGroup")],
                        [custom.Button.url(
                            "⚒️ 𝗗𝗘𝗣𝗟𝗢𝗬 ⚒️",
                            "https://github.com/aryazakaria01/SkyNet-Userbot")]],
                    link_preview=True,
                )
            await event.answer([result] if result else None)

        @lynx.tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith(
                    "@LynxAliveRobot"):
                _result = alive_inline()
                photo_bytesio = alivvlogo
                result = builder.photo(photo_bytesio,
                                       link_preview=False,
                                       text=_result[0],
                                       buttons=_result[1],
                                       )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "Bantuan Dari 𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭",
                    text="Daftar Plugins",
                    buttons=[],
                    link_preview=True)
            else:
                result = builder.article(
                    "╔╡𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭╞╗",
                    text="""**Anda Bisa Membuat 𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭 Anda Sendiri\nDengan Cara :**__Tekan Dibawah Ini__ 👇""",
                    buttons=[
                        [
                            custom.Button.url(
                                "𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭",
                                "https://github.com/aryazakaria01/SkyNet-Userbot"),
                            custom.Button.url(
                                "Dᴇᴠᴇʟᴏᴘᴇʀ",
                                "t.me/CyberSupportGroup")],
                        [custom.Button.url(
                            "⚒️ 𝗗𝗘𝗣𝗟𝗢𝗬 ⚒️",
                            "https://github.com/aryazakaria01/SkyNet-Userbot")]],
                    link_preview=True,
                )
            await event.answer([result] if result else None)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"mainmenu")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                buttons = paginate_help(0, dugmeler, "helpme")
                text = f"\n**Bᴏᴛ ᴏꜰ {DEFAULTUSER}**\n\n`Branch  :` __{repo.active_branch.name}__\n`Bot     :` __v{BOT_VER}__\n`Plugins :` __{len(plugins)}__\n\n\n**Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\nLicense: GNU AFFERO GENERAL PUBLIC LICENSE v3.0**"
                await event.edit(text,
                                 file=skynetlogo,
                                 buttons=buttons,
                                 link_preview=False,
                                 )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"opener")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                current_page_number = int(unpage)
                buttons = paginate_help(current_page_number, plugins, "helpme")
                text = f"\n**Bᴏᴛ ᴏꜰ {DEFAULTUSER}**\n\n`Branch  :` __{repo.active_branch.name}__\n`Bot     :` __v{BOT_VER}__\n`Plugins :` __{len(plugins)}__\n\n\n**Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\nLicense: GNU AFFERO GENERAL PUBLIC LICENSE v3.0**"
                await event.edit(text,
                                 file=skynetlogo,
                                 buttons=buttons,
                                 link_preview=False,
                                 )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © Lynx-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"open_menu")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # Lynx-Openeer
                # https://t.me/TelethonChat/115200
                    text = f"**Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\nLicense: GNU AFFERO GENERAL PUBLIC LICENSE v3.0**"
                    await event.edit(text,
                    file=Skynetlogo,
                    link_preview=True,
                    buttons=[
                        [custom.Button.inline("⚙️ Settings ⚙️", data="settings")],
                        [custom.Button.inline("Plugins", data="mainmenu")],
                        [custom.Button.inline("Close", data="close")],
                    ]
                )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"close")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                buttons = [
                    (custom.Button.inline("Open Menu Again", data="open_menu"),),
                ]
                await event.edit(f"**Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\nLicense: GNU AFFERO GENERAL PUBLIC LICENSE v3.0**", file=lynxlogo, buttons=buttons)
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © Lynx-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"settings")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # Lynx-Settings
                text = f"**Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\nLicense: GNU AFFERO GENERAL PUBLIC LICENSE v3.0**"
                await event.edit(text,
                    file=skynetlogo,
                    link_preview=False,
                    buttons=[
                        [
                            custom.Button.inline("ᴀʟɪᴠᴇ", data="allive")
                        ],
                        [
                            custom.Button.url("SkyNet-Userbot",
                                              "t.me/CyberSupportGroup"),
                            custom.Button.url("My Instagram",
                                              f"{INSTAGRAM_ALIVE}")
                        ],
                        [custom.Button.inline("Back", data="open_menu")],
                    ]
                )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"allive")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                _result = alive_inline()
                await event.edit(_result[0], buttons=_result[1],
                                 link_preview=False,
                                 file=alivvlogo,
                                 )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_next\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_back\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # Lynx-Openeer
                # https://t.me/TelethonChat/115200
                text = f"**Copyright © 𝟤𝟢𝟤𝟣 SkyNet-Userbot\nLicense: GNU AFFERO GENERAL PUBLIC LICENSE v3.0**"
                await event.edit(text,
                    file=lynxlogo,
                    link_preview=True,
                    buttons=[
                        [custom.Button.inline("⚙️ Settings ⚙️", data="settings")],
                        [custom.Button.inline("Plugins", data="mainmenu")],
                        [custom.Button.inline("Close", data="close")],
                    ]
                )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_prev\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1, dugmeler, "helpme"  # pylint:disable=E0602
                )
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @lynx.tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(b"ub_modul_(.*)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 150:
                    help_string = (
                        str(CMD_HELP[modul_name]).replace(
                            '`', '')[:150] + "..."
                        + "\n\nBaca Text Berikutnya Ketik .help "
                        + modul_name
                        + " "
                    )
                else:
                    help_string = str(CMD_HELP[modul_name]).replace('`', '')

                reply_pop_up_alert = (
                    help_string
                    if help_string is not None
                    else "{} Tidak Ada Document Yang Tertulis Untuk Plugin".format(
                        modul_name
                    )
                )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n © SkyNet-Userbot"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    except BaseException:
        LOGS.info(
            "Mode Inline Bot Mu Nonaktif. "
            "Untuk Mengaktifkannya, Silahkan Pergi Ke @BotFather Lalu, Settings Bot > Pilih Mode Inline > Turn On."
        )
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID environment variable isn't a "
            "valid entity. Check your environment variables/config.env file."
        )
        quit(1)
