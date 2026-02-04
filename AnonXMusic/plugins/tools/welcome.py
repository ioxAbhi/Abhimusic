from AnonXMusic import app
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
from os import environ
import random
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, time, aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from logging import getLogger
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger


random_photo = [
    "https://files.catbox.moe/smdxm9.jpg",
]
# --------------------------------------------------------------------------------- #





LOGGER = getLogger(name)

class WelDatabase:
    def init(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        if chat_id not in self.data:
            self.data[chat_id] = {"state": "on"}  # Default state is "on"

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

wlcm = WelDatabase()

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None



def circle(pfp, size=(500, 500), brightness_factor=10):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    pfp = ImageEnhance.Brightness(pfp).enhance(brightness_factor)
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chatname, id, uname, brightness_factor=1.3):
    background = Image.open("AnonXMusic/assets/wel2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp, brightness_factor=brightness_factor) 
    pfp = pfp.resize((500, 500))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('AnonXMusic/assets/font.ttf', size=60)
    welcome_font = ImageFont.truetype('AnonXMusic/assets/font.ttf', size=60)
    
 #   draw.text((630, 230), f"USERNAME : {uname}", fill=(255, 255, 255), font=font)
   # draw.text((630, 300), f'NAME: {user}', fill=(255, 255, 255), font=font)
    draw.text((630, 450), f'ID: {id}', fill=(255, 255, 255), font=font)

    pfp_position = (48, 88)
    background.paste(pfp, pfp_position, pfp)
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"
    @app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "ᴜѕαgє:\n⦿ /welcome [on|off]"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        A = await wlcm.find_one(chat_id)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "off":
            if A:
                await message.reply_text("ᴡєʟᴄᴏϻє ηᴏτɪғɪᴄατɪᴏη αʟʀєαᴅʏ ᴅɪѕαʙʟєᴅ !!")
            else:
                await wlcm.add_wlcm(chat_id)
                await message.reply_text(f"ᴅɪѕαʙʟєᴅ ᴡєʟᴄᴏϻє ηᴏτɪғɪᴄατɪᴏη ɪη  {message.chat.title}")
        elif state == "on":
            if not A:
                await message.reply_text("єηαʙʟє ᴡєʟᴄᴏϻє ηᴏτɪғɪᴄατɪᴏη.")
            else:
                await wlcm.rm_wlcm(chat_id)
                await message.reply_text(f"єηαʙʟєᴅ ᴡєʟᴄᴏϻє ηᴏτɪғɪᴄατɪᴏη ɪη {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("ѕᴏʀʀʏ ᴏηʟʏ αᴅϻɪηѕ ᴄαη єηαʙʟє ᴡєʟᴄᴏϻє ηᴏτɪғɪᴄατɪᴏη!!")



@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    count = await app.get_chat_members_count(chat_id)
    A = await wlcm.find_one(chat_id)
    if A:
        return

    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    
    # Add the modified condition here
    if member.new_chat_member and not member.old_chat_member and member.new_chat_member.status != "kicked":
    
        try:
            pic = await app.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        except AttributeError:
            pic = "AnonXMuisc/assets/upic.png"
        if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
            try:
                await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
            except Exception as e:
                LOGGER.error(e)
        try:
            welcomeimg = welcomepic(
                pic, user.first_name, member.chat.title, user.id, user.username
            )
            button_text = "๏ ᴠɪєᴡ ηєᴡ ϻєϻʙєʀ ๏"
            add_button_text = "✙ ᴋɪᴅηαρ ϻє ✙"
            deep_link = f"tg://openmessage?user_id={user.id}"
            add_link = f"https://t.me/{app.username}?startgroup=true"
            temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
                member.chat.id,
                photo=welcomeimg,
                caption=f"""
⎊─────☵ ᴡєʟᴄᴏϻє ☵─────⎊

▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬

☉ ηαϻє ⧽ {user.mention}
☉ ɪᴅ ⧽ {user.id}
☉ ᴜ_ηαϻє ⧽ @{user.username}
☉ τᴏταʟ ϻєϻʙєʀѕ ⧽ {count}

▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬

⎉──────▢✭ 侖 ✭▢──────⎉
""",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)],
                    [InlineKeyboardButton(text=add_button_text, url=add_link)],
                ])
            )
        except Exception as e:
            LOGGER.error(e)
