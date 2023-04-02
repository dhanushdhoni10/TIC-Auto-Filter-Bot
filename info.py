import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
PORT = environ.get("PORT", "8080")
WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://graph.org/file/97a26138845e20df7877d.jpg https://graph.org/file/dc0eeb7b1ccff88c8a7bd.jpg https://graph.org/file/7a28e808fe665b3263311.jpg https://graph.org/file/5ddda3fc33cd8ff979305.jpg https://graph.org/file/3211cd9459d85452f0aee.jpg https://graph.org/file/24b8081da43a04d28f1b0.jpg https://graph.org/file/7ddbcd34628a266dc21ea.jpg https://graph.org/file/fa212b80229fd74f84e35.jpg https://graph.org/file/df2f8bfdbab98643b0764.jpg https://graph.org/file/b820de0aeb193e6de34b3.jpg https://graph.org/file/3f0332f067b4d9aaef4e8.jpg https://graph.org/file/31560912cd67b601c70cf.jpg https://graph.org/file/59fce6fc8a51f48ac7858.jpg https://graph.org/file/183a777f709959ffa3b05.jpg https://graph.org/file/1fbe27cb31c1c0cfee2a7.jpg https://graph.org/file/b8e0574bdffb9ac77002c.jpg https://graph.org/file/eea62bb410c572fa6eabf.jpg https://graph.org/file/3974cac35f82ad736e43d.jpg https://graph.org/file/faac2e07ba2cc922fa65b.jpg https://graph.org/file/c701eb597f9f268e2959c.jpg https://graph.org/file/5ec376b8255c09b90e6d5.jpg https://graph.org/file/d621e264d7fe15b31ab41.jpg https://graph.org/file/5e5352d077e411dae9d8a.jpg https://graph.org/file/7c99850c364bce70ace0a.jpg https://graph.org/file/88f48485ef6ce73a3a794.jpg https://graph.org/file/454b12802f719cc541d62.jpg https://graph.org/file/00f981e0a99095e76631b.jpg https://graph.org/file/a392be492743c37071fdd.jpg https://graph.org/file/66b6d2fe2fb94f5c74221.jpg https://graph.org/file/e6bb09a75225051c48d05.jpg https://graph.org/file/99283690c547591e74b56.jpg https://graph.org/file/2f0e45f972b26b3679328.jpg https://graph.org/file/63b12dc66953073e5d923.jpg https://graph.org/file/076f9057a60baaec4322f.jpg https://graph.org/file/ebc88585ff7b2884d1457.jpg https://graph.org/file/1d41eeb0a0068fb691540.jpg https://graph.org/file/aa20e94827a05ae376e8f.jpg https://graph.org/file/6bb4a8ab8e78dcb089d16.jpg https://graph.org/file/d9a0b7a25fa35406d97f1.jpg https://graph.org/file/90b0659003ee97dc2e1cf.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'TIC_Files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', 'ʜᴇʏ {user} 👋\n\nᴍʏ ɴᴀᴍᴇ ɪs {bot},\n\nɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴍᴏᴠɪᴇs ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ\n\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ɢᴇᴛ ᴍᴏᴠɪᴇs ʜᴇʀᴇ ɪɴ ʙᴏᴛ ᴘᴍ')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "⚠️ ʜᴇʏ {query}! ᴅᴏɴᴛ ᴛᴏᴜᴄʜ ᴏᴛʜᴇʀ's ᴍᴏᴠɪᴇ ʀᴇǫᴜᴇsᴛ\n\nᴘʟᴇᴀsᴇ ʀᴇǫᴜᴇsᴛ ʏᴏᴜʀ ᴏᴡɴ")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', 'sᴏʀʀʏ , ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇ ғɪʟᴇs\n\nᴊᴏɪɴ ᴏᴜʀ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴀɴᴅ ᴄʟɪᴄᴋ ᴛʀʏ ᴀɢᴀɪɴ')
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "ʜᴇʏ {user}\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chat}")
PMFILTER = environ.get('PMFILTER', "True")
G_FILTER = bool(environ.get("G_FILTER", True))
BUTTON_LOCK = environ.get("BUTTON_LOCK", "True")

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "43200"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', '')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
PM_IMDB = environ.get('PM_IMDB', "False")
IMDB = is_enabled((environ.get('IMDB', "False")), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "{file_name}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", None)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌\nIMDb Data:\n🏷 Title: <a href={url}>{title}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🎭 Genres: {genres}")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)



