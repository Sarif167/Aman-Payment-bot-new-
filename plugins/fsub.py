import asyncio # Fixed: lowercase 'import'
import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from database.users_db import db
from info import ADMINS, AUTH_CHANNEL, AUTH_REQ_CHANNEL, AUTH_PICS
from utils import temp
from Script import script

logger = logging.getLogger(__name__)

# Filter function fixed
def is_auth_req_channel(_, __, query):
    if not AUTH_REQ_CHANNEL:
        return False
    # Ensure AUTH_REQ_CHANNEL is a list/tuple
    return query.chat.id in (AUTH_REQ_CHANNEL if isinstance(AUTH_REQ_CHANNEL, list) else [AUTH_REQ_CHANNEL])

@Client.on_chat_join_request(filters.create(is_auth_req_channel)) # Added filters.create
async def join_reqs(client, message: ChatJoinRequest):
    try:
        await db.add_join_req(message.from_user.id, message.chat.id)
    except Exception as e:
        logger.error(f"Error saving join request: {e}")

@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")

# ========== REQUIRED JOIN FUNCTION (APPROVE REQ) ==========
async def is_req_subscribed(bot, user_id, rqfsub_channels, database): # Renamed 'db' to 'database' to avoid confusion
    if not database: # Safety check for NoneType error
        from database.users_db import db as database
        
    btn = []
    # Ensure channels is a list
    channels = rqfsub_channels if isinstance(rqfsub_channels, list) else [rqfsub_channels]
    
    for ch_id in channels:
        if await database.has_joined_channel(user_id, ch_id):
            continue
        try:
            member = await bot.get_chat_member(ch_id, user_id)
            if member.status in [enums.ChatMemberStatus.MEMBER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                await database.add_join_req(user_id, ch_id)
                continue
        except UserNotParticipant:
            pass 
        except Exception as e:
            logger.error(f"Error checking membership in {ch_id}: {e}")
        
        try:
            chat = await bot.get_chat(ch_id)
            invite = await bot.create_chat_invite_link(ch_id, creates_join_request=True)
            btn.append([InlineKeyboardButton(f"📩 Join {chat.title}", url=invite.invite_link)])
        except Exception as e:
            logger.warning(f"Invite link error for {ch_id}: {e}")
            
    return btn

# ========== NORMAL F-SUB FUNCTION ==========
async def is_subscribed(bot, user_id, fsub_channels):
    btn = []
    channels = fsub_channels if isinstance(fsub_channels, list) else [fsub_channels]

    async def check_channel(channel_id):
        try:
            await bot.get_chat_member(channel_id, user_id)
        except UserNotParticipant:
            try:
                chat = await bot.get_chat(int(channel_id))
                return InlineKeyboardButton(f"📢 Join {chat.title}", url=(await bot.create_chat_invite_link(channel_id)).invite_link)
            except Exception:
                return None
        except Exception:
            return None
        return None

    tasks = [check_channel(c) for c in channels]
    results = await asyncio.gather(*tasks)
    for button in results:
        if button: btn.append([button])
    return btn

# ========== MAIN USER CHECK FUNCTION ==========
async def is_user_joined(client, message):
    user_id = message.from_user.id
    btn = []
    
    # 1. Check Normal FSUB
    if AUTH_CHANNEL:
        btn += await is_subscribed(client, user_id, AUTH_CHANNEL)
    
    # 2. Check Request FSUB
    if AUTH_REQ_CHANNEL:
        btn += await is_req_subscribed(client, user_id, AUTH_REQ_CHANNEL, db)
    
    if btn:
        # --- PARAMETER EXTRACTION ---
        # Agar user kisi file link se aaya hai (movie-123), toh wo parameter bachega.
        # Agar koi parameter nahi hai, toh default 'start' par bhejega.
        param = message.command[1] if (hasattr(message, 'command') and len(message.command) > 1) else "start"
        
        # --- URL BUTTON ---
        btn.append([
            InlineKeyboardButton(
                "🔄 ᴛʀʏ ᴀɢᴀɪɴ", 
                url=f"https://t.me/{temp.U_NAME}?start={param}"
            )
        ])
        
        reply_markup = InlineKeyboardMarkup(btn)
        mention = message.from_user.mention
        text = script.AUTH_TXT.format(mention)
        
        if AUTH_PICS:
            await message.reply_photo(
                photo=AUTH_PICS,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        return False # Subscription complete nahi hai
        
    return True # User passed all checks
