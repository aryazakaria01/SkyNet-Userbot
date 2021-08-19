# imported from ppe-remix by @heyworld & @DeletedUser420
# Based Code by @adekmaulana
# Improve by @aidilaryanto
from asyncio import sleep
import re
import random

from userbot import CMD_HELP, bot
from userbot.events import register


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+")


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, '', inputString)


@register(outgoing=True, pattern="^.waifu(?: |$)(.*)")
async def waifu(animu):
    #"""Generate random waifu sticker with the text!"""

    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.answer("`No text given, hence the waifu ran away.`")
            return
    animus = [15, 30, 32, 33, 40, 41, 42, 48, 55, 58]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}")
    try:
        await sticcers[0].click(
            animu.chat_id,
            reply_to=animu.reply_to_msg_id,
            silent=True if animu.is_reply else False,
            hide_via=True,
        )
    except Exception:
        return await animu.edit(
            "`You cannot send inline results in this chat (caused by SendInlineBotResultRequest)`"
        )
    await sleep(5)
    await animu.delete()


CMD_HELP.update({
    "waifu": "✘ Pʟᴜɢɪɴ : Waifu\
    \n\n⚡𝘾𝙈𝘿⚡: `.waifu` <Text>\
    \n↳ : For Custom Stickers."
})
