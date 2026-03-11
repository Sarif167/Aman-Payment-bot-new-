import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Message
)
from database.users_db import db
from info import ADMINS, LOG_CHANNEL
from utils import temp, get_readable_time, users_broadcast

lock = asyncio.Lock()

@Client.on_message(filters.command("msg") & filters.user(ADMINS))
async def send_private_message(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text(
            "⚠️ <b>Wʀᴏɴɢ Fᴏʀᴍᴀᴛ!</b>\n\n"
            "<b>Uꜱᴀɢᴇ:</b> <code>/msg [user_id] [ᴍᴇꜱꜱᴀɢᴇ]</code>\n"
            "<b>Exᴀᴍᴘʟᴇ:</b> <code>/msg 123456789 Yᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ɪꜱ ᴀᴄᴛɪᴠᴇ!</code>"
        )

    try:
        user_id = int(message.command[1])
        text = " ".join(message.command[2:]) 

        await client.send_message(chat_id=user_id, text=f"👨‍💻 <b>Aᴅᴍɪɴ Mᴇꜱꜱᴀɢᴇ:</b>\n\n{text}")
        
        await message.reply_text(
            f"✅ <b>Mᴇꜱꜱᴀɢᴇ Sᴇɴᴛ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!</b>\n\n"
            f"👤 <b>Tᴏ Uꜱᴇʀ:</b> <code>{user_id}</code>\n"
            f"📩 <b>Mᴇꜱꜱᴀɢᴇ:</b> {text}"
        )

        try:
            await client.send_message(LOG_CHANNEL, f"📩 <b>#Aᴅᴍɪɴ_DM</b>\n\n👮 <b>Bʏ:</b> {message.from_user.mention}\n👤 <b>Tᴏ:</b> <code>{user_id}</code>\n📝 <b>Mꜱɢ:</b> {text}")
        except Exception:
            pass

    except ValueError:
        await message.reply_text("❌ <b>Eʀʀᴏʀ:</b> Uꜱᴇʀ ID ᴍᴜꜱᴛ ʙᴇ ᴀ ɴᴜᴍʙᴇʀ!")
    except Exception as e:
        await message.reply_text(f"⚠️ <b>Mᴇꜱꜱᴀɢᴇ ꜱᴇɴᴅ ꜰᴀɪʟᴇᴅ!</b>\n<i>(Mᴀʏʙᴇ ᴛʜᴇ ᴜꜱᴇʀ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴏʀ ᴡʀᴏɴɢ ID)</i>\n\n<b>Eʀʀᴏʀ:</b> <code>{str(e)}</code>")

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_users(bot, message):
    if lock.locked():
        return await message.reply(
            "<b>⚠️ Bʀᴏᴀᴅᴄᴀꜱᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ!</b>\n\n"
            "<i>Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ɪᴛ ᴛᴏ ᴄᴏᴍᴘʟᴇᴛᴇ.</i>"
        )

    ask_pin = await message.reply(
        "<b>📌 Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘɪɴ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ?</b>",
        reply_markup=ReplyKeyboardMarkup(
            [['Yᴇꜱ', 'Nᴏ']], 
            one_time_keyboard=True, 
            resize_keyboard=True
        )
    )

    try:
        msg = await bot.listen(chat_id=message.chat.id, user_id=message.from_user.id, timeout=30)
    except asyncio.TimeoutError:
        await ask_pin.delete()
        return await message.reply("<b>⏰ Tɪᴍᴇᴏᴜᴛ! Bʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴀɴᴄᴇʟʟᴇᴅ.</b>")

    if msg.text == 'Yᴇꜱ':
        is_pin = True
    elif msg.text == 'Nᴏ':
        is_pin = False
    else:
        await ask_pin.delete()
        return await message.reply("<b>❌ Iɴᴠᴀʟɪᴅ ʀᴇꜱᴘᴏɴꜱᴇ!</b>")

    await ask_pin.delete()
    await msg.delete() 
    
    await bot.send_message(
        chat_id=message.chat.id, 
        text="<b>🚀 Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ...</b>", 
        reply_markup=ReplyKeyboardRemove()
    )

    users = await db.get_all_users()
    b_msg = message.reply_to_message
    
    b_sts = await message.reply_text("<b>⏳ Pʀᴏᴄᴇꜱꜱɪɴɢ Bʀᴏᴀᴅᴄᴀꜱᴛ...</b>")

    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    success = 0
    failed = 0

    async with lock:
        async for user in users:
            if temp.USERS_CANCEL:
                temp.USERS_CANCEL = False
                time_taken = get_readable_time(time.time() - start_time)
                await b_sts.edit(
                    f"<b>❌ Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴀɴᴄᴇʟʟᴇᴅ!</b>\n\n"
                    f"<b>⏱️ Tɪᴍᴇ:</b> {time_taken}\n"
                    f"<b>👥 Tᴏᴛᴀʟ:</b> <code>{total_users}</code>\n"
                    f"<b>✅ Sᴜᴄᴄᴇꜱꜱ:</b> <code>{success}</code>\n"
                    f"<b>❌ Fᴀɪʟᴇᴅ:</b> <code>{failed}</code>"
                )
                return

            success_flag, sts = await users_broadcast(int(user['id']), b_msg, is_pin)
            
            if sts == 'Success':
                success += 1
            else:
                failed += 1
            
            done += 1

            if done % 20 == 0:
                btn = [[InlineKeyboardButton('✖️ Cᴀɴᴄᴇʟ Bʀᴏᴀᴅᴄᴀꜱᴛ', callback_data='broadcast_cancel#users')]]
                await b_sts.edit(
                    f"<b>📢 Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ...</b>\n"
                    "➖➖➖➖➖➖➖➖➖➖➖\n"
                    f"<b>👥 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:</b> <code>{total_users}</code>\n"
                    f"<b>✅ Sᴜᴄᴄᴇꜱꜱ:</b> <code>{success}</code>\n"
                    f"<b>❌ Fᴀɪʟᴇᴅ:</b> <code>{failed}</code>\n"
                    f"<b>🔄 Cᴏᴍᴘʟᴇᴛᴇᴅ:</b> <code>{done}</code>\n"
                    "➖➖➖➖➖➖➖➖➖➖➖",
                    reply_markup=InlineKeyboardMarkup(btn)
                )

        time_taken = get_readable_time(time.time() - start_time)
        await b_sts.edit(
            f"<b>✅ Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ!</b>\n"
            "➖➖➖➖➖➖➖➖➖➖➖\n"
            f"<b>⏱️ Tɪᴍᴇ Tᴀᴋᴇɴ:</b> {time_taken}\n"
            f"<b>👥 Tᴏᴛᴀʟ Uꜱᴇʀꜱ:</b> <code>{total_users}</code>\n"
            f"<b>✅ Sᴜᴄᴄᴇꜱꜱ:</b> <code>{success}</code>\n"
            f"<b>❌ Fᴀɪʟᴇᴅ:</b> <code>{failed}</code>\n"
            "➖➖➖➖➖➖➖➖➖➖➖"
        )

@Client.on_callback_query(filters.regex(r'^broadcast_cancel'))
async def broadcast_cancel(bot, query):
    _, ident = query.data.split("#")
    if ident == 'users':
        await query.message.edit("<b>🛑 Sᴛᴏᴘᴘɪɴɢ Bʀᴏᴀᴅᴄᴀꜱᴛ...</b>")
        temp.USERS_CANCEL = True

