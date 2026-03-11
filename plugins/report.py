from pyrogram import Client, filters
from pyrogram.types import Message
from info import LOG_CHANNEL

@Client.on_message(filters.command("report") & filters.private)
async def user_report_command(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ <b>Uꜱᴀɢᴇ:</b> <code>/report [ᴍᴇꜱꜱᴀɢᴇ]</code>\n\n"
            "<b>Exᴀᴍᴘʟᴇ:</b> <code>/report Fɪʟᴇ ɪꜱ ɴᴏᴛ ᴏᴘᴇɴɪɴɢ.</code>"
        )
    
    report_text = message.text.split(None, 1)[1]
    user = message.from_user
    username = f"@{user.username}" if user.username else "Nᴏɴᴇ"
    
    admin_msg = (
        f"🚨 <b>#Nᴇᴡ_Rᴇᴘᴏʀᴛ</b> 🚨\n\n"
        f"👤 <b>Uꜱᴇʀ:</b> {user.mention}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
        f"📌 <b>Uꜱᴇʀɴᴀᴍᴇ:</b> {username}\n\n"
        f"📝 <b>Rᴇᴘᴏʀᴛ Mᴇꜱꜱᴀɢᴇ:</b>\n{report_text}\n\n"
        f"💡 <i>Uꜱᴇ <code>/check_user {user.id}</code> ꜰᴏʀ ᴅᴇᴛᴀɪʟꜱ.</i>"
    )
    
    try:
        await client.send_message(chat_id=LOG_CHANNEL, text=admin_msg)
        await message.reply_text(
            "✅ <b>Yᴏᴜʀ ʀᴇᴘᴏʀᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴛ ᴛᴏ ᴛʜᴇ ᴀᴅᴍɪɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!</b>\n"
            "<i>Wᴇ ᴡɪʟʟ ʀᴇᴠɪᴇᴡ ɪᴛ ꜱᴏᴏɴ. Tʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ʀᴇᴘᴏʀᴛɪɴɢ. ❤️</i>"
        )
    except Exception as e:
        await message.reply_text(f"❌ <b>Eʀʀᴏʀ:</b> <code>{e}</code>")
        
