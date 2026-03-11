import re
import asyncio
import random  
from datetime import datetime, timedelta
import pytz
from pyrogram import Client, enums, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from plugins.Command import process_trial
from database.users_db import db  
from Script import script
from info import CHANNEL, SUPPORT, TRIAL_PIC, LOG_CHANNEL, SCREENSHOT, CHANNEL_LINK, CLAIM_REWARD_PIC, DECLINED_PIC, SUCCESSFULLY_PIC
from utils import (
    temp, 
    FIXED_PRICES, 
    FIXED_PRICES2,
    FIXED_PRICES3, 
    UPI_ID, 
    NAME, 
    CURRENCY, 
    generate_qr,
    get_seconds,
    get_time_str,
    payment_timer_task
)

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "close_data":
        await query.message.delete()

    elif data == "about":
        buttons = [[InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start'),
                    InlineKeyboardButton('✖️ ᴄʟᴏsᴇ', callback_data='close_data')]]
        
        caption_text = script.ABOUT_TXT.format(temp.B_NAME, temp.B_NAME)
        
        if query.message.photo:
            await query.message.edit_caption(
                caption=caption_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.edit_text(
                text=caption_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
    
    elif data == "start":
        state_data = await db.get_payment_state(user_id)
        if state_data:
            try:
                await client.delete_messages(
                    chat_id=query.message.chat.id, 
                    message_ids=[state_data["photo_id"], state_data["text_id"]]
                )
            except:
                pass
            await db.del_payment_state(user_id)

        user_data = await db.get_user(user_id) or {}

        buttons = [
            
            [InlineKeyboardButton('✨ ✨ ᴠɪᴇᴡ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴘʟᴀɴs ✨ ✨', callback_data='subscription')],
            [InlineKeyboardButton("ℹ️ ʜᴇʟᴘ", callback_data="help"),
             InlineKeyboardButton("👨‍💻 ᴀʙᴏᴜᴛ", callback_data="about")]
        ]

        if not user_data.get("trial_claimed"):
            buttons.insert(0, [InlineKeyboardButton("🎁 ᴄʟᴀɪᴍ 1-ʜᴏᴜʀ ғʀᴇᴇ ᴛʀɪᴀʟ", callback_data="claim_trial")])
        
        caption_text = script.START_TXT.format(query.from_user.mention, temp.B_NAME)

        if query.message.photo:
            await query.message.edit_caption(
                caption=caption_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.edit_text(
                text=caption_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
        
    elif data == "help":
        buttons = [[InlineKeyboardButton("📢 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs", url="https://t.me/TenxHubBackup"), InlineKeyboardButton("📜 ᴏᴡɴᴇʀ", url="https://t.me/XP_Owner_BoT")],
                   [InlineKeyboardButton('🏠 ʜᴏᴍᴇ', callback_data='start')]
        ]
        
        if query.message.photo:
            await query.message.edit_caption(
                caption=script.HELP_TXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.edit_text(
                text=script.HELP_TXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )  

    elif data == "claim_trial":
        await query.answer("ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ғʀᴇᴇ ᴛʀɪᴀʟ...", show_alert=False)
        await query.message.delete()
        await process_trial(client, query.message, query.from_user.id, query.from_user.first_name, query.from_user.mention)
        
    elif data == "subscription":
        user_id = query.from_user.id
        user_data = await db.get_user(user_id)
        current_time = datetime.now()
        
        is_premium = False
        if user_data:
            expiry = user_data.get("expiry_time")
            if expiry:
                if expiry.tzinfo:
                    expiry = expiry.replace(tzinfo=None)
                if expiry > current_time:
                    is_premium = True
                    
        if is_premium:
            await query.answer("✨ Yᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ!", show_alert=True)
            
            already_premium_text = (
                "🌟 <b>Yᴏᴜ Aʟʀᴇᴀᴅʏ Pᴜʀᴄʜᴀꜱᴇᴅ Oᴜʀ Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ!</b>\n\n"
                "<i>Eɴᴊᴏʏ ʏᴏᴜʀ VIP ʙᴇɴᴇꜰɪᴛꜱ. Yᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʟᴀɴ ᴅᴇᴛᴀɪʟꜱ ᴜꜱɪɴɢ /myplan.</i>"
            )
            buttons = [[InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="start")]]
            
            return await query.message.edit_text(
                text=already_premium_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )

        price_buttons = []
        row = []
        for i, price in enumerate(FIXED_PRICES, 1):
            row.append(InlineKeyboardButton(f"💳 ₹{price}", callback_data=f"pay_{price}"))
            if i % 3 == 0:
                price_buttons.append(row)
                row = []
        if row: 
            price_buttons.append(row)
            
        price_buttons.append([InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="start")])
        
        await query.message.edit_text(
            text=script.CHECK_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(price_buttons),
            parse_mode=enums.ParseMode.HTML
        )
        
        
    elif data.startswith("pay_"):
        amount = int(data.split("_")[1])
        user_id = query.from_user.id
        
        state_data = await db.get_payment_state(user_id)
        if state_data:
            await query.answer("⚠️ Pʟᴇᴀꜱᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ʏᴏᴜʀ ᴘʀᴇᴠɪᴏᴜꜱ ᴘᴀʏᴍᴇɴᴛ ᴏʀ ᴜꜱᴇ /cancel ᴛᴏ ꜱᴛᴏᴘ ɪᴛ.", show_alert=True)
            return
            
        await query.answer("🔄 Gᴇɴᴇʀᴀᴛɪɴɢ QR Cᴏᴅᴇ...", show_alert=False)

        mapping = FIXED_PRICES3
        if amount not in mapping:
            return await client.send_message(
                chat_id=query.message.chat.id, 
                text="❌ <b>Iɴᴠᴀʟɪᴅ Aᴍᴏᴜɴᴛ!</b>", 
                parse_mode=enums.ParseMode.HTML
            )

        premium_duration = FIXED_PRICES2.get(amount, "1day")
        duration_text = mapping[amount]
        transaction_note = f"{amount} {duration_text}"

        upi_link = f"upi://pay?pa={UPI_ID}&pn={NAME}&am={amount}&cu={CURRENCY}&tr={user_id}&tn={transaction_note}"
        qr_image = generate_qr(upi_link)
        
        await query.message.delete()

        sent_photo = await client.send_photo(
            chat_id=query.message.chat.id,
            photo=qr_image,  
            caption=script.SCAN_TXT.format(amount, premium_duration),
            reply_markup=None,
            parse_mode=enums.ParseMode.HTML 
        )

        sent_text = await client.send_message(
            chat_id=query.message.chat.id,
            text="📸 <b>Sᴇɴᴅ ᴀ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴏꜰ ᴛʜᴇ ᴘᴀʏᴍᴇɴᴛ ꜰᴏʀ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ.</b>\n\n<i>Uꜱᴇ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇꜱꜱ.</i>",
            parse_mode=enums.ParseMode.HTML
        )

        await db.set_payment_state(user_id, {
            "amount": amount,
            "premium_duration": premium_duration,
            "photo_id": sent_photo.id,
            "text_id": sent_text.id,
            "pay_type": "pay"
        })

        asyncio.create_task(
            payment_timer_task(client, user_id, query.message.chat.id, amount, premium_duration, sent_photo.id, sent_text.id)
        )
        
    elif data.startswith("approve_"):
        data_parts = data.split("_")
        target_user_id = int(data_parts[1])
        amount = int(data_parts[2])

        await query.answer("Pʀᴏᴄᴇꜱꜱɪɴɢ Aᴘᴘʀᴏᴠᴀʟ...", show_alert=False)
        
        premium_duration = FIXED_PRICES2.get(amount, "1day")
        seconds = get_seconds(premium_duration)
        
        try:
            user = await client.get_users(target_user_id)
            mention = user.mention
        except Exception:
            mention = f"Uꜱᴇʀ <code>{target_user_id}</code>"
            
        now_dt = datetime.now(pytz.timezone("Asia/Kolkata"))
        now_str = now_dt.strftime("%d-%m-%Y %I:%M:%S %p")
            
        user_data = await db.get_user(target_user_id) or {"id": target_user_id, "name": mention}
        current_expiry = user_data.get("expiry_time")
        current_time = datetime.now()
        
        if current_expiry and current_expiry.tzinfo:
            current_expiry = current_expiry.replace(tzinfo=None)
            
        if current_expiry and current_expiry > current_time:
            new_expiry = current_expiry + timedelta(seconds=seconds)
        else:
            new_expiry = current_time + timedelta(seconds=seconds)
            
        user_data["expiry_time"] = new_expiry
        await db.update_user(user_data) 
        
        tz = pytz.timezone("Asia/Kolkata")
        expiry_str = new_expiry.astimezone(tz).strftime("%d-%m-%Y ᴀᴛ %I:%M:%S %p")
        
        try:
            await db.payments.insert_one({
                "user_id": target_user_id,
                "name": mention,
                "amount": amount,
                "pay_type": "pay",
                "date": now_str
            })
        except Exception:
            pass

        reward_ranges = {
            15: (2, 5), 39: (5, 10), 75: (10, 15),
            110: (15, 20), 199: (20, 30), 360: (30, 50),
        }

        reward_points = 0
        min_r, max_r = reward_ranges.get(amount, (0, 0))
        if max_r > 0:
            reward_points = random.randint(min_r, max_r)
            try:
                await db.rewards.update_one(
                    {"user_id": target_user_id},
                    {"$inc": {"coins": reward_points}},
                    upsert=True
                )
            except Exception:
                pass

        reward_text = f"\n\n🎁 Yᴏᴜ'ᴠᴇ ᴀʟꜱᴏ ᴇᴀʀɴᴇᴅ <b>{reward_points} Rᴇᴡᴀʀᴅ Pᴏɪɴᴛꜱ!</b>" if reward_points > 0 else ""

        btn = None
        try:
            invite_link = await client.create_chat_invite_link(
                chat_id=CHANNEL_LINK,
                member_limit=1,
                expire_date=current_time + timedelta(minutes=5)
            )
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("✨ Jᴏɪɴ VIP Cʜᴀɴɴᴇʟ ✨", url=invite_link.invite_link)]])
        except Exception:
            pass 
            
        success_caption = (
            f"🎉 <b>Pᴀʏᴍᴇɴᴛ Vᴇʀɪꜰɪᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!</b>\n\n"
            f"👋 Hᴇʟʟᴏ {mention}, ʏᴏᴜʀ ᴘᴀʏᴍᴇɴᴛ ᴏꜰ <b>₹{amount}</b> ʜᴀꜱ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ.\n\n"
            f"📦 <b>Pʟᴀɴ:</b> <code>{premium_duration} Pʀᴇᴍɪᴜᴍ</code>\n"
            f"📅 <b>Nᴇᴡ Exᴘɪʀʏ:</b> <code>{expiry_str}</code>\n"
            f"👉 <i>/myplan</i>\n"
            f"{reward_text}\n"
            f"👉 <i>/myreward</i>\n\n"
            f"⚠️ <b>Iᴍᴘᴏʀᴛᴀɴᴛ Wᴀʀɴɪɴɢ:</b>\n"
            f"• Tʜɪꜱ ʟɪɴᴋ ᴡɪʟʟ ᴡᴏʀᴋ ꜰᴏʀ <b>1 ᴘᴇʀꜱᴏɴ ᴏɴʟʏ</b>.\n"
            f"• Iᴛ ᴡɪʟʟ ꜱᴛʀɪᴄᴛʟʏ ᴇxᴘɪʀᴇ ɪɴ <b>5 ᴍɪɴᴜᴛᴇꜱ</b>."
        )

        try:
            await client.send_photo(
                chat_id=target_user_id,
                photo=SUCCESSFULLY_PIC,
                caption=success_caption,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            pass 

        current_caption = query.message.caption or ""
        new_caption = (
            current_caption + 
            f"\n\n<b>Sᴛᴀᴛᴜꜱ:</b> ✅ Aᴘᴘʀᴏᴠᴇᴅ ʙʏ {query.from_user.mention}\n"
            f"<b>Aᴄᴛɪᴏɴ Tᴀᴋᴇɴ:</b> Pʀᴇᴍɪᴜᴍ Aᴅᴅᴇᴅ\n"
            f"💰 <b>Rᴇᴠᴇɴᴜᴇ Aᴅᴅᴇᴅ:</b> ₹{amount}\n"
            f"🎁 <b>Rᴇᴡᴀʀᴅ Gɪᴠᴇɴ:</b> {reward_points} Cᴏɪɴꜱ"
        )
        
        try:
            await query.message.edit_caption(
                caption=new_caption,
                reply_markup=None, 
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            pass

        if query.message.photo:
            try:
                await client.send_photo(
                    chat_id=SCREENSHOT,
                    photo=query.message.photo.file_id,
                    caption=f"🔥 <b>Pʀɪᴄᴇ:</b> ₹{amount}\n📅 <b>Dᴜʀᴀᴛɪᴏɴ:</b> {premium_duration}\n👤 <b>Aᴘᴘʀᴏᴠᴇᴅ Bʏ:</b> @TenxHubBackup",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("💠 Bᴜʏ Tᴏ Pʀᴇᴍɪᴜᴍ", url="https://t.me/XP_PaymentBoT")],
                        [InlineKeyboardButton("📝 Aɴʏ Qᴜᴇꜱᴛɪᴏɴꜱ", url="https://t.me/XP_Owner_BoT")]
                    ]),
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception:
                pass


    elif data.startswith("reject_"):
        target_user_id = int(data.split("_")[1])
        amount = int(data.split("_")[2])
        premium_duration = FIXED_PRICES2.get(amount, "1day")
        
        await query.answer("Pᴀʏᴍᴇɴᴛ Rᴇᴊᴇᴄᴛᴇᴅ!", show_alert=False)

        reject_text = (
            "❌ <b>Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ RᴇQᴜᴇꜱᴛ Dᴇᴄʟɪɴᴇᴅ Bʏ Aᴅᴍɪɴ!</b>\n\n"
            "📄 <b>Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Dᴇᴛᴀɪʟꜱ:</b>\n"
            f"💰 <b>Pʀɪᴄᴇ:</b> <code>₹{amount}</code>\n"
            f"⏳ <b>Dᴜʀᴀᴛɪᴏɴ:</b> <code>{premium_duration}</code>\n"
            "📄 <b>Tʏᴘᴇ:</b> <code>Pᴜʀᴄʜᴀꜱᴇ</code>\n\n"
            "📋 <b>Rᴇᴀꜱᴏɴ:</b> <code>Sᴏʀʀʏ ᴘᴀʏᴍᴇɴᴛ ɴᴏᴛ ʀᴇᴄᴇɪᴠᴇᴅ.</code>\n\n"
            "<i>Mᴀᴋᴇ ᴘᴀʏᴍᴇɴᴛ ᴀɴᴅ ꜱᴇɴᴅ ʀᴇQᴜᴇꜱᴛ ᴀɢᴀɪɴ. ☺️</i>\n\n"
            "<i>Iꜰ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ɪꜱ ᴀ ᴍɪꜱᴛᴀᴋᴇ ᴏʀ ʜᴀᴠᴇ ᴀɴʏ Qᴜᴇꜱᴛɪᴏɴꜱ, ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴀᴅᴍɪɴ. 🧑‍💻💬</i>"
        )

        user_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Jᴏɪɴ Uᴘᴅᴀᴛᴇꜱ", url="https://t.me/TenxHubBackup"), InlineKeyboardButton("📜 Oᴡɴᴇʀ", url="https://t.me/XP_Owner_BoT")]
        ])

        try: 
            await client.send_photo(
                chat_id=target_user_id,
                photo=DECLINED_PIC,
                caption=reject_text,
                reply_markup=user_buttons,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            try:
                await client.send_message(
                    chat_id=target_user_id, 
                    text=reject_text, 
                    reply_markup=user_buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception: 
                pass

        current_caption = query.message.caption or ""
        new_caption = current_caption + f"\n\n<b>Sᴛᴀᴛᴜꜱ:</b> ❌ Rᴇᴊᴇᴄᴛᴇᴅ ʙʏ {query.from_user.mention}"
        
        try:
            await query.message.edit_caption(
                caption=new_caption, 
                reply_markup=None, 
                parse_mode=enums.ParseMode.HTML
            )
        except Exception: 
            pass
            
    elif data.startswith("claim_") and data != "claim_trial":
        target_user_id = int(data.split("_")[1])

        if user_id != target_user_id:
            return await query.answer("❌ Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴄʟᴀɪᴍ ᴛʜɪꜱ ʀᴇᴡᴀʀᴅ! Uꜱᴇ /myreward.", show_alert=True)

        user_profile = await db.get_user(user_id) or {"id": user_id, "name": query.from_user.first_name}
        current_time = datetime.now()
        
        current_expiry = user_profile.get("expiry_time")
        if current_expiry and current_expiry.tzinfo:
            current_expiry = current_expiry.replace(tzinfo=None)

        if current_expiry and current_expiry > current_time:
            return await query.answer("❌ Yᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ! Yᴏᴜ ᴄᴀɴɴᴏᴛ ᴄʟᴀɪᴍ ʀᴇᴡᴀʀᴅꜱ ʀɪɢʜᴛ ɴᴏᴡ.", show_alert=True)

        user_data = await db.rewards.find_one({"user_id": user_id})
        coins = user_data.get("coins", 0) if user_data else 0

        if coins < 50:
            return await query.answer("❌ Yᴏᴜ ɴᴇᴇᴅ ᴀᴛ ʟᴇᴀꜱᴛ 50 ᴘᴏɪɴᴛꜱ ᴛᴏ ᴄʟᴀɪᴍ ᴀ ʀᴇᴡᴀʀᴅ!", show_alert=True)

        REWARD_TIERS = [
            {"cost": 180, "duration": "48 Hᴏᴜʀ", "hours": 48},  
            {"cost": 150, "duration": "24 Hᴏᴜʀ", "hours": 24},  
            {"cost": 110, "duration": "12 Hᴏᴜʀ", "hours": 12},  
            {"cost": 60,  "duration": "6 Hᴏᴜʀ",  "hours": 6},   
            {"cost": 50,  "duration": "2 Hᴏᴜʀ",  "hours": 2}    
        ]

        eligible_tier = next((tier for tier in REWARD_TIERS if coins >= tier["cost"]), None)

        if not eligible_tier:
            return await query.answer("❌ Nᴏᴛ ᴇɴᴏᴜɢʜ ᴘᴏɪɴᴛꜱ ꜰᴏʀ ᴀɴʏ ʀᴇᴡᴀʀᴅ ᴛɪᴇʀ.", show_alert=True)

        cost = eligible_tier["cost"]
        duration = eligible_tier["duration"]
        hours_to_add = eligible_tier["hours"]
        remaining_points = coins - cost

        await query.answer("🔄 Pʀᴏᴄᴇꜱꜱɪɴɢ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ʀᴇᴡᴀʀᴅ...", show_alert=False)

        await db.rewards.update_one(
            {"user_id": user_id},
            {"$set": {"coins": remaining_points}}
        )

        new_expiry = current_time + timedelta(hours=hours_to_add)
        user_profile["expiry_time"] = new_expiry
        
        btn = None
        try:
            invite_link = await client.create_chat_invite_link(
                chat_id=CHANNEL_LINK, 
                member_limit=1, 
                expire_date=current_time + timedelta(minutes=5)
            )
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("✨ Jᴏɪɴ VIP Cʜᴀɴɴᴇʟ ✨", url=invite_link.invite_link)]])
        except Exception:
            pass

        await db.update_user(user_profile)

        try:
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=(
                    f"🎁 <b>#Rᴇᴡᴀʀᴅ_Cʟᴀɪᴍᴇᴅ</b>\n\n"
                    f"👤 <b>Uꜱᴇʀ:</b> {query.from_user.mention} [<code>{user_id}</code>]\n"
                    f"🪙 <b>Pᴏɪɴᴛꜱ Sᴘᴇɴᴛ:</b> <code>{cost}</code>\n"
                    f"⏱️ <b>Pʀᴇᴍɪᴜᴍ Gᴏᴛ:</b> <code>{duration}</code>"
                )
            )
        except Exception:
            pass
        
        success_caption = (
            f"✅ <b>Rᴇᴡᴀʀᴅ Cʟᴀɪᴍᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!</b> 🎉\n\n"
            f"🎁 Yᴏᴜ ꜱᴘᴇɴᴛ <b>{cost} ᴘᴏɪɴᴛꜱ</b> ᴀɴᴅ ʀᴇᴄᴇɪᴠᴇᴅ <b>{duration} Pʀᴇᴍɪᴜᴍ</b>.\n"
            f"💰 <b>Rᴇᴍᴀɪɴɪɴɢ Pᴏɪɴᴛꜱ:</b> <code>{remaining_points}</code>\n\n"
            f"🚀 <i>Cʜᴇᴄᴋ ʏᴏᴜʀ ꜱᴛᴀᴛᴜꜱ ᴜꜱɪɴɢ /myplan</i>"
        )

        try:
            await query.message.delete()
        except Exception:
            pass
            
        await client.send_photo(
            chat_id=user_id,
            photo=CLAIM_REWARD_PIC,
            caption=success_caption,
            reply_markup=btn,
            parse_mode=enums.ParseMode.HTML
        )
        
