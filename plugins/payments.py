from datetime import datetime
import pytz, io
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from info import ADMINS
from database.users_db import db

@Client.on_message(filters.command("payments") & filters.user(ADMINS))
async def check_payments_cmd(client: Client, message: Message):
    msg = await message.reply_text("🔄 <b>Fᴇᴛᴄʜɪɴɢ Nᴀᴍᴇ & Pᴀʏᴍᴇɴᴛ Lɪꜱᴛ...</b>", parse_mode=enums.ParseMode.HTML)
    
    try:
        cursor = db.payments.find({})
        user_payments = {}
        user_names = {}
        total_revenue = 0
        total_tx = 0
        
        async for pay in cursor:
            uid = pay.get("user_id")
            amt = int(pay.get("amount", 0))
            name = pay.get("name", f"Uꜱᴇʀ <code>{uid}</code>")
            
            if uid:
                user_payments[uid] = user_payments.get(uid, 0) + amt
                user_names[uid] = name
                total_revenue += amt
                total_tx += 1
                
        if not user_payments:
            return await msg.edit_text("❌ <b>Nᴏ ᴘᴀʏᴍᴇɴᴛ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ.</b>", parse_mode=enums.ParseMode.HTML)
            
        pay_data = [{"id": uid, "name": user_names[uid], "spent": amt} for uid, amt in user_payments.items()]
        pay_data.sort(key=lambda x: x["spent"], reverse=True)
        
        if len(pay_data) <= 15:
            text = (
                f"💳 <b>Pᴀʏᴍᴇɴᴛꜱ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ</b> 💳\n"
                f"━━━━━━━━━━━━━━━━━━━\n\n"
            )
            for u in pay_data:
                text += f"👤 {u['name']} [<code>{u['id']}</code>]\n💰 <b>Tᴏᴛᴀʟ Pᴀɪᴅ:</b> <code>₹{u['spent']}</code>\n\n"
                
            text += (
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"📊 <b>Tᴏᴛᴀʟ Tʀᴀɴꜱᴀᴄᴛɪᴏɴꜱ:</b> <code>{total_tx}</code>\n"
                f"💸 <b>Tᴏᴛᴀʟ Rᴇᴠᴇɴᴜᴇ:</b> <code>₹{total_revenue}</code>"
            )
            await msg.edit_text(text, parse_mode=enums.ParseMode.HTML)
            
        else:
            file_content = f"Global Payments Report\nGenerated on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n"
            file_content += f"Total Revenue: Rs {total_revenue} | Total Transactions: {total_tx}\n"
            file_content += "="*50 + "\n\n"
            
            for i, u in enumerate(pay_data, 1):
                raw_name = u['name'].replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '')
                file_content += f"{i}. Name: {raw_name}\n   ID: {u['id']}\n   Total Paid: Rs {u['spent']}\n"
                file_content += "-"*30 + "\n"
                
            with io.BytesIO(str.encode(file_content)) as out_file:
                out_file.name = "Payments_List.txt"
                await message.reply_document(
                    document=out_file, 
                    caption=(
                        f"💳 <b>Pᴀʏᴍᴇɴᴛꜱ Dᴀꜱʜʙᴏᴀʀᴅ</b> 💳\n\n"
                        f"📊 <b>Tᴏᴛᴀʟ Tʀᴀɴꜱᴀᴄᴛɪᴏɴꜱ:</b> <code>{total_tx}</code>\n"
                        f"💸 <b>Tᴏᴛᴀʟ Rᴇᴠᴇɴᴜᴇ:</b> <code>₹{total_revenue}</code>\n\n"
                        f"📄 <i>Fᴜʟʟ ɴᴀᴍᴇ & ᴘᴀʏᴍᴇɴᴛ ʟɪꜱᴛ ɪꜱ ɪɴ ᴛʜᴇ ꜰɪʟᴇ ᴀᴛᴛᴀᴄʜᴇᴅ.</i>"
                    ),
                    parse_mode=enums.ParseMode.HTML
                )
            await msg.delete()
            
    except Exception as e:
        await msg.edit_text(f"❌ <b>Eʀʀᴏʀ:</b> <code>{e}</code>", parse_mode=enums.ParseMode.HTML)
        

