# Based Plugins
# Ported For Lord-Userbot By liualvinas/Alvin
# If You Kang It Don't Delete / Warning!! Jangan Hapus Ini!!!
from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.xogame(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


# Alvin Gans


@register(outgoing=True, pattern=r"^\.mod(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    modr = event.pattern_match.group(1)
    botusername = "@PremiumAppBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, modr)
    await tap[0].click(event.chat_id)
    await event.delete()

# Ported For Lord-Userbot By liualvinas/Alvin

CMD_HELP.update({
    "games": "✘ Pʟᴜɢɪɴ : Games\
\n\n⚡𝘾𝙈𝘿⚡: `.xogame`\
\n↳ : Mainkan game XO bersama Temanmu.\
\n\n⚡𝘾𝙈𝘿⚡: `.mod <Nama App>`\
\n↳ : Dapatkan applikasi mod."})
