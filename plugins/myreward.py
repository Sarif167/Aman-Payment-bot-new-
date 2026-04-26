import re # Fixed: lowercase 'import'
from datetime import datetime, timedelta
import pytz
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 
from database.users_db import db
from info import REWARD_PIC

REWARD_TIERS = [
    {"cost": 180, "duration": "48 ʜᴏᴜʀ", "hours": 48},  
    {"cost": 150, "duration": "24 ʜᴏᴜʀ", "hours": 24},  
    {"cost": 110, "duration": "12 ʜᴏᴜʀ", "hours": 12},  
    {"cost": 60,  "duration": "6 ʜᴏᴜʀ",  "hours": 6},   
    {"cost": 50,  "duration": "2 ʜᴏᴜʀ",  "hours": 2}    
]

@Client.on_message(filters.command("myreward") & filters.private)
async def check_rewards(client: Client, message: Message):
    user_id = message.from_user.id
    # Database se coins fetch karein
    user_data = await db.rewards.find_one({"user_id": user_id})
    coins = user_data.get("coins", 0) if user_data else 0

    # Base Text with Stylish Font
    base_text = f"🎁 <b>ʏᴏᴜʀ ʀᴇᴡᴀʀᴅ ᴘᴏɪɴᴛs:</b> <code>{coins}</code>\n\n"

    if coins == 0:
        return await message.reply_photo(
            photo=REWARD_PIC,
            caption=base_text + "⚠️ <b>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ʀᴇᴡᴀʀᴅ ᴘᴏɪɴᴛs ʏᴇᴛ!</b>\n<i>ʙᴏᴛ ᴜsᴇ ᴋᴀʀᴇɪɴ ᴀᴜʀ ᴘᴏɪɴᴛs ᴇᴀʀɴ ᴋᴀʀᴇɪɴ.</i>"
        )

    # Best eligible tier find karein
    eligible_tier = next((tier for tier in REWARD_TIERS if coins >= tier["cost"]), None)

    if eligible_tier:
        # Yeh button 'cb_handler' mein 'Selection Menu' (Movie/Insta) ko trigger karega
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"👑 ᴄʟᴀɪᴍ {eligible_tier['duration']} ᴘʀᴇᴍɪᴜᴍ", callback_data=f"claim_{user_id}")],
            [InlineKeyboardButton("✖️ ᴄʟᴏsᴇ", callback_data="close_data")]
        ])
        
        caption = (
            base_text +
            f"🎉 <b>ʏᴏᴜ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴏɪɴᴛs ᴛᴏ ᴄʟᴀɪᴍ ᴀ ʀᴇᴡᴀʀᴅ!</b>\n\n"
            f"🎁 <b>ᴀᴠᴀɪʟᴀʙʟᴇ ʀᴇᴡᴀʀᴅ:</b> <code>{eligible_tier['duration']} ᴘʀᴇᴍɪᴜᴍ</code>\n"
            f"💰 <b>ᴄᴏsᴛ:</b> <code>{eligible_tier['cost']} ᴘᴏɪɴᴛs</code>\n\n"
            f"👇 <b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴄʟᴀɪᴍ ʏᴏᴜʀ ʀᴇᴡᴀʀᴅ:</b>"
        )
        await message.reply_photo(
            photo=REWARD_PIC,
            caption=caption,
            reply_markup=keyboard
        )
    else:
        # Minimum 50 points required
        caption = (
            base_text + 
            "⚠️ <b>ʏᴏᴜ ɴᴇᴇᴅ ᴀᴛ ʟᴇᴀsᴛ 50 ᴘᴏɪɴᴛs ᴛᴏ ᴄʟᴀɪᴍ ᴛʜᴇ ғɪʀsᴛ ʀᴇᴡᴀʀᴅ ᴛɪᴇʀ!</b>\n\n"
            "🚀 <i>ᴋᴇᴇᴘ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴇᴀʀɴ ᴍᴏʀᴇ ᴘᴏɪɴᴛs.</i>"
        )
        await message.reply_photo(
            photo=REWARD_PIC,
            caption=caption
        )
        