@Client.on_message(filters.command("check_user") & filters.user(ADMINS))
async def check_user_cmd(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ <b>Uꜱᴀɢᴇ:</b> <code>/check_user [user_id]</code>")
    
    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("❌ <b>Uꜱᴇʀ ID ᴍᴜꜱᴛ ʙᴇ ᴀ ɴᴜᴍʙᴇʀ.</b>")
        
    msg = await message.reply_text("🔄 <b>Sᴇᴀʀᴄʜɪɴɢ Dᴀᴛᴀʙᴀꜱᴇ...</b>")
    
    try:
        user_data = await db.get_user(user_id)
        if not user_data:
            return await msg.edit_text(f"❌ <b>Uꜱᴇʀ <code>{user_id}</code> Nᴏᴛ Fᴏᴜɴᴅ.</b>")
            
        reward_data = await db.rewards.find_one({"user_id": user_id})
        coins = reward_data.get("coins", 0) if reward_data else 0

        pipeline = [
            {"$match": {"user_id": user_id}}, 
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        pay_result = await db.payments.aggregate(pipeline).to_list(1)
        user_total_paid = pay_result[0]["total"] if pay_result else 0
        
        name = user_data.get("name", "Uɴᴋɴᴏᴡɴ")
        username = f"@{user_data['username']}" if user_data.get("username") else "Nᴏɴᴇ"
        joined_date = user_data.get("joined_date", "Uɴᴋɴᴏᴡɴ")
        
        current_time = datetime.now()
        tz = pytz.timezone("Asia/Kolkata")
        
        expiry = user_data.get("expiry_time")
        if expiry and expiry.tzinfo:
            expiry = expiry.replace(tzinfo=None)
            
        if expiry and expiry > current_time:
            status = "✅ <b>Aᴄᴛɪᴠᴇ</b>"
            try:
                localized_expiry = tz.localize(expiry)
                expiry_str = localized_expiry.strftime("%d %b %Y, %I:%M %p")
            except ValueError:
                expiry_str = expiry.strftime("%d %b %Y, %I:%M %p")
        else:
            status = "❌ <b>Iɴᴀᴄᴛɪᴠᴇ (Fʀᴇᴇ Uꜱᴇʀ)</b>"
            expiry_str = "N/A"
            
        text = (
            f"👤 <b>Uꜱᴇʀ Iɴꜰᴏʀᴍᴀᴛɪᴏɴ</b> 👤\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 <b>Nᴀᴍᴇ:</b> {name}\n"
            f"🔹 <b>Uꜱᴇʀɴᴀᴍᴇ:</b> {username}\n"
            f"🔹 <b>Uꜱᴇʀ ID:</b> <code>{user_id}</code>\n"
            f"📅 <b>Jᴏɪɴᴇᴅ Oɴ:</b> <code>{joined_date}</code>\n\n"
            f"👑 <b>Pʀᴇᴍɪᴜᴍ Sᴛᴀᴛᴜꜱ:</b> {status}\n"
            f"⏳ <b>Exᴘɪʀʏ Dᴀᴛᴇ:</b> <code>{expiry_str}</code>\n\n"
            f"💰 <b>Tᴏᴛᴀʟ Aᴍᴏᴜɴᴛ Pᴀɪᴅ:</b> <code>₹{user_total_paid}</code>\n"
            f"🎁 <b>Rᴇᴡᴀʀᴅ Pᴏɪɴᴛꜱ:</b> <code>{coins}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
        
        await msg.edit_text(text)
        
    except Exception as e:
        await msg.edit_text(f"❌ <b>Eʀʀᴏʀ:</b> <code>{e}</code>")
        
