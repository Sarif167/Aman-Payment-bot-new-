from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS, MOVIE_CHANNEL, INSTA_CHANNEL

@Client.on_message(filters.command("inst_post") & filters.user(ADMINS))
async def inst_post_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>❌ ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ!</b>\n\n<code>/inst_post ɪᴍᴀɢᴇ_ʟɪɴᴋ, ᴅᴇᴛᴀɪʟs</code>")

    try:
        input_data = message.text.split(None, 1)[1]
        img_url, details = input_data.split(",", 1)

        btns = InlineKeyboardMarkup([[
            InlineKeyboardButton("📸 ɢᴇᴛ ɪɴsᴛᴀ ᴘʀᴇᴍɪᴜᴍ", url=f"https://t.me/{temp.U_NAME}?start=inst{INSTA_CHANNEL}")
        ]])

        await client.send_photo(
            chat_id=INSTA_CHANNEL,
            photo=img_url.strip(),
            caption=details.strip(),
            reply_markup=btns,
            parse_mode=enums.ParseMode.HTML
        )
        await message.reply_text("<b>✅ ᴘᴏsᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ɪɴ ɪɴsᴛᴀɢʀᴀᴍ ᴄʜᴀɴɴᴇʟ!</b>")
    except Exception as e:
        await message.reply_text(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>")

@Client.on_message(filters.command("Mov_post") & filters.user(ADMINS))
async def mov_post_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>❌ ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ!</b>\n\n<code>/Mov_post ɪᴍᴀɢᴇ_ʟɪɴᴋ, ᴅᴇᴛᴀɪʟs</code>")

    try:
        input_data = message.text.split(None, 1)[1]
        img_url, details = input_data.split(",", 1)

        btns = InlineKeyboardMarkup([[
            InlineKeyboardButton("🎬 ᴡᴀᴛᴄʜ ғᴜʟʟ ᴍᴏᴠɪᴇ", url=f"https://t.me/{temp.U_NAME}?start=movie{MOVIE_CHANNEL}")
        ]])

        await client.send_photo(
            chat_id=MOVIE_CHANNEL,
            photo=img_url.strip(),
            caption=details.strip(),
            reply_markup=btns,
            parse_mode=enums.ParseMode.HTML
        )
        await message.reply_text("<b>✅ ᴘᴏsᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ɪɴ ᴍᴏᴠɪᴇ ᴄʜᴀɴɴᴇʟ!</b>")
    except Exception as e:
        await message.reply_text(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>")
        
