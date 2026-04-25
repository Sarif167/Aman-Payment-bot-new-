import asyncio, random, pytz
from datetime import datetime, timedelta
from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.users_db import db  
from Script import script
from info import (
    CHANNEL, SUPPORT, LOG_CHANNEL, SCREENSHOT, 
    CHANNEL_LINK_MOV, CHANNEL_LINK_INST, CLAIM_REWARD_PIC, 
    DECLINED_PIC, SUCCESSFULLY_PIC
)
from utils import (
    temp, MOVIE_PRICES1, INSTAGRAM_PRICES1, MOVIE_PRICES2, 
    INSTAGRAM_PRICES2, UPI_ID, NAME, generate_qr, 
    get_seconds, payment_timer_task
)

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "close_data":
        await query.message.delete()

    elif data == "about":
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME, temp.B_NAME),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start')]]),
            parse_mode=enums.ParseMode.HTML
        )
    
    elif data == "start":
        buttons = [
            [InlineKeyboardButton("ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ", url=CHANNEL)],
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"), InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")]
        ]
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.B_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
        
    elif data == "help":
        buttons = [
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/"), InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/")],
            [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start')]
        ]
        await query.message.edit_text(
            text=script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

    elif data.startswith("pay_mov_") or data.startswith("pay_inst_"):
        splited = data.split("_")
        pay_type = splited[1]
        amount = int(splited[2])
        
        mapping = MOVIE_PRICES1 if pay_type == "mov" else INSTAGRAM_PRICES1
        pay_name = "ᴍᴏᴠɪᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ" if pay_type == "mov" else "ɪɴsᴛᴀ/ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ"

        state_data = await db.get_payment_state(user_id)
        if state_data:
            return await query.answer("ᴘʟᴇᴀsᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ʏᴏᴜʀ ᴘᴇɴᴅɪɴɢ ᴘᴀʏᴍᴇɴᴛ ғɪʀsᴛ!", show_alert=True)

        if amount not in mapping:
            return await query.answer("ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ!", show_alert=True)

        duration = mapping[amount]
        await query.answer("ɢᴇɴᴇʀᴀᴛɪɴɢ ǫʀ ᴄᴏᴅᴇ...", show_alert=False)

        upi_link = f"upi://pay?pa={UPI_ID}&pn={NAME}&am={amount}&cu=INR&tr={user_id}&tn=ᴘᴀʏ_{user_id}_{amount}"
        qr_image = generate_qr(upi_link)
        await query.message.delete()

        sent_photo = await client.send_photo(
            chat_id=query.message.chat.id,
            photo=qr_image,  
            caption=script.SCAN_TXT.format(amount, pay_name, duration),
            parse_mode=enums.ParseMode.HTML 
        )
        sent_text = await client.send_message(
            chat_id=query.message.chat.id,
            text="Abhi payment ka screenshot bhejein ya /cancel use karein",
            parse_mode=enums.ParseMode.HTML
        )

        log_text = f"🔔 ǫʀ ɢᴇɴᴇʀᴀᴛᴇᴅ\n\nᴜsᴇʀ: {query.from_user.mention}\nᴛʏᴘᴇ: {pay_name}\nᴀᴍᴏᴜɴᴛ: ₹{amount}"
        await client.send_message(LOG_CHANNEL, text=log_text)

        await db.set_payment_state(user_id, {
            "amount": amount, "premium_duration": duration,
            "photo_id": sent_photo.id, "text_id": sent_text.id, "pay_type": pay_type
        })
        asyncio.create_task(payment_timer_task(client, user_id, query.message.chat.id, amount, pay_type, sent_photo.id, sent_text.id))

    elif data.startswith("approve_"):
        _, target_id, amount, pay_type = data.split("_")
        target_id, amount = int(target_id), int(amount)
        
        await query.answer("ᴀᴘᴘʀᴏᴠɪɴɢ...", show_alert=False)
        
        if pay_type == "mov":
            mapping, target_chat, cat_name, expiry_key = MOVIE_PRICES2, CHANNEL_LINK_MOV, "ᴍᴏᴠɪᴇ", "expiry_mov"
        else:
            mapping, target_chat, cat_name, expiry_key = INSTAGRAM_PRICES2, CHANNEL_LINK_INST, "ɪɴsᴛᴀ/ᴠɪᴘ", "expiry_inst"

        duration = mapping.get(amount, "1day")
        seconds = get_seconds(duration)
        
        try:
            user = await client.get_users(target_id)
            mention = user.mention
        except: mention = f"ᴜsᴇʀ {target_id}"
            
        now = datetime.now()
        user_data = await db.get_user(target_id) or {"id": target_id}
        curr_exp = user_data.get(expiry_key)
        
        if curr_exp and curr_exp.tzinfo: curr_exp = curr_exp.replace(tzinfo=None)
        new_exp = (curr_exp if curr_exp and curr_exp > now else now) + timedelta(seconds=seconds)
            
        user_data[expiry_key] = new_expiry = new_exp
        await db.update_user(user_data) 
        
        exp_str = new_expiry.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M %p")
        
        reward_points = 0
        if 1 <= amount <= 20: reward_points = random.randint(1, 8)
        elif 21 <= amount <= 50: reward_points = random.randint(5, 10)
        elif 51 <= amount <= 100: reward_points = random.randint(10, 15)
        elif 101 <= amount <= 200: reward_points = random.randint(15, 30)
        elif 201 <= amount <= 500: reward_points = random.randint(30, 80)
        elif amount > 500: reward_points = random.randint(80, 120)

        if reward_points > 0:
            await db.rewards.update_one({"user_id": target_id}, {"$inc": {"coins": reward_points}}, upsert=True)

        try:
            link = await client.create_chat_invite_link(chat_id=target_chat, member_limit=1, expire_date=now + timedelta(minutes=10))
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(f"ᴊᴏɪɴ {cat_name}", url=link.invite_link)]])
            
            cap = f"🎉 ᴘᴀʏᴍᴇɴᴛ ᴀᴘᴘʀᴏᴠᴇᴅ!\n\nᴀᴍᴏᴜɴᴛ: ₹{amount}\nᴄᴀᴛᴇɢᴏʀʏ: {cat_name}\nᴇxᴘɪʀʏ: {exp_str}\n\n🎁 ʀᴇᴡᴀʀᴅ: {reward_points} ᴘᴏɪɴᴛs"
            await client.send_photo(chat_id=target_id, photo=SUCCESSFULLY_PIC, caption=cap, reply_markup=btn)
        except: pass 

        await query.message.edit_caption(caption=query.message.caption + f"\n\n✅ ᴀᴘᴘʀᴏᴠᴇᴅ | ₹{amount} | ʀᴇᴡᴀʀᴅ: {reward_points}", reply_markup=None)

    elif data.startswith("reject_"):
        _, target_id, amount = data.split("_")
        await query.answer("ʀᴇᴊᴇᴄᴛᴇᴅ!", show_alert=True)
        
        cap = f"❌ ᴘᴀʏᴍᴇɴᴛ ʀᴇᴊᴇᴄᴛᴇᴅ!\n\nᴀᴍᴏᴜɴᴛ: ₹{amount}\nʀᴇᴀsᴏɴ: sᴄʀᴇᴇɴsʜᴏᴛ ɴᴏᴛ ᴠᴀʟɪᴅ"
        try: await client.send_photo(chat_id=int(target_id), photo=DECLINED_PIC, caption=cap)
        except: pass
        await query.message.edit_caption(caption=query.message.caption + "\n\n❌ ʀᴇᴊᴇᴄᴛᴇᴅ", reply_markup=None)

    elif data.startswith("claim_") and not any(x in data for x in ["_mov", "_inst"]):
        t_id = data.split("_")[1]
        btns = [[InlineKeyboardButton("ᴍᴏᴠɪᴇ ᴠɪᴘ", callback_data=f"claim_mov_{t_id}"), InlineKeyboardButton("ɪɴsᴛᴀ ᴠɪᴘ", callback_data=f"claim_inst_{t_id}")]]
        await query.message.edit_text("sᴇʟᴇᴄᴛ ᴄᴀᴛᴇɢᴏʀʏ ᴛᴏ ᴄʟᴀɪᴍ ʀᴇᴡᴀʀᴅ:", reply_markup=InlineKeyboardMarkup(btns))
            
    elif data.startswith("claim_mov_") or data.startswith("claim_inst_"):
        _, p_type, t_id = data.split("_")
        t_id = int(t_id)
        if user_id != t_id: return await query.answer("ɴᴏᴛ ʏᴏᴜʀ ʀᴇᴡᴀʀᴅ!", show_alert=True)

        user_p = await db.get_user(t_id) or {"id": t_id}
        exp_key = "expiry_mov" if p_type == "mov" else "expiry_inst"
        
        now = datetime.now()
        curr_exp = user_p.get(exp_key)
        if curr_exp and curr_exp.replace(tzinfo=None) > now:
            return await query.answer("ʏᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴘʀᴇᴍɪᴜᴍ!", show_alert=True)

        reward_db = await db.rewards.find_one({"user_id": t_id})
        coins = reward_db.get("coins", 0) if reward_db else 0
        
        tiers = [{"c": 180, "h": 48}, {"c": 150, "h": 24}, {"c": 110, "h": 12}, {"c": 60, "h": 6}, {"c": 50, "h": 2}]
        tier = next((x for x in tiers if coins >= x["c"]), None)
        
        if not tier: return await query.answer("ɴᴇᴇᴅ 50 ᴘᴏɪɴᴛs!", show_alert=True)

        await db.rewards.update_one({"user_id": t_id}, {"$inc": {"coins": -tier["c"]}})
        user_p[exp_key] = now + timedelta(hours=tier["h"])
        await db.update_user(user_p)

        target_ch = CHANNEL_LINK_MOV if p_type == "mov" else CHANNEL_LINK_INST
        try:
            link = await client.create_chat_invite_link(chat_id=target_ch, member_limit=1, expire_date=now + timedelta(minutes=10))
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=link.invite_link)]])
            await client.send_photo(chat_id=t_id, photo=CLAIM_REWARD_PIC, caption="🎁 ʀᴇᴡᴀʀᴅ ᴄʟᴀɪᴍᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!", reply_markup=btn)
            await query.message.delete()
        except: pass

    elif data.startswith("sendlink_"):
        _, p_type, t_id, t_str = data.split("_")
        t_id = int(t_id)
        target_ch = CHANNEL_LINK_MOV if p_type == "mov" else CHANNEL_LINK_INST
        
        try:
            link = await client.create_chat_invite_link(chat_id=target_ch, member_limit=1, expire_date=datetime.now() + timedelta(minutes=10))
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("ᴊᴏɪɴ ᴠɪᴘ", url=link.invite_link)]])
            await client.send_message(chat_id=t_id, text=f"🎉 ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ {t_str}!", reply_markup=btn)
            await query.message.edit_text("✅ ʟɪɴᴋ sᴇɴᴛ ᴛᴏ ᴜsᴇʀ!")
        except: await query.message.edit_text("❌ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ʟɪɴᴋ!")
            
