import asyncio
import qrcode
import pytz
from io import BytesIO
from datetime import datetime
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from database.users_db import db

class temp(object):
    ME = None
    U_NAME = None
    B_NAME = None
    B_LINK = None
    USERS_CANCEL = False  

FIXED_PRICES = [15, 39, 75, 110, 199, 360]
UPI_ID = "pay.to.prajwal@ybl"
NAME = "prajwal"
CURRENCY = "INR"

FIXED_PRICES2 = {
    15: "1week",
    39: "1month",
    75: "2month",
    110: "3month",
    199: "6month",
    360: "12month"
}

def get_seconds(time_str):
    time_units = {
        'year': 31536000,
        'month': 2592000,
        'week': 604800,
        'day': 86400,
        'hour': 3600,
        'min': 60
    }
    for unit in time_units:
        if time_str.endswith(unit):
            try:
                time_amount = int(time_str.replace(unit, ''))
                return time_amount * time_units[unit]
            except:
                return -1
    return -1
    
def generate_qr(link):
    qr = qrcode.make(link)
    bio = BytesIO()
    bio.name = "qr.png"
    qr.save(bio, "PNG")
    bio.seek(0)
    return bio

FIXED_PRICES3 = {
    15: "1 week premium for",
    39: "1 month premium for",
    75: "2 month premium for",
    110: "3 month premium for",
    199: "6 month premium for",
    360: "12 month premium for"
}

def get_readable_time(seconds: int) -> str:
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}ᴅ "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}ʜ "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}ᴍ "
    seconds = int(seconds)
    result += f"{seconds}s"
    return result

async def users_broadcast(user_id, message, is_pin):
    try:
        m = await message.copy(chat_id=user_id)
        if is_pin:
            try:
                await m.pin(both_sides=True)
            except:
                pass 
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await users_broadcast(user_id, message, is_pin)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        await db.delete_user(int(user_id))
        return False, "Deleted/Blocked"
    except Exception:
        return False, "Error"
        
def get_time_str(amount):
    mapping = {15: "1ᴡᴇᴇᴋ", 39: "1ᴍᴏɴᴛʜ", 75: "2ᴍᴏɴᴛʜ", 110: "3ᴍᴏɴᴛʜ", 199: "6ᴍᴏɴᴛʜ", 360: "12ᴍᴏɴᴛʜ"}
    return mapping.get(amount)

async def payment_timer_task(client, user_id, chat_id, amount, premium_duration, photo_id, text_id):
    await asyncio.sleep(300) 
    state_data = await db.get_payment_state(user_id)
    
    if state_data:
        if state_data.get("photo_id") == photo_id:
            await db.del_payment_state(user_id) 
            try:
                await client.delete_messages(chat_id=chat_id, message_ids=[photo_id, text_id])
            except:
                pass
            
            buttons = [
                [InlineKeyboardButton("🏠 ᴍᴀɪɴ ᴍᴇɴᴜ", callback_data="start"),
                 InlineKeyboardButton("🔄 ʀᴇsᴛᴀʀᴛ", callback_data=f"pay_{amount}")]
            ]
            
            await client.send_message(
                chat_id=chat_id,
                text=(
                    "⏳ <b>ᴘᴀʏᴍᴇɴᴛ ᴛɪᴍᴇ ᴇxᴘɪʀᴇᴅ!</b>\n\n"
                    "ʏᴏᴜʀ 5-ᴍɪɴᴜᴛᴇ ᴘᴀʏᴍᴇɴᴛ ᴡɪɴᴅᴏᴡ ʜᴀs ʙᴇᴇɴ ᴄʟᴏsᴇᴅ. "
                    "ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛʀʏ ᴀɢᴀɪɴ, ᴄʟɪᴄᴋ ʀᴇsᴛᴀʀᴛ ʙᴇʟᴏᴡ."
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
    )
            
