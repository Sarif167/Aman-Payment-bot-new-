from os import environ

API_ID = int(environ.get('API_ID', '28690893'))
API_HASH = environ.get('API_HASH', 'c214f988aa1ac0b998ace0b7cd0e215f')
BOT_TOKEN = environ.get("BOT_TOKEN", "")
PORT = environ.get("PORT", "8000")

START_PIC = environ.get("START_PIC", "https://files.catbox.moe/nylx2a.jpg")
PAYMENT_UN_PIC = environ.get("START_PIC", "https://files.catbox.moe/9o2l2f.jpg")
DECLINED_PIC = environ.get("START_PIC", "https://files.catbox.moe/oml3v4.jpg")
SUCCESSFULLY_PIC = environ.get("START_PIC", "https://files.catbox.moe/1vvrjd.jpg")
EXPIRE_SOON_PIC = environ.get("START_PIC", "https://files.catbox.moe/j27k1r.jpg")
END_PIC = environ.get("START_PIC", "https://files.catbox.moe/eevnt4.jpg")
TRIAL_PIC = environ.get("TRIAL_PIC", "https://files.catbox.moe/9yhy65.jpg")


REWARD_PIC = environ.get("TRIAL_PIC", "https://files.catbox.moe/ktdef9.jpg")
CLAIM_REWARD_PIC = environ.get("TRIAL_PIC", "https://files.catbox.moe/20jktr.jpg")

ADMINS = list(map(int, environ.get("ADMINS", "1454524346").split()))

LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1003625964837"))
CHANNEL_LINK = int(environ.get("LOG_CHANNEL", "-1003567090375"))
SCREENSHOT = int(environ.get("LOG_CHANNEL", "-1003636482628"))

DB_URL = environ.get("DATABASE_URI", "mongodb+srv://SubscriptionBoT:SubscriptionBoT@cluster0.13yqal2.mongodb.net/?appName=Cluster0")
DB_NAME = environ.get("DATABASE_NAME", "Cluster0")

CHANNEL = environ.get("CHANNEL", "https://t.me/TenxHubBackup")
SUPPORT = environ.get("SUPPORT", "https://t.me/TenxHubSupport")


