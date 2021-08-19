# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Modified by KENZO @SyndicateTwenty4
# Port by Lynx-Userbot

import io
import textwrap
import cv2
import os

from random import choice, randint
from textwrap import wrap
from io import BytesIO
from requests import get

from PIL import Image, ImageDraw, ImageFont
from asyncio.exceptions import TimeoutError

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.errors import ChatSendInlineForbiddenError, ChatSendStickersForbiddenError

from userbot.events import register
from userbot import CMD_HELP, bot

# Credits Ultroid


@register(outgoing=True, pattern=r"^\.honka (.*)")
async def honkasays(event):
    await event.edit("`Sedang Memproses, Mohon Tunggu Sebentar...`")
    text = event.pattern_match.group(1)
    if not text:
        return await event.edit("Beri Aku Bebeberapa Text, Contoh : `.honka space <text>`")
    try:
        if not text.endswith("."):
            text = text + "."
        if len(text) <= 9:
            results = await bot.inline_query("honka_says_bot", text)
            await results[2].click(
                event.chat_id,
                silent=True,
                hide_via=True,
            )
        elif len(text) >= 14:
            results = await bot.inline_query("honka_says_bot", text)
            await results[0].click(
                event.chat_id,
                silent=True,
                hide_via=True,
            )
        else:
            results = await bot.inline_query("honka_says_bot", text)
            await results[1].click(
                event.chat_id,
                silent=True,
                hide_via=True,
            )
        await event.delete()
    except ChatSendInlineForbiddenError:
        await event.edit("`Mohon Maaf, Saya Tidak Bisa Menggunakan Hal-Hal Sebaris Disini.`")
    except ChatSendStickersForbiddenError:
        await event.edit("Mohon Maaf, Tidak Bisa Mengirim Sticker Disini.")


@register(outgoing=True, pattern=r"^\.stext (.*)")
async def stext(event):
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`Mohon Maaf Yang Mulia, Saya Membutuhkan Text Anda.`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    font = ImageFont.truetype(
        "userbot/utils/styles/ProductSans-BoldItalic.ttf",
        size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(
            "userbot/utils/styles/ProductSans-BoldItalic.ttf",
            size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2,
         (512 - height) / 2),
        sticktext,
        font=font,
        fill="white")

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream)


@register(outgoing=True, pattern=r"^\.q")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        return await qotli.edit("```Please reply to message.```")
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        return await qotli.edit("```Please reply to message.```")
    chat = "@QuotLyBot"
    if reply_message.sender.bot:
        return await qotli.edit("```Please reply to message.```")
    await qotli.edit("```Processing stickers, please wait.```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(
                        incoming=True,
                        from_users=1031952739))
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
# St No Effect
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await qotli.reply("```Please don't block `@QuotLyBot`\nUnblock or press start then try again.```")
            if response.text.startswith("Hi!"):
                await qotli.edit("```Please disable ur forward Privacy Settings.```")
            else:
                await qotli.delete()
                await bot.forward_messages(qotli.chat_id, response.message)
                await bot.send_read_acknowledge(qotli.chat_id)
# St No Effect
                await qotli.client.delete_messages(conv.chat_id,
                                                   [msg.id, response.id])
    except TimeoutError:
        await qotli.edit()


@register(outgoing=True, pattern=r"^\.tiny(?: |$)(.*)", disable_errors=True)
async def _(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit("`Mohon Balas Ke Sticker`")
        return
    xx = await event.edit("`Proccesing....`")
    ik = await bot.download_media(reply)
    im1 = Image.open("userbot/utils/styles/Lynx-Userbot.png")
    if ik.endswith(".tgs"):
        await event.client.download_media(reply, "ult.tgs")
        os.system("lottie_convert.py ult.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        json.close()
        jsn = jsn.replace("512", "2000")
        open("json.json", "w").write(jsn)
        os.system("lottie_convert.py json.json ult.tgs")
        file = "ult.tgs"
        os.remove("json.json")
    elif ik.endswith((".gif", ".mp4")):
        iik = cv2.VideoCapture(ik)
        dani, busy = iik.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(ik)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await event.client.send_file(event.chat_id, file, reply_to=event.reply_to_msg_id)
    await xx.delete()
    os.remove(file)
    os.remove(ik)


@register(outgoing=True, pattern=r"^\.imp (.*)")
async def f_load(message):
    clrs = {
        "red": 1,
        "lime": 2,
        "green": 3,
        "blue": 4,
        "cyan": 5,
        "brown": 6,
        "purple": 7,
        "pink": 8,
        "orange": 9,
        "yellow": 10,
        "white": 11,
        "black": 12,
    }
    clr = randint(1, 12)
    text = message.pattern_match.group(1)
    reply = await message.get_reply_message()
    if text in clrs:
        clr = clrs[text]
        text = None
    if not text:
        if not reply:
            await bruh(message, message.sender)
            return
        if not reply.text:
            await bruh(message, reply.sender)
            return
        text = reply.pattern_match.group(1)

    if text.split(" ")[0] in clrs:
        clr = clrs[text.split(" ")[0]]
        text = " ".join(text.split(" ")[1:])

    if text == "colors":
        await message.edit(
            "Cores disponíveis:\n"
            + ("\n".join([f"• `{i}`" for i in list(clrs.keys())]))
        )
        return

    url = "https://raw.githubusercontent.com/KeyZenD/AmongUs/master/"
    font = ImageFont.truetype(BytesIO(get(url + "bold.ttf").content), 60)
    imposter = Image.open(BytesIO(get(f"{url}{clr}.png").content))
    text_ = "\n".join(["\n".join(wrap(part, 30)) for part in text.split("\n")])
    w, h = ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textsize(
        text_, font, stroke_width=2
    )
    text = Image.new("RGBA", (w + 30, h + 30))
    ImageDraw.Draw(text).multiline_text(
        (15, 15), text_, "#FFF", font, stroke_width=2, stroke_fill="#000"
    )
    w = imposter.width + text.width + 10
    h = max(imposter.height, text.height)
    image = Image.new("RGBA", (w, h))
    image.paste(imposter, (0, h - imposter.height), imposter)
    image.paste(text, (w - text.width, 0), text)
    image.thumbnail((512, 512))
    output = BytesIO()
    output.name = "imposter.webp"
    image.save(output)
    output.seek(0)
    await message.delete()
    await message.client.send_file(message.to_id, output, reply_to=reply)


async def bruh(message, user):
    fn = user.first_name
    ln = user.last_name
    name = fn + (" " + ln if ln else "")
    name = "***" + name
    await message.edit(name + choice([" ", " Tidak "]) + "Adalah Seorang Penipu! ***")


CMD_HELP.update({
    "animastick": "✘ Pʟᴜɢɪɴ : Animated Stickers"
    "\n\n⚡𝘾𝙈𝘿⚡: `.stext` <Text>"
    "\n↳ : Mengubah Teks/Kata-Kata, Menjadi Stiker Anda."
    "\n\n⚡𝘾𝙈𝘿⚡: `.honka` <Text>"
    "\n↳ : Menampilkan Pesan (Text) di Sticker Animasi."
    "\n\n⚡𝘾𝙈𝘿⚡: `.q <Reply>`"
    "\n↳ : Mengubah Text/Pesan Menjadi Sticker."
    "\n\n⚡𝘾𝙈𝘿⚡: `.tiny`"
    "\n↳ : Untuk Memperkecil Sticker."
    "\n\n⚡𝘾𝙈𝘿⚡: `.imp <Text>`"
    "\n↳ : Mengirim Sticker Impostor (Among US)."
})
