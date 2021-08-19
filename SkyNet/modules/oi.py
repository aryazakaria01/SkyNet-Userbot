from time import sleep
from userbot.events import register


@register(outgoing=True, pattern='^.axel(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(3)
    await typew.edit("`Hai Perkenalkan Namaku Axel`")
    sleep(3)
    await typew.edit("`21 Tahun`")
    sleep(1)
    await typew.edit("`Tinggal Di Tangerang, Salam Kenal :)`")
# Create by myself @localheart


@register(outgoing=True, pattern='^.sayang(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(3)
    await typew.edit("`Cuma Mau Bilang`")
    sleep(3)
    await typew.edit("`Aku Sayang Kamu`")
    sleep(1)
    await typew.edit("`I LOVE YOU 💞`")
# Create by myself @localheart


@register(outgoing=True, pattern='^.semangat(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(3)
    await typew.edit("`Apapun Yang Terjadi`")
    sleep(3)
    await typew.edit("`Tetaplah Putus Asa...`")
    sleep(3)
    await typew.edit("#KITHEART\n`Dan Selalu Berputus Asa :)`")
# Create by myself @localheart


@register(outgoing=True, pattern='^.padadimana(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(7)
    await typew.edit("`Pada Dimanaa ?`")
    sleep(6)
    await typew.edit("`Woiiii...`")
    sleep(5)
    await typew.edit("`Dimanaa oiii`")
    sleep(5)
    await typew.edit("`Memeg...`")
# Create by myself @localheart
