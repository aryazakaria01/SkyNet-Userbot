from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern='^.P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`as-salamu'alaikum wr. wb.`🙏")


@register(outgoing=True, pattern='^.p(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`as-salamu'alaikum wr. wb.`🙏")


@register(outgoing=True, pattern='^.L(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`wa'alaikumussalam wr. wb.`🙏")


@register(outgoing=True, pattern='^.l(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`wa'alaikumussalam wr. wb.`🙏")


CMD_HELP.update({
    "salam":
    "✘ Pʟᴜɢɪɴ : Assalamu'alaikum wr. wb.\
\n\n⚡𝘾𝙈𝘿⚡: `.P`\
\n↳ : Untuk Memberi Salam.\
\n\n⚡𝘾𝙈𝘿⚡: `.L`\
\n↳ : Untuk Menjawab Salam."
})
