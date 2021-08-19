# Copyright (C) 2020 Adek Maulana.
# All rights reserved.

"""
   Heroku manager for your userbot
"""

import heroku3
import aiohttp
import math
import sys

from os import environ, execle
from userbot import (
    HEROKU_APP_NAME,
    HEROKU_API_KEY,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    ALIVE_NAME)
from userbot.events import register

heroku_api = "https://api.heroku.com"
if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    app = Heroku.app(HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None


"""
   ConfigVars setting, get current var, set var or delete var...
"""


@register(outgoing=True,
          pattern=r"^.(get|del) var(?: |$)(\w*)")
async def variable(var):
    exe = var.pattern_match.group(1)
    if app is None:
        await var.edit("`[HEROKU]"
                       "\nHarap Siapkan`  **HEROKU_APP_NAME**.")
        return False
    if exe == "get":
        await var.edit("`Mendapatkan Informasi...`")
        variable = var.pattern_match.group(2)
        if variable != '':
            if variable in heroku_var:
                if BOTLOG:
                    await var.client.send_message(
                        BOTLOG_CHATID, "#CONFIGVARS\n\n"
                        "**Config Vars** :\n"
                        f"`{variable}` **=** `{heroku_var[variable]}`\n"
                    )
                    await var.edit("`Diterima Ke BOTLOG_CHATID...`")
                    return True
                else:
                    await var.edit("`Mohon Ubah BOTLOG Ke True...`")
                    return False
            else:
                await var.edit("`Informasi Tidak Ditemukan...`")
                return True
        else:
            configvars = heroku_var.to_dict()
            msg = ''
            if BOTLOG:
                for item in configvars:
                    msg += f"`{item}` = `{configvars[item]}`\n"
                await var.client.send_message(
                    BOTLOG_CHATID, "#GETCONFIGVARS\n\n"
                    "**Config Vars** :\n"
                    f"{msg}"
                )
                await var.edit("`Diterima Ke BOTLOG_CHATID`")
                return True
            else:
                await var.edit("`Mohon Ubah BOTLOG Ke True`")
                return False
    elif exe == "del":
        await var.edit("`Menghapus Config Vars...`")
        variable = var.pattern_match.group(2)
        if variable == '':
            await var.edit("`Mohon Tentukan Config Vars Yang Mau Anda Hapus.`")
            return False
        if variable in heroku_var:
            if BOTLOG:
                await var.client.send_message(
                    BOTLOG_CHATID, "#DELCONFIGVARS\n\n"
                    "**Menghapus Config Vars** :\n"
                    f"`{variable}`"
                )
            await var.edit("`Config Vars Telah Dihapus`")
            del heroku_var[variable]
        else:
            await var.edit("`Tidak Dapat Menemukan Config Vars, Kemungkinan Telah Anda Hapus.`")
            return True


@register(outgoing=True, pattern=r'^.set var (\w*) ([\s\S]*)')
async def set_var(var):
    if app is None:
        return await var.edit(
            "`[HEROKU]\nPlease setup your`  "
            "**HEROKU_APP_NAME** and ***HEROKU_API_KEY**."
        )
    await var.edit("`Sedang Menyetel Config Vars...`")
    variable = var.pattern_match.group(1)
    value = var.pattern_match.group(2)
    if variable in heroku_var:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#SETCONFIGVARS\n\n"
                "**Mengganti Config Vars**:\n"
                f"`{variable}` = `{value}`"
            )
        await var.edit("`Sedang Dalam Prosess...\nMohon Menunggu Dalam Beberapa Detik.")
    else:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#ADDCONFIGVARS\n\n"
                "**Menambahkan Config Vars** :\n"
                f"`{variable}` **=** `{value}`"
            )
        await var.edit("`Sedang Menambahkan Config Vars...`")
    heroku_var[variable] = value

    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{var.chat_id}\n{var.id}")
    except AttributeError:
        pass

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


"""
    Check account quota, remaining quota, used quota, used app quota
"""


