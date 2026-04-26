from os import environ

def str_to_bool(val):
    return str(val).lower() in {"true", "yes", "1", "t", "y"}

API_ID = int(environ.get('API_ID', '23621595'))
API_HASH = environ.get('API_HASH', 'de904be2b4cd4efe2ea728ded17ca77d')
BOT_TOKEN = environ.get("BOT_TOKEN", "")
PORT = environ.get("PORT", "8000")

START_PIC = environ.get("START_PIC", "https://files.catbox.moe/nylx2a.jpg")
PAYMENT_UN_PIC = environ.get("PAYMENT_PIC", "https://files.catbox.moe/9o2l2f.jpg")
DECLINED_PIC = environ.get("DECLINE_PIC", "https://files.catbox.moe/oml3v4.jpg")
SUCCESSFULLY_PIC = environ.get("SUCCESS_PIC", "https://files.catbox.moe/1vvrjd.jpg")
EXPIRE_SOON_PIC = environ.get("REMINDER_PIC", "https://files.catbox.moe/j27k1r.jpg")
END_PIC = environ.get("EXPIRY_PIC", "https://files.catbox.moe/eevnt4.jpg")
REWARD_PIC = environ.get("REWARD_PIC", "https://files.catbox.moe/ktdef9.jpg")
CLAIM_REWARD_PIC = environ.get("CLAIM_PIC", "https://files.catbox.moe/20jktr.jpg")
AUTH_PICS = environ.get("AUTH_PICS", "https://files.catbox.moe/facpku.jpg")

ADMINS = list(map(int, environ.get("ADMINS", "1249672673").split()))
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1003184409377"))
SCREENSHOT = int(environ.get("SCREENSHOT_CHANNEL", "-1002813745328"))

#add premium channel 
CHANNEL_LINK_INST = int(environ.get("INSTA_LINK_ID", "-1002259803190"))
CHANNEL_LINK_MOV = int(environ.get("MOVIE_LINK_ID", "-1001551886347"))


#post channel 
MOVIE_CHANNEL = int(environ.get("MOVIE_POST_ID", "-1001551886347"))
INSTA_CHANNEL = int(environ.get("INSTA_POST_ID", "-1002259803190"))

DB_URL = environ.get('DATABASE_URI', "mongodb+srv://wajsarif461_db_user:TwacJh76mwpHHpjw@cluster0.biueyst.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
")
DB_NAME = environ.get('DATABASE_NAME', "testing")

CHANNEL = environ.get("CHANNEL", "https://t.me/MovieSearchAutoGroup")
SUPPORT = environ.get("SUPPORT", "https://t.me/payment_prime")

AUTH_CHANNEL = list(map(int, environ.get("AUTH_CHANNEL", "-1002641663814").split()))
AUTH_REQ_CHANNEL = list(map(int, environ.get("AUTH_REQ_CHANNELS", "-1002314687215").split()))
FSUB = str_to_bool(environ.get("FSUB", "True"))
