import pytz
from datetime import date, datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from Script import script
from info import LOG_CHANNEL, START_PIC, FSUB, CHANNEL
from utils import temp, MOVIE_PRICES, INSTAGRAM_PRICES
from plugins.fsub import is_user_joined

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    
    # 1. Force Join Check (Sabse pehle)
    if FSUB and not await is_user_joined(client, message):
        return

    # 2. Database & Logs
    first_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "ɴᴏɴᴇ"
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    time_str = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%d-%m-%Y")

    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, first_name, username, date_str)
        await client.send_message(
            LOG_CHANNEL, 
            script.LOG_TEXT.format(temp.B_NAME, mention, user_id, username, time_str, date_str)
        )

    # 3. Parameter Handling (movie ya inst links)
    if len(message.command) == 2:
        data = message.command[1]
        
        if data.startswith('movie'):
            _, group_id = data.split("-")
            return await movie_menu(client, message)

        if data.startswith('inst'):
            _, group_id = data.split("-")
            return await inst_menu(client, message)

    # 4. Default Start Message (Agar koi parameter nahi hai)
    buttons = [[
        InlineKeyboardButton("❤️ 𝐁𝐀𝐂𝐊𝐔𝐏 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ❤️", url=CHANNEL)],
        [InlineKeyboardButton("ℹ️ ʜᴇʟᴘ", callback_data="help"),
        InlineKeyboardButton("👨‍💻 ᴀʙᴏᴜᴛ", callback_data="about")
    ]]

    await message.reply_photo(
        photo=START_PIC,
        caption=script.START_TXT.format(mention, temp.B_NAME),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    ) 

async def movie_menu(client, message, group_id=None):
    user_id = message.from_user.id
    user_data = await db.get_user(user_id)
    current_time = datetime.now()

    # Sirf Movie ki expiry check karein (expiry_mov)
    expiry_mov = user_data.get("expiry_mov")
    if expiry_mov:
        if expiry_mov.tzinfo:
            expiry_mov = expiry_mov.replace(tzinfo=None)
        
        if expiry_mov > current_time:
            buttons = [[InlineKeyboardButton("📞 Cᴏɴᴛᴀᴄᴛ Mᴇ", url="https://t.me/premiumuseronly_Bot")]]
            return await message.reply_text(
                text="🌟 <b>Yᴏᴜ Aʟʀᴇᴀᴅʏ Hᴀᴠᴇ Mᴏᴠɪᴇ Pᴀss!</b>\n\n<i>Cʜᴇᴄᴋ ᴅᴇᴛᴀɪʟs ᴠɪᴀ /myplan.</i>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    price_buttons = []
    row = []
    for price in MOVIE_PRICES:
        row.append(InlineKeyboardButton(f"🎬 ₹{price}", callback_data=f"pay_mov_{price}"))
        if len(row) == 3:
            price_buttons.append(row)
            row = []
    if row: price_buttons.append(row)
    price_buttons.append([InlineKeyboardButton("📞 Cᴏɴᴛᴀᴄᴛ Mᴇ", url="https://t.me/premiumuseronly_Bot")])
    
    await message.reply_text(
        text=f"🍿 <b>Mᴏᴠɪᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ Pʟᴀɴs</b>\n\nSᴇʟᴇᴄᴛ ᴀ ᴘʟᴀɴ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ:",
        reply_markup=InlineKeyboardMarkup(price_buttons)
    )
    
async def inst_menu(client, message, group_id=None):
    user_id = message.from_user.id
    user_data = await db.get_user(user_id)
    current_time = datetime.now()

    # Sirf Insta ki expiry check karein (expiry_inst)
    expiry_inst = user_data.get("expiry_inst")
    if expiry_inst:
        if expiry_inst.tzinfo:
            expiry_inst = expiry_inst.replace(tzinfo=None)
            
        if expiry_inst > current_time:
            buttons = [[InlineKeyboardButton("📞 Cᴏɴᴛᴀᴄᴛ Mᴇ", url="https://t.me/premiumuseronly_Bot")]]
            return await message.reply_text(
                text="✨ <b>Aap pehle se hi VIP member hain!</b>\n\n<i>Apni details check karne ke liye /myplan use karein.</i>",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    price_buttons = []
    row = []
    for price in INSTAGRAM_PRICES:
        row.append(InlineKeyboardButton(f"💎 ₹{price}", callback_data=f"pay_inst_{price}"))
        if len(row) == 3:
            price_buttons.append(row)
            row = []
    if row: 
        price_buttons.append(row)
    price_buttons.append([InlineKeyboardButton("📞 Cᴏɴᴛᴀᴄᴛ Mᴇ", url="https://t.me/premiumuseronly_Bot")])
    
    await message.reply_text(
        text=f"📸 <b>Pʀᴇᴍɪᴜᴍ VIP Pʟᴀɴs</b>\n\nCʜᴏᴏsᴇ ʏᴏᴜʀ ᴘʟᴀɴ:",
        reply_markup=InlineKeyboardMarkup(price_buttons)
    )
    