@register(outgoing=True, pattern=r"^\.kuota(?: |$)")
async def dyno_usage(dyno):
    """Get your account Dyno Usage."""
    if app is None:
        return await dyno.edit(
            "`[HEROKU]\nPlease setup your`  "
            "**HEROKU_APP_NAME** and ***HEROKU_API_KEY**."
        )
    await dyno.edit("`Getting Information...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.117 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    async with aiohttp.ClientSession() as session:
        async with session.get(heroku_api + path, headers=headers) as r:
            if r.status != 200:
                await dyno.client.send_message(
                    dyno.chat_id, f"`{r.reason}`", reply_to=dyno.id
                )
                await dyno.edit("`Can't get information...`")
                return False
            result = await r.json()
            quota = result["account_quota"]
            quota_used = result["quota_used"]

            """ - User Quota Limit and Used - """
            remaining_quota = quota - quota_used
            percentage = math.floor(remaining_quota / quota * 100)
            minutes_remaining = remaining_quota / 60
            hours = math.floor(minutes_remaining / 60)
            minutes = math.floor(minutes_remaining % 60)

            """ - User App Used Quota - """
            Apps = result["apps"]
            for apps in Apps:
                if apps.get("app_uuid") == app.id:
                    AppQuotaUsed = apps.get("quota_used") / 60
                    AppPercentage = math.floor(
                        apps.get("quota_used") * 100 / quota)
                    break
            else:
                AppQuotaUsed = 0
                AppPercentage = 0

            AppHours = math.floor(AppQuotaUsed / 60)
            AppMinutes = math.floor(AppQuotaUsed % 60)

            await dyno.edit(
                "╭┈─╼━━━━━━━━━━━━━━━╾─┈╮ \n"
                "│      ⇱ ⚡𝗟𝘆𝗻𝘅-𝙐𝙎𝙀𝙍𝘽𝙊𝙏⚡ ⇲ \n"
                "╭┈─╼━━━━━━━━━━━━━━━╾─┈╮ \n"
                "│📱◈ 𝐏𝐞𝐧𝐠𝐠𝐮𝐧𝐚𝐚𝐧 𝐊𝐮𝐨𝐭𝐚 𝐀𝐧𝐝𝐚 : \n"
                f"│⏳◈ {AppHours} Jam - {AppMinutes} Menit. \n"
                f"│⚡◈ 𝐏𝐞𝐫𝐬𝐞𝐧𝐭𝐚𝐬𝐞 : {AppPercentage}% \n"
                "╰┈───────────────────┈╮ \n"
                "│📱◈ 𝐒𝐢𝐬𝐚 𝐊𝐮𝐨𝐭𝐚 𝐁𝐮𝐥𝐚𝐧 𝐈𝐧𝐢 : \n"
                f"│⏳◈ {hours} Jam - {minutes} Menit. \n"
                f"│⚡◈ 𝐏𝐞𝐫𝐬𝐞𝐧𝐭𝐚𝐬𝐞 : {percentage}% Lagi. \n"
                "╰┈───────────────────┈╯ \n"
                f"• Oᴡɴᴇʀ  : {ALIVE_NAME} \n"
            )
            return True


CMD_HELP.update({"herokuapp": "✘ Pʟᴜɢɪɴ : Heroku App"
                 "\n\n⚡𝘾𝙈𝘿⚡: `.kuota`"
                 "\n↳ : Check Quota Dyno Heroku"
                 "\n\n⚡𝘾𝙈𝘿⚡: `.set var <NEW VAR> <VALUE>`"
                 "\n↳ : Tambahkan Variabel Baru Atau Memperbarui Variabel"
                 "\nSetelah Menyetel Variabel Tersebut, Lynx-Userbot Akan Di Restart."
                 "\n\n⚡𝘾𝙈𝘿⚡: `.get var atau .get var <VAR>`"
                 "\n↳ : Dapatkan Variabel Yang Ada, !!PERINGATAN!! Gunakanlah Di Group Privasi Anda."
                 "\nIni Mengembalikan Semua Informasi Pribadi Anda, Harap berhati-hati."
                 "\n\n⚡𝘾𝙈𝘿⚡: `.del var <VAR>`"
                 "\n↳ : Menghapus Variabel Yang Ada"
                 "\nSetelah Menghapus Variabel, Bot Akan Di Restart."})
