# Based Plugins
# Ported By liualvinas/Alvin

from telethon import events
from userbot.events import register
from userbot import CMD_HELP

PRINTABLE_ASCII = range(0x21, 0x7F)


def aesthetify(string):
    for c in string:
        c = ord(c)
        if c in PRINTABLE_ASCII:
            c += 0xFF00 - 0x20
        elif c == ord(" "):
            c = 0x3000
        yield chr(c)


@register(outgoing=True, pattern=r"^\.ae(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    text = event.pattern_match.group(1)
    text = "".join(aesthetify(text))
    await event.edit(text=text, parse_mode=None, link_preview=False)
    raise events.StopPropagation


CMD_HELP.update({
    "aeshtetic": "✘ Pʟᴜɢɪɴ : Aesthetic Font\
    \n\n⚡𝘾𝙈𝘿⚡: `.ae <Text>`\
    \n↳ : Change Fonts."
})
