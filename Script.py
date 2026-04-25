class script(object):

    START_TXT = """<b>✨ ʜᴇʟʟᴏ {}!</b>

🚀 <b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {}!</b>  

ᴛʜɪs ʙᴏᴛ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ɪs ғᴜʟʟʏ ᴀᴜᴛᴏᴍᴀᴛɪᴄ. ᴀᴀᴘ ᴀᴘɴᴇ ʜɪsᴀʙ sᴇ ᴘʟᴀɴ sᴇʟᴇᴄᴛ ᴋᴀʀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴇɴᴊᴏʏ ᴋᴀʀ sᴀᴋᴛᴇ ʜᴀɪɴ. 🚀"""
    
    LOG_TEXT = """<b>🚀 #ɴᴇᴡᴜsᴇʀ {}

👤 ɴᴀᴍᴇ - {}
🆔 ɪᴅ - <code>{}</code>
🔗 ᴜsᴇʀɴᴀᴍᴇ - {}
⏰ ᴛɪᴍᴇ - {} 
📅 ᴅᴀᴛᴇ - {}
🌍 ᴛɪᴍᴇᴢᴏɴᴇ - ᴀsɪᴀ/ᴋᴏʟᴋᴀᴛᴀ</b>"""

    HELP_TXT = """<b>❓ ɴᴇᴇᴅ ʜᴇʟᴘ ᴏʀ sᴜᴘᴘᴏʀᴛ? 🤖</b>

<i>ғᴏʀ ᴀʟʟ ǫᴜᴇʀɪᴇs ʀᴇʟᴀᴛᴇᴅ ᴛᴏ sᴜʙsᴄʀɪᴘᴛɪᴏɴs, ᴘʟᴀɴs, ᴏʀ ᴀɴʏᴛʜɪɴɢ ᴇʟsᴇ, ᴊᴜsᴛ ʀᴇᴀᴄʜ ᴏᴜᴛ ᴛᴏ ᴏᴜʀ ᴀᴅᴍɪɴs ᴀɴᴅ ᴡᴇ ᴡɪʟʟ ɢᴇᴛ ʙᴀᴄᴋ ᴛᴏ ʏᴏᴜ ᴀs sᴏᴏɴ ᴀs ᴘᴏssɪʙʟᴇ! ⚡📩</i>

<blockquote><b>📝 ᴛᴇʀᴍs & ᴄᴏɴᴅɪᴛɪᴏɴs:</b>
🔸 sᴇɴᴅ ᴀ ᴄʟᴇᴀʀ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ — ғᴀᴋᴇ ᴏʀ ᴇᴅɪᴛᴇᴅ ᴘʀᴏᴏғs ᴡɪʟʟ ʟᴇᴀᴅ ᴛᴏ ᴀ ʙᴀɴ.
🔸 ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴘᴀᴛɪᴇɴᴛʟʏ ғᴏʀ ᴀᴘᴘʀᴏᴠᴀʟ — ᴅᴏ ɴᴏᴛ sᴘᴀᴍ ᴛʜᴇ ʙᴏᴛ.
🔸 ɴᴏ ʀᴇғᴜɴᴅs ᴡɪʟʟ ʙᴇ ɪssᴜᴇᴅ ᴀғᴛᴇʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛɪᴏɴ.</blockquote>

<b>🆘 sᴜᴘᴘᴏʀᴛ & ᴄᴏɴᴛᴀᴄᴛs:</b>
🔹 Hum fast, safe aur reliable service dene ke liye pratibaddh hain.  
🔹 ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ: <b>@premiumuseronly_Bot</b>  
🔹 sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ: <b>@premiumuseronly_Bot</b>"""

    ABOUT_TXT = """<b>╔═══❰  {}  ❱═══❍
║╭━━━━━━━━━━━━━━━➣
║┣⪼🤖 ᴍʏ ɴᴀᴍᴇ : {}
║┣⪼👑 ᴏᴡɴᴇʀ : <a href='https://t.me/premiumuseronly_Bot'>xᴘ ᴏᴡɴᴇʀ</a>
║┣⪼👦 ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/premiumuseronly_Bot'>ᴀᴍᴀɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ</a>
║┣⪼❣️ ᴜᴘᴅᴀᴛᴇ : <a href='https://t.me/+oHB7vpOIXdszOWVl'>xᴘ ʙᴏᴛᴢ</a>
║┣⪼📡 ʜᴏsᴛᴇᴅ ᴏɴ : ᴋᴏʏᴇʙ 
║┣⪼🗣️ ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ 3
║┣⪼📚 ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ
║┣⪼🗒️ ᴠᴇʀsɪᴏɴ : ᴀᴅᴠᴀɴᴄᴇ ᴠ2.01
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍ </b>"""
    
    CHECK_TXT = """<blockquote>🎖️ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs :</blockquote>

<i>❏ ₹𝟷𝟻   ➠ 𝟷 ᴡᴇᴇᴋ ᴀᴄᴄᴇss  
❏ ₹𝟹𝟿   ➠ 𝟷 ᴍᴏɴᴛʜ 
❏ ₹𝟽𝟻   ➠ 𝟸 ᴍᴏɴᴛʜs  
❏ ₹𝟷𝟷𝟶 ➠ 𝟹 ᴍᴏɴᴛʜs  
❏ ₹𝟷𝟿𝟿 ➠ 𝟼 ᴍᴏɴᴛʜs
❏ ₹𝟹𝟼𝟶 ➠ 𝟷𝟸 ᴍᴏɴᴛʜs</i> <b>(ʙᴇsᴛ ᴠᴀʟᴜᴇ)</b>

<b>⚠️ Payment ke baad screenshot bhejein:</b>  
<i>📸 Verification ke liye apna payment screenshot bhejein.</i>

<b><u>👇 Neeche diye gaye buttons se apna plan choose karein.</u></b>"""

    SCAN_TXT = """<b>🧾 ᴘᴀʏᴍᴇɴᴛ ᴅᴇᴛᴀɪʟs:</b>

• QR code scan karke payment karein <b>₹{}</b>  
• ᴘᴀʏ ᴛʏᴘᴇ: <b>{}</b>
• ᴘʀᴇᴍɪᴜᴍ ᴛɪᴍᴇ: <b>{}</b>
• ǫʀ ᴄᴏᴅᴇ ᴠᴀʟɪᴅ ғᴏʀ <b>5 ᴍɪɴᴜᴛᴇs</b>

<blockquote><b>⚠️ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ:</b>
📸 • Payment ke baad screenshot bhejein </blockquote>"""
    
    AUTH_TXT = """<b>👋 ʜᴇʟʟᴏ {} !

⚠️ Mujhe use karne ke liye kripya hamare updates channel ko join karein !

Server overload ke karan sirf hamare channel ke subscribers hi is bot ko use kar sakte hain !</b>"""
    
