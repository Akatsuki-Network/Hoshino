import os
from Hoshino import hoshi as logger
from sys import exit

API_ID = os.getenv("API_ID", 28122413) or (logger.error("API_ID is not defined.") or exit(1))
API_HASH = os.getenv("API_HASH", "750432c8e1b221f91fd2c93a92710093") or (logger.error("API_HASH is not defined.") or exit(1))
BOT_TOKEN = os.getenv("BOT_TOKEN", "7680292640:AAFMnLNbZcmkkEILKIw5MpgrtqGDLhDG5hs") or (logger.error("BOT_TOKEN is not defined.") or exit(1))
#SUPPORT_CHAT = os.getenv("SUPPORT_CHAT") or (logger.error("SUPPORT_CHAT is not defined.") or exit(1))
#UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL") or (logger.error("UPDATE_CHANNEL is not defined.") or exit(1))
BOT_UNAME = os.getenv("BOT_UNAME", "@NsfwGuardianBot") or (logger.error("BOT_UNAME is not defined.") or exit(1))
#MONGO_URI = os.getenv("MONGO_URI", "") or (logger.error("MONGO_URI is not defined.") or exit(1))

DEV_LIST = list(map(int, os.getenv("DEV_LIST", "6312693124").split())) or (logger.error("DEV_LIST is not defined.") or exit(1))
SUDO = list(map(int, os.getenv("SUDO", "6312693124").split())) or (logger.error("SUDO is not defined.") or exit(1))
