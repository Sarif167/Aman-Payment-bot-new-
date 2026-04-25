import io, pytz
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from info import ADMINS
from database.users_db import db

# ==========================================
# 💳 GLOBAL PAYMENTS DASHBOARD
# ==========================================
@Client.on_message(filters.command("payments") & filters.user(ADMINS))
async def check_payments_cmd(client: Client, message: Message):
    msg = await message.reply_text("🔄 <b>ғᴇᴛᴄʜɪɴɢ ᴘᴀʏᴍᴇɴᴛ ᴅᴀᴛᴀ...</b>")
    
    try:
        cursor = db.payments.find({})
        user_payments = {}
        user_names = {}
        total_revenue = 0
        total_tx = 0
        
        async for pay in cursor:
            uid = pay.get("user_id")
            amt = int(pay.get("amount", 0))
            name = pay.get("name", f"ᴜsᴇʀ {uid}")
            
            if uid:
                user_payments[uid] = user_payments.get(uid, 0) + amt
                user_names[uid] = name
                total_revenue += amt
                total_tx += 1
                
        if not user_payments:
            return await msg.edit_text("❌ <b>ɴᴏ ᴘᴀʏᴍᴇɴᴛ ʀᴇᴄᴏʀᴅs ғᴏᴜɴᴅ.</b>")
            
        pay_data = [{"id": uid, "name": user_names[uid], "spent": amt} for uid, amt in user_payments.items()]
        pay_data.sort(key=lambda x: x["spent"], reverse=True)
        
        header = (
            f"💳 <b>ᴘᴀʏᴍᴇɴᴛs ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
        )
        footer = (
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📊 <b>ᴛᴏᴛᴀʟ ᴛxɴ:</b> <code>{total_tx}</code>\n"
            f"💸 <b>ᴛᴏᴛᴀʟ ʀᴇᴠᴇɴᴜᴇ:</b> <code>₹{total_revenue}</code>"
        )

        if len(pay_data) <= 15:
            text = header
            for u in pay_data:
                text += f"👤 {u['name']}\n🆔 <code>{u['id']}</code> | 💰 <b>₹{u['spent']}</b>\n\n"
            await msg.edit_text(text + footer)
            
        else:
            file_content = f"ɢʟᴏʙᴀʟ ᴘᴀʏᴍᴇɴᴛs ʀᴇᴘᴏʀᴛ\nɢᴇɴᴇʀᴀᴛᴇᴅ: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n"
            file_content += f"ᴛᴏᴛᴀʟ ʀᴇᴠᴇɴᴜᴇ: ʀs {total_revenue} | ᴛᴏᴛᴀʟ ᴛxɴ: {total_tx}\n"
            file_content += "="*50 + "\n\n"
            
            for i, u in enumerate(pay_data, 1):
                raw_name = u['name'].replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
                file_content += f"{i}. {raw_name} [{u['id']}] - ʀs {u['spent']}\n"
                
            with io.BytesIO(str.encode(file_content)) as out_file:
                out_file.name = "ᴘᴀʏᴍᴇɴᴛs_ʀᴇᴘᴏʀᴛ.txt"
                await message.reply_document(
                    document=out_file, 
                    caption=f"💳 <b>ᴘᴀʏᴍᴇɴᴛs ᴅᴀsʜʙᴏᴀʀᴅ</b>\n\n{footer}"
                )
            await msg.delete()
            
    except Exception as e:
        await msg.edit_text(f"❌ <b>ᴇʀʀᴏʀ:</b> <code>{e}</code>")

# ==========================================
# 🔍 DETAILED USER INSPECTOR
# ==========================================
@Client.on_message(filters.command("check_user") & filters.user(ADMINS))
async def check_user_cmd(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ <b>ᴜsᴀɢᴇ:</b> <code>/check_user [ᴜsᴇʀ_ɪᴅ]</code>")
    
    try:
        user_id = int(message.command[1])
    except:
        return await message.reply_text("❌ <b>ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ.</b>")
        
    msg = await message.reply_text("🔄 <b>sᴇᴀʀᴄʜɪɴɢ ᴅᴀᴛᴀʙᴀsᴇ...</b>")
    
    try:
        user_data = await db.get_user(user_id)
        if not user_data:
            return await msg.edit_text(f"❌ <b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴅʙ.</b>")
            
        reward_data = await db.rewards.find_one({"user_id": user_id})
        coins = reward_data.get("coins", 0) if reward_data else 0

        # ᴛᴏᴛᴀʟ sᴘᴇɴᴛ ᴄᴀʟᴄᴜʟᴀᴛɪᴏɴ
        pipeline = [{"$match": {"user_id": user_id}}, {"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
        pay_result = await db.payments.aggregate(pipeline).to_list(1)
        total_paid = pay_result[0]["total"] if pay_result else 0
        
        # ᴇxᴘɪʀʏ ᴄʜᴇᴄᴋs ғᴏʀ ʙᴏᴛʜ ᴛʏᴘᴇs
        now = datetime.now()
        tz = pytz.timezone("Asia/Kolkata")

        def get_status(key):
            exp = user_data.get(key)
            if exp:
                if exp.tzinfo: exp = exp.replace(tzinfo=None)
                if exp > now:
                    return f"✅ <b>ᴀᴄᴛɪᴠᴇ</b> (<code>{exp.replace(tzinfo=pytz.utc).astimezone(tz).strftime('%d %b, %I:%M %p')}</code>)"
            return "❌ <b>ɪɴᴀᴄᴛɪᴠᴇ</b>"

        mov_status = get_status("expiry_mov")
        inst_status = get_status("expiry_inst")
        
        text = (
            f"👤 <b>ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 <b>ɴᴀᴍᴇ:</b> {user_data.get('name', 'ᴜɴᴋɴᴏᴡɴ')}\n"
            f"🔹 <b>ɪᴅ:</b> <code>{user_id}</code>\n"
            f"📅 <b>ᴊᴏɪɴᴇᴅ:</b> <code>{user_data.get('joined_date', 'ᴜɴᴋɴᴏᴡɴ')}</code>\n\n"
            f"🎬 <b>ᴍᴏᴠɪᴇ ᴠɪᴘ:</b> {mov_status}\n"
            f"📸 <b>ɪɴsᴛᴀ ᴠɪᴘ:</b> {inst_status}\n\n"
            f"💰 <b>ᴛᴏᴛᴀʟ ᴘᴀɪᴅ:</b> <code>₹{total_paid}</code>\n"
            f"🎁 <b>ʀᴇᴡᴀʀᴅ ᴘᴏɪɴᴛs:</b> <code>{coins}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        await msg.edit_text(text)
        
    except Exception as e:
        await msg.edit_text(f"❌ <b>ᴇʀʀᴏʀ:</b> <code>{e}</code>")
        
