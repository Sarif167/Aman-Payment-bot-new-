import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from info import ADMINS

@Client.on_message(filters.command("owner_cmd") & filters.private & filters.user(ADMINS))
async def admin_cmd(client, message):
    buttons = [
        [KeyboardButton("/stats"), KeyboardButton("/payments")],
        [KeyboardButton("/check_user"), KeyboardButton("/premium_user")],
        [KeyboardButton("/addpremium"), KeyboardButton("/removepremium")],
        [KeyboardButton("/code"), KeyboardButton("/allcodes")],
        [KeyboardButton("/delete_redeem"), KeyboardButton("/clearcodes")],
        [KeyboardButton("/broadcast"), KeyboardButton("/msg")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard=buttons, 
        resize_keyboard=True, 
        one_time_keyboard=False 
    )
    
    msg = await message.reply_text(
        "🛠️ <b>Aᴅᴍɪɴ Cᴏɴᴛʀᴏʟ Pᴀɴᴇʟ</b> 🛠️\n\n"
        "<i>Aʟʟ ᴀᴄᴛɪᴠᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀʀᴇ ꜱᴇᴛ ʜᴇʀᴇ. Cʟɪᴄᴋ ᴀɴʏ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ 👇\n\n"
        "⚠️ Tʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ɪɴ 2 ᴍɪɴᴜᴛᴇꜱ.</i>",
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )
    
    await asyncio.sleep(120)
    
    try:
        await msg.delete()
    except Exception:
        pass
        
