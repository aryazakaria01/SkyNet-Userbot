from SkyNet.events import register
from SkyNet import CMD_HELP

# Port from @VckyouuBitch (GeezProject)


@register(outgoing=True, pattern=r"^\$(?:dm)\s?(.*)?")
async def remoteaccess(event):

    p = event.pattern_match.group(1)
    m = p.split(" ")

    chat_id = m[0]
    try:
        chat_id = int(chat_id)
    except BaseException:

        pass

    msg = ""
    mssg = await event.get_reply_message()
    if event.reply_to_msg_id:
        await event.client.send_message(chat_id, mssg)
        await event.edit("`Success Mengirim Pesan Anda.`")
    for i in m[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await event.client.send_message(chat_id, msg)
        await event.edit("`Success Mengirim Pesan Anda.`")
    except BaseException:
        await event.edit("**Terjadi Error. Lu limit kayanya tot.**")

CMD_HELP.update(
    {
        "dm": "✘ Pʟᴜɢɪɴ : `Direct Message`\
    \n\n⚡𝘾𝙈𝘿⚡: `$dm` <Username> <Pesan/Message>\
    \n↳ : Direct Message Mampu Mengirim Pesan Dimanapun Anda Berada\n Contoh : .dm <Username> <Pesan/Message>."
    })
