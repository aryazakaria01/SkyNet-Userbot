from SkyNet import CMD_HELP
from SkyNet.events import register


@register(outgoing=True, pattern='^$P(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb.`π")


@register(outgoing=True, pattern='^$p(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb.`π")


@register(outgoing=True, pattern='^$PA(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb. Sayang`π")


@register(outgoing=True, pattern='^$pa(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`As-salamu'alaikum wr. wb. Sayang`π")


@register(outgoing=True, pattern='^$L(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb.`π")


@register(outgoing=True, pattern='^$LA(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb.`π")


@register(outgoing=True, pattern='^$l(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb.`π")


@register(outgoing=True, pattern='^$la(?: |$)(.*)')
async def typewriter(typew):
    typew.pattern_match.group(1)
    await typew.edit("`Wa'alaikumussalam wr. wb. Sayang`π")

CMD_HELP.update({
    "salam":
    "β PΚα΄Ι’ΙͺΙ΄ : Assalamu'alaikum wr. wb.\
\n\nβ‘πΎππΏβ‘: `$P`\
\nβ³ : Untuk Memberi Salam.\
\n\nβ‘πΎππΏβ‘: `$L`\
\nβ³ : Untuk Menjawab Salam."
})
