""" Userbot module for other small commands. """
from userbot import CMD_HELP, DEFAULTUSER
from userbot.events import register


@register(outgoing=True, pattern="^.lhelp$")
async def usit(e):
    await e.edit(
        f"**Hai {DEFAULTUSER} 🐈 Jika Anda Tidak Tau Perintah Untuk Memerintah Ku,\nKetik:** `.help` Atau Bisa Minta Bantuan Ke\n"
        "\n📬**Developer :**"
        "\n[Telegram](t.me/TeamSecret_Kz)"
        "\n[Dev Repo](https://github.com/KENZO-404)"
        "\n[Instagram](instagram.com/si_axeell)")


@register(outgoing=True, pattern="^.vars$")
async def var(m):
    await m.edit(
        f"**Daftar Vars Untuk {DEFAULTUSER}:**\n"
        "\nClick » [ [Lynx-VARS](https://raw.githubusercontent.com/KENZO-404/Lynx-Userbot/Lynx-Userbot/varshelper.txt) ] «")


CMD_HELP.update({
    "lynxhelper":
    "✘ Pʟᴜɢɪɴ : Lynx Helper\
\n\n⚡𝘾𝙈𝘿⚡: `.lhelp`\
\n↳ : Bantuan Untuk User Lynx.\
\n\n⚡𝘾𝙈𝘿⚡: `.vars`\
\n↳ : Melihat Daftar Vars Lynx-Userbot."
})
