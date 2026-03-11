from datetime import datetime
import pytz
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db

@Client.on_message(filters.command(["myplan", "profile"]) & filters.private)
async def user_profile_plan(client: Client, message: Message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    
    msg = await message.reply_text("🔄 <b>Fᴇᴛᴄʜɪɴɢ Yᴏᴜʀ Pʀᴏꜰɪʟᴇ...</b>", parse_mode=enums.ParseMode.HTML)
    
    user_data = await db.get_user(user_id)
    
    if not user_data:
        text = (
            f"👤 <b>Uꜱᴇʀ Pʀᴏꜰɪʟᴇ</b> 👤\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 <b>Nᴀᴍᴇ:</b> {mention}\n"
            f"🔹 <b>Uꜱᴇʀ ID:</b> <code>{user_id}</code>\n\n"
            f"📦 <b>Cᴜʀʀᴇɴᴛ Pʟᴀɴ:</b> <code>Fʀᴇᴇ Uꜱᴇʀ</code>\n"
            f"╰ ❌ Nᴏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        buttons = [[InlineKeyboardButton("✨ Vɪᴇᴡ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Pʟᴀɴꜱ ✨", callback_data="subscription")]]
        return await msg.edit_text(
            text=text, 
            reply_markup=InlineKeyboardMarkup(buttons), 
            parse_mode=enums.ParseMode.HTML
        )

    # Timezone set karein
    tz = pytz.timezone("Asia/Kolkata")
    
    # Current time directly IST mein get karein comparison ke liye
    current_time = datetime.now(tz)
    
    normal_expiry = user_data.get("expiry_time")
    buttons = []

    if normal_expiry:
        # Agar database se time bina timezone (naive) aa raha hai, toh use UTC maane
        if normal_expiry.tzinfo is None:
            normal_expiry = pytz.utc.localize(normal_expiry)
            
        # Ab UTC time ko safely IST (Asia/Kolkata) mein convert karein
        expiry_ist = normal_expiry.astimezone(tz)
        
        # IST to IST compare karein
        if expiry_ist > current_time:
            # Aapka bataya hua custom format yahan use ho raha hai
            normal_date = expiry_ist.strftime("%d-%m-%Y ᴀᴛ %I:%M:%S %p")

            plan_details = (
                f"👑 <b>Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ:</b>\n"
                f"╰ ✅ <b>Aᴄᴛɪᴠᴇ</b>\n\n"
                f"💰 <b>Pʀɪᴄᴇ:</b> <code>Pᴀɪᴅ</code>\n"
                f"⏳ <b>Dᴜʀᴀᴛɪᴏɴ:</b> <code>Pʀᴇᴍɪᴜᴍ Aᴄᴄᴇꜱꜱ</code>\n"
                f"⏰ <b>Eɴᴅ Tɪᴍᴇ:</b> <code>{normal_date}</code>\n\n"
            )
        else:
            plan_details = (
                f"📦 <b>Cᴜʀʀᴇɴᴛ Pʟᴀɴ:</b> <code>Fʀᴇᴇ Uꜱᴇʀ</code>\n"
                f"╰ ❌ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Exᴘɪʀᴇᴅ.\n\n"
            )
            buttons.append([InlineKeyboardButton("✨ Rᴇɴᴇᴡ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ✨", callback_data="subscription")])
    else:
        plan_details = (
            f"📦 <b>Cᴜʀʀᴇɴᴛ Pʟᴀɴ:</b> <code>Fʀᴇᴇ Uꜱᴇʀ</code>\n"
            f"╰ ❌ Nᴏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ.\n\n"
        )
        buttons.append([InlineKeyboardButton("✨ Vɪᴇᴡ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Pʟᴀɴꜱ ✨", callback_data="subscription")])

    profile_text = (
        f"👤 <b>Uꜱᴇʀ Pʀᴏꜰɪʟᴇ & Pʟᴀɴꜱ</b> 👤\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🔹 <b>Nᴀᴍᴇ:</b> {mention}\n"
        f"🔹 <b>Uꜱᴇʀ ID:</b> <code>{user_id}</code>\n\n"
        f"{plan_details}"
        f"━━━━━━━━━━━━━━━━━━━"
    )
    
    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None
    
    await msg.edit_text(
        text=profile_text, 
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML
    )
    
