import datetime
from datetime import timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from info import DB_URL, DB_NAME

client = AsyncIOMotorClient(DB_URL)
mydb = client[DB_NAME]

class Database:
    def __init__(self):
        self.users = mydb.users
        self.codes = mydb.codes
        self.rewards = mydb.rewards
        self.payment_state = mydb.payment_state 
        self.payments = mydb.payments # 👈 FIX 1: Yeh line add karni zaroori thi!

    async def add_user(self, id, name, username, date):
        user = {"id": int(id), "name": name, "username": username, "joined_date": date}
        await self.users.update_one({"id": int(id)}, {"$set": user}, upsert=True)

    async def is_user_exist(self, id):
        user = await self.users.find_one({'id': int(id)})
        return bool(user)

    async def total_users(self):
        return await self.users.count_documents({})

    async def get_all_users(self):
        return self.users.find({})

    async def delete_user(self, user_id):
        await self.users.delete_many({'id': int(user_id)})

    async def total_users_count(self):
        return await self.users.count_documents({})

    async def set_payment_state(self, user_id, data):
        await self.payment_state.update_one(
            {"user_id": int(user_id)},
            {"$set": data},
            upsert=True
        )

    async def get_payment_state(self, user_id):
        return await self.payment_state.find_one({"user_id": int(user_id)})

    async def del_payment_state(self, user_id):
        await self.payment_state.delete_one({"user_id": int(user_id)})

    async def get_user(self, user_id):
        user_data = await self.users.find_one({"id": int(user_id)})
        return user_data

    async def update_user(self, user_data):
        await self.users.update_one(
            {"id": int(user_data["id"])}, 
            {"$set": user_data}, 
            upsert=True
        )

    async def get_expired(self, current_time):
        expired_users = []
        cursor = self.users.find({"expiry_time": {"$lt": current_time}})
        async for user in cursor:
            expired_users.append(user)
        return expired_users

    async def get_expiring_soon(self, label, delta):
        reminder_key = f"reminder_{label}_sent"
        now = datetime.datetime.utcnow()
        target_time = now + delta
        window = timedelta(seconds=30)

        start_range = target_time - window
        end_range = target_time + window

        reminder_users = []
        cursor = self.users.find({
            "expiry_time": {"$gte": start_range, "$lte": end_range},
            reminder_key: {"$ne": True}
        })

        async for user in cursor:
            reminder_users.append(user)
            await self.users.update_one(
                {"id": user["id"]}, {"$set": {reminder_key: True}}
            )

        return reminder_users

    async def remove_premium_access(self, user_id):
        return await self.users.update_one(
            {"id": int(user_id)}, 
            {"$set": {"expiry_time": None}} 
        )

    async def total_amount(self):
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
        result = await self.payments.aggregate(pipeline).to_list(1)
        return result[0]["total"] if result else 0
        
    async def total_payments(self):
        return await self.payments.count_documents({})
        
db = Database()
