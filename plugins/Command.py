import asyncio, pytz, random
from datetime import date, datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified, WebpageMediaEmpty
from database.users_db import db
from Script import script
from info import LOG_CHANNEL, START_PIC, CHANNEL_LINK, TRIAL_PIC
from utils import temp

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    mention = message.from_user.mention
    username = f"@{message.from_user.username}" if message.from_user.username else "ɴᴏɴᴇ"
    
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    time_str = now.strftime("%I:%M:%S %p")
    date_str = date.today().strftime("%d-%m-%Y")

    if not await db.is_user_exist(user_id):
        await db.add_user(user_id, first_name, username, date_str)
        await client.send_message(
            LOG_CHANNEL, 
            script.LOG_TEXT.format(temp.B_NAME, mention, user_id, username, time_str, date_str)
        )

    user_data = await db.get_user(user_id) or {}
    
    buttons = [
        [InlineKeyboardButton('✨ ᴠɪᴇᴡ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴘʟᴀɴs ✨', callback_data='subscription')]
    ]

    if not user_data.get("trial_claimed"):
        buttons.insert(0, [InlineKeyboardButton("🎁 ᴄʟᴀɪᴍ 1-ʜᴏᴜʀ ғʀᴇᴇ ᴛʀɪᴀʟ", callback_data="claim_trial")])

    buttons.append([
        InlineKeyboardButton("ℹ️ ʜᴇʟᴘ", callback_data="help"),
        InlineKeyboardButton("👨‍💻 ᴀʙᴏᴜᴛ", callback_data="about")
    ])     

    await message.reply_photo(
        photo=START_PIC,
        caption=script.START_TXT.format(mention, temp.B_LINK),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

async def process_trial(client: Client, message: Message, user_id: int, user_name: str, mention: str):
    user_data = await db.get_user(user_id) or {"id": user_id, "name": user_name}
    
    if user_data.get("trial_claimed"):
        return await message.reply_text(
            "❌ <b>ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ ғʀᴇᴇ ᴛʀɪᴀʟ!</b>\n\n"
            "<i>ᴘʟᴇᴀsᴇ ᴘᴜʀᴄʜᴀsᴇ ᴀ ᴘʀᴇᴍɪᴜᴍ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</i>",
            parse_mode=enums.ParseMode.HTML
        )
        
    current_time = datetime.now()
    current_expiry = user_data.get("expiry_time")
    
    if current_expiry and current_expiry.tzinfo:
        current_expiry = current_expiry.replace(tzinfo=None)

    if current_expiry and current_expiry > current_time:
        new_expiry = current_expiry + timedelta(hours=1)
    else:
        new_expiry = current_time + timedelta(hours=1)
    
    user_data["expiry_time"] = new_expiry
    user_data["trial_claimed"] = True
    await db.update_user(user_data)
    
    btn = None
    try:
        invite_link = await client.create_chat_invite_link(
            chat_id=CHANNEL_LINK,
            member_limit=1, 
            expire_date=current_time + timedelta(minutes=5)
        )
        link_url = invite_link.invite_link
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✨ ᴊᴏɪɴ ᴠɪᴘ ᴄʜᴀɴɴᴇʟ ✨", url=link_url)]])
    except Exception:
        pass
        
    success_caption = (
        f"🎉 <b>ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs!</b>\n\n"
        f"<b>ʏᴏᴜ ʜᴀᴠᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ 1-ʜᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴛʀɪᴀʟ!</b> 🚀\n"
        f"<i>ᴇɴᴊᴏʏ ᴀʟʟ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs ᴡɪᴛʜᴏᴜᴛ ʟɪᴍɪᴛs.</i>\n\n"
        f"👉 <i>ᴛʏᴘᴇ /myplan ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴛᴀᴛᴜs.</i>"
    )

    try:
        await message.reply_photo(
            photo=TRIAL_PIC,
            caption=success_caption,
            reply_markup=btn,
            parse_mode=enums.ParseMode.HTML
        )
    except WebpageMediaEmpty:
        # Agar photo link corrupt hai toh text message bhejega crash hone ki bajaye
        await message.reply_text(
            text=success_caption,
            reply_markup=btn,
            parse_mode=enums.ParseMode.HTML
        )
    
    await client.send_message(
        LOG_CHANNEL, 
        f"🆓 <b>#ᴛʀɪᴀʟ_ᴄʟᴀɪᴍᴇᴅ</b>\n\n👤 <b>ᴜsᴇʀ:</b> {mention} [<code>{user_id}</code>]\n⏱️ <b>ᴘʟᴀɴ:</b> <code>1-ʜᴏᴜʀ ғʀᴇᴇ ᴛʀɪᴀʟ</code>",
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("trial") & filters.private)
async def free_trial_command(client: Client, message: Message):
    await process_trial(client, message, message.from_user.id, message.from_user.first_name, message.from_user.mention)
    
