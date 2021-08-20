from SkyNet import CMD_HELP
from SkyNet.events import register


@register(outgoing=True, pattern='^$P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb.`🙏")


@register(outgoing=True, pattern='^$p(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb.`🙏")


@register(outgoing=True, pattern='^$PA(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb. Sayang`🙏")


@register(outgoing=True, pattern='^$pa(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb. Sayang`🙏")


@register(outgoing=True, pattern='^$L(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb.`🙏")


@register(outgoing=True, pattern='^$LA(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb.`🙏")


@register(outgoing=True, pattern='^$l(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb.`🙏")


@register(outgoing=True, pattern='^$la(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb. Sayang`🙏")

CMD_HELP.update({
    "salam":
    "✘ Pʟᴜɢɪɴ : Assalamu'alaikum wr. wb.\
\n\n⚡𝘾𝙈𝘿⚡: `$P`\
\n↳ : Untuk Memberi Salam.\
\n\n⚡𝘾𝙈𝘿⚡: `$L`\
\n↳ : Untuk Menjawab Salam."
})
