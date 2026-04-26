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

MOVIE_PRICES = [15, 39, 75, 110, 199, 360]
INSTAGRAM_PRICES = [15, 39, 75, 110, 199, 360]

INSTAGRAM_PRICES2 = {
    15: "1week",
    39: "1month",
    75: "2month",
    110: "3month",
    199: "6month",
    360: "12month"
}

MOVIE_PRICES2 = {
    15: "1week",
    39: "1month",
    75: "2month",
    110: "3month",
    199: "6month",
    360: "12month"
}
    
def generate_qr(link):
    qr = qrcode.make(link)
    bio = BytesIO()
    bio.name = "qr.png"
    qr.save(bio, "PNG")
    bio.seek(0)
    return bio

MOVIE_PRICES1 = {
    15: "1 week premium for",
    39: "1 month premium for",
    75: "2 month premium for",
    110: "3 month premium for",
    199: "6 month premium for",
    360: "12 month premium for"
}

INSTAGRAM_PRICES1 = {
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

def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:].strip().lower()
        if value:
            value = int(value)
        return value, unit
        
    value, unit = extract_value_and_unit(time_string)
    unit_mapping = {
        's': 1,
        'sec': 1,
        'second': 1,
        'seconds': 1,
        'min': 60,
        'minute': 60,
        'minutes': 60,
        'hour': 3600,
        'hours': 3600,
        'day': 86400,
        'days': 86400,
        'month': 86400 * 30,
        'months': 86400 * 30,
        'year': 86400 * 365,
        'years': 86400 * 365
    }
    
async def payment_timer_task(client, user_id, chat_id, amount, pay_type, photo_id, text_id):
    await asyncio.sleep(300) # 5 minutes
    state_data = await db.get_payment_state(user_id)
    
    # Check karein agar payment abhi bhi pending hai
    if state_data and state_data.get("photo_id") == photo_id:
        await db.del_payment_state(user_id) 
        try:
            await client.delete_messages(chat_id=chat_id, message_ids=[photo_id, text_id])
        except:
            pass
        
        # Restart button will now point to pay_mov_ or pay_inst_
        buttons = [
            [
                InlineKeyboardButton("🏠 ᴍᴀɪɴ ᴍᴇɴᴜ", callback_data="start"),
                InlineKeyboardButton("🔄 ʀᴇsᴛᴀʀᴛ", callback_data=f"pay_{pay_type}_{amount}")
            ]
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
        
