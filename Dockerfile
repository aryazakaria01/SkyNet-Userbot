# Docker Tag Images, Using Python Slim Buster.
FROM aryazakaria01/skynetuser:Buster
# ==========================================
#              Lynx - Userbot
# ==========================================
RUN git clone -b SkyNet-Userbot https://github.com/aryazakaria01/SkyNet-Userbot /home/SkyNet-Userbot \
    && chmod 777 /home/SkyNet-Userbot \
    && mkdir /home/SkyNet-Userbot/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/SkyNet-Userbot/

WORKDIR /home/SkyNet-Userbot/

# Finishim
CMD ["bash","./resource/startup/startup.sh"]
