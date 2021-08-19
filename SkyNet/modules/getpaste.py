# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot module containing commands for interacting with dogbin(https://del.dog)."""
import os

import aiohttp
from aiofile import async_open

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

DOGBIN_URL = "https://del.dog/"
NEKOBIN_URL = "https://nekobin.com/"
KATBIN_URL = "https://katb.in/"


@register(outgoing=True, pattern=r"^\.paste(?: (k|d)|$)?(?: ([\s\S]+)|$)")
async def paste(pstl):
    """For .paste command, pastes the text directly to nekobin/dogbin"""
    url_type = pstl.pattern_match.group(1)
    url_type = url_type.strip() if url_type else "n"
    match = pstl.pattern_match.group(2)
    match = match.strip() if match else ""
    replied = await pstl.get_reply_message()
    f_ext = ".txt"

    use_dogbin = False
    use_katbin = False
    use_nekobin = False
    if "d" in url_type:
        use_dogbin = True
    elif "k" in url_type:
        use_katbin = True
    elif "n" in url_type:
        use_nekobin = True

    if not match and not pstl.is_reply:
        return await pstl.edit("`What should i paste...?`")

    if match:
        message = match
    elif replied:
        if replied.media:
            downloaded_file_name = await pstl.client.download_media(
                replied,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            f_ext = os.path.splitext(downloaded_file_name)[-1]
            async with async_open(downloaded_file_name, "r") as fd:
                try:
                    message = await fd.read()
                except UnicodeDecodeError:
                    os.remove(downloaded_file_name)
                    return await pstl.edit("`Can't paste this file.`")
            os.remove(downloaded_file_name)
        else:
            message = replied.message

    async with aiohttp.ClientSession() as ses:
        if use_nekobin:
            await pstl.edit("`Pasting to Nekobin...`")
            async with ses.post(
                NEKOBIN_URL + "api/documents", json={"content": message}
            ) as resp:
                if resp.status == 201:
                    response = await resp.json()
                    key = response["result"]["key"]
                    nekobin_final_url = NEKOBIN_URL + key + f_ext
                    reply_text = (
                        "`Pasted successfully!`\n\n"
                        f"[Nekobin URL]({nekobin_final_url})\n"
                        f"[View RAW]({NEKOBIN_URL}raw/{key})"
                    )
                else:
                    reply_text = "`Failed to reach Nekobin.`"
        elif use_dogbin:
            await pstl.edit("`Pasting to Dogbin...`")
            async with ses.post(
                DOGBIN_URL + "documents", data=message.encode("utf-8")
            ) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    key = response["key"]
                    dogbin_final_url = DOGBIN_URL + key + f_ext

                    if response["isUrl"]:
                        reply_text = (
                            "`Pasted successfully!`\n\n"
                            f"[Shortened URL]({dogbin_final_url})\n\n"
                            "`Original(non-shortened) URLs`\n"
                            f"[Dogbin URL]({DOGBIN_URL}v/{key})\n"
                            f"[View RAW]({DOGBIN_URL}raw/{key})"
                        )
                    else:
                        reply_text = (
                            "`Pasted successfully!`\n\n"
                            f"[Dogbin URL]({dogbin_final_url})\n"
                            f"[View RAW]({DOGBIN_URL}raw/{key})"
                        )
                else:
                    reply_text = "`Failed to reach Dogbin.`"
        elif use_katbin:
            await pstl.edit("`Pasting to Katbin...`")
            async with ses.post(
                "https://api.katb.in/api/paste", json={"content": message}
            ) as resp:
                if resp.status == 201:
                    response = await resp.json()
                    katbin_final_url = KATBIN_URL + response.get("paste_id")
                    reply_text = (
                        "`Pasted successfully!`\n\n"
                        f"[Katb.in URL]({katbin_final_url})\n"
                        f"[View RAW]({katbin_final_url}/raw)"
                    )
                else:
                    reply_text = "`Failed to reach Katb.in.`"

    await pstl.edit(reply_text, link_preview=False)


@register(outgoing=True, pattern=r"^\.getpaste(?: |$)(.*)")
async def get_dogbin_content(dog_url):
    """For .getpaste command, fetches the content of a dogbin URL."""
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    await dog_url.edit("`Getting dogbin content...`")

    if textx:
        message = str(textx.message)

    format_normal = f"{DOGBIN_URL}"
    format_view = f"{DOGBIN_URL}v/"

    if message.startswith(format_view):
        message = message[len(format_view):]
    elif message.startswith(format_normal):
        message = message[len(format_normal):]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/"):]
    else:
        return await dog_url.edit("`Is that even a dogbin url?`")

    async with aiohttp.ClientSession(raise_for_status=True) as ses:
        try:
            async with ses.get(f"{DOGBIN_URL}raw/{message}") as resp:
                paste_content = await resp.text()
        except aiohttp.ClientResponseError as err:
            return await dog_url.edit(
                f"Request returned an unsuccessful status code.\n\n{str(err)}"
            )
        except aiohttp.ServerTimeoutError as err:
            return await dog_url.edit(f"Requests timed out.\n\n{str(err)}")
        except aiohttp.TooManyRedirects as err:
            return await dog_url.edit(
                f"Request exceeded the configured number of maximum redirections.\n\n{str(err)}"
            )
        reply_text = (
            f"Fetched Dogbin content successfully!\n\nContent :\n`{paste_content}`"
        )

    await dog_url.edit(reply_text)


CMD_HELP.update(
    {
        "getpaste": "✘ Pʟᴜɢɪɴ : Get & Paste"
        "\n\n⚡𝘾𝙈𝘿⚡: `.paste` or `.paste <d/k>` <Text/Reply>"
        "\n↳ : Paste your text to Nekobin or Dogbin or Katbin"
        "\n\n⚡𝘾𝙈𝘿⚡: `.getpaste`"
        "\n↳ : Gets the content of a paste or shortened url from dogbin (https://del.dog/)"
    }
)
