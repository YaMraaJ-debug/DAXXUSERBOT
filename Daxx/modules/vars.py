import os

from os import getenv
from dotenv import load_dotenv
from pyrogram import filters


if os.path.exists("Internal"):
  load_dotenv("Internal")




class Config(object):
  # REQUIRED VARIABLES
  API_ID = int(getenv("API_ID", 0))
  API_HASH = getenv("API_HASH", None)
  BOT_TOKEN = getenv("BOT_TOKEN", None)
  STRING_SESSION = getenv("STRING_SESSION", None)
  MONGO_DATABASE = getenv("MONGO_DATABASE", None)

  # OPTIONAL VARIABLES
  SESSION_STRING = getenv("SESSION_STRING", None)
  COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", ". ! > *").split())
  USERBOT_PICTURE = getenv("USERBOT_PICTURE", None)
  LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))
  PMPERMIT = getenv("PMPERMIT", "True")
  PERMIT_MSG = getenv("PERMIT_MSG", None)
  PERMIT_LIMIT = int(getenv("PERMIT_LIMIT", 6))


  PLUGINS = {}
  SUPUSER = filters.me
  SUDOERS = filters.user([])
  CRAIDUB = filters.user([])
  LRAIDUB = filters.user([])
  RRAIDUB = filters.user([])
  GDELSUB = filters.user([])
  GBANSUB = filters.user([])
  GMUTEUB = filters.user([])
  COMMAND_HANDLERS = list(COMMAND_PREFIXES)
  COMMAND_HANDLERS.append('')
    #######################################



# get all config variables in a list
all_vars = list(Config.__dict__.keys())
all_vals = list(Config.__dict__.values())

