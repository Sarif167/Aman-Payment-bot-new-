import io, pytz
from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_seconds
from info import ADMINS, LOG_CHANNEL, CHANNEL_LINK_MOV, CHANNEL_LINK_INST
from database.users_db import db

# ==========================================
# ➕ ADD PREMIUM (CATEGORY SELECTION)
# ==========================================
@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def manual_add_premium(client: Client, message: Message):
    if len(message.command) != 3:
        return await message.reply_text(
            "⚠️ <b>ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ!</b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b> <code>/addpremium [ᴜsᴇʀ_ɪᴅ] [ᴛɪᴍᴇ]</code>\n"
            "<b>ᴇx. :</b> <code>/addpremium 12345 1month</code>"
        )
    
    user_id = message.command[1]
    time_str = message.command[2]

    # sᴇʟᴇᴄᴛ ᴄᴀᴛᴇɢᴏʀʏ ғɪʀsᴛ ᴛᴏ ᴜᴘᴅᴀᴛᴇ ᴄᴏʀʀᴇᴄᴛ ᴅʙ ғɪᴇʟᴅ
    btns = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 ᴍᴏᴠɪᴇ ᴘʀᴇᴍɪᴜᴍ", callback_data=f"addp_mov_{user_id}_{time_str}"),
            InlineKeyboardButton("📸 ɪɴsᴛᴀ ᴘʀᴇᴍɪᴜᴍ", callback_data=f"addp_inst_{user_id}_{time_str}")
        ],
        [InlineKeyboardButton("✖️ ᴄᴀɴᴄᴇʟ", callback_data="close_data")]
    ])

    await message.reply_text(
        f"👤 <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>\n"
        f"⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{time_str}</code>\n\n"
        f"❓ <b>ᴋᴀᴜɴsᴀ ᴘʟᴀɴ ᴀᴅᴅ ᴋᴀʀɴᴀ ʜᴀɪ? sᴇʟᴇᴄᴛ ᴋᴀʀᴇɪɴ:</b>",
        reply_markup=btns
    )

# ==========================================
# ➖ REMOVE PREMIUM (BOTH CATEGORIES)
# ==========================================
@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def manual_remove_premium(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ <b>ᴜsᴀɢᴇ:</b> <code>/removepremium [ᴜsᴇʀ_ɪᴅ]</code>")
    
    try:
        user_id = int(message.command[1])
        user_data = await db.get_user(user_id)
        
        if not user_data:
            return await message.reply_text("❌ <b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ!</b>")

        # ʀᴇᴍᴏᴠɪɴɢ ʙᴏᴛʜ ᴘʀᴇᴍɪᴜᴍs
        user_data["expiry_mov"] = None
        user_data["expiry_inst"] = None
        await db.update_user(user_data)

        for ch in [CHANNEL_LINK_MOV, CHANNEL_LINK_INST]:
            try:
                await client.ban_chat_member(ch, user_id)
                await client.unban_chat_member(ch, user_id)
            except: pass

        await message.reply_text(f"✅ <b>ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ғᴏʀ {user_id}</b>")
        try: await client.send_message(user_id, "⚠️ <b>ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ʙʏ ᴀᴅᴍɪɴ.</b>")
        except: pass

    except Exception as e:
        await message.reply_text(f"❌ <b>ᴇʀʀᴏʀ:</b> <code>{e}</code>")

# ==========================================
# 👑 PREMIUM USER LIST (ALL TYPES)
# ==========================================
@Client.on_message(filters.command("premium_user") & filters.user(ADMINS))
async def premium_users_list(client: Client, message: Message):
    msg = await message.reply_text("🔄 <b>ғᴇᴛᴄʜɪɴɢ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs...</b>")
    now = datetime.now()
    mov_list, inst_list = [], []
    
    users = await db.get_all_users()
    async for user in users:
        # ᴄʜᴇᴄᴋ ᴍᴏᴠɪᴇ ᴘʀᴇᴍɪᴜᴍ
        m_exp = user.get("expiry_mov")
        if m_exp and m_exp.replace(tzinfo=None) > now:
            mov_list.append(f"{user.get('name', 'ᴜɴᴋ')} [{user['id']}]")
            
        # ᴄʜᴇᴄᴋ ɪɴsᴛᴀ ᴘʀᴇᴍɪᴜᴍ
        i_exp = user.get("expiry_inst")
        if i_exp and i_exp.replace(tzinfo=None) > now:
            inst_list.append(f"{user.get('name', 'ᴜɴᴋ')} [{user['id']}]")

    if not mov_list and not inst_list:
        return await msg.edit_text("❌ <b>ɴᴏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ғᴏᴜɴᴅ.</b>")

    content = f"🏆 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ʀᴇᴘᴏʀᴛ 🏆\n{'='*30}\n\n"
    content += f"🎬 ᴍᴏᴠɪᴇ ᴘʀᴇᴍɪᴜᴍ ({len(mov_list)}):\n" + "\n".join(mov_list) + "\n\n"
    content += f"📸 ɪɴsᴛᴀ ᴘʀᴇᴍɪᴜᴍ ({len(inst_list)}):\n" + "\n".join(inst_list)

    with io.BytesIO(str.encode(content)) as out_file:
        out_file.name = "ᴘʀᴇᴍɪᴜᴍ_ᴜsᴇʀs.txt"
        await message.reply_document(
            document=out_file, 
            caption=f"👑 <b>ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ʟɪsᴛ</b>\n\n🎬 ᴍᴏᴠɪᴇ: <code>{len(mov_list)}</code>\n📸 ɪɴsᴛᴀ: <code>{len(inst_list)}</code>"
        )
        await msg.delete()


