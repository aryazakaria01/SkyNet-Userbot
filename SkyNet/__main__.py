# Copyright (C) 2021 GNU AFFERO GENERAL PUBLIC LICENSE.
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
#
""" SkyNet start point """

from importlib import import_module

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from SkyNet import BOT_VER, LOGS, bot
from SkyNet.modules import ALL_MODULES

INVALID_PH = (
    "\nERROR: The Phone No. entered is INVALID"
    "\n Tip: Use Country Code along with number."
    "\n or check your phone number and try again !"
)

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("SkyNet.modules." + module_name)


LOGS.info(
    f"𝐒𝐤𝐲𝐍𝐞𝐭-𝐔𝐬𝐞𝐫𝐛𝐨𝐭 🤖 v.{BOT_VER}\n[TELAH DIAKTIFKAN!]")

bot.run_until_disconnected()
