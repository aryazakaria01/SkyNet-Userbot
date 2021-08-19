# © Copyright 2021 Lynx-Userbot LLC Company.
# GPL-3.0 License From Github
# Ported by @TeamSecret_Kz (KENZO)
# WARNING !!
# Credits by @TeamUltroid

from userbot.events import register
from userbot import bot


@register(outgoing=True, pattern=r"^\.ggcast (.*)")
async def gcast(event):
    """Adds given chat to global group cast."""
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Mohon Berikan Sebuah Pesan`")
    tt = event.text
    msg = tt[7:]
    kk = await event.edit("`Sedang Mengirim Pesan Group Secara Global... 📢`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group and not x.is_user:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**✔️Berhasil** Mengirim Pesan Ke : `{done}` Group.\n**❌Gagal** Mengirim Pesan Ke : `{er}` Group.")


@register(outgoing=True, pattern=r"^\.gucast (.*)")
async def gucast(event):
    """Adds given chat to global user cast."""
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("`Mohon Berikan Sebuah Pesan`")
    tt = event.text
    msg = tt[7:]
    kk = await event.edit("`Sedang Mengirim Pivate Messages Secara Global... 📢`")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**✔️Berhasil** Mengirim Pesan Ke : `{done}` Orang.\n**❌Gagal** Mengirim Pesan Ke : `{er}` Orang.")
