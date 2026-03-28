import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
import os

# ===== デバッグ（超重要）=====
print("ファイル一覧:", os.listdir())
print("credentials.json exists:", os.path.exists("credentials.json"))

# ===== 設定 =====
TOKEN = "MTQ4NzMzNjQ3NTI1NDMyOTQyNA.GtK0kO.5L7GchmTrf-8v-1smo33lN-RfHvBqsN-0Gl7B8"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1bbybYhgtYtA5egVCOIT91U8XdWTSf0XOzxEatgPAqyU/edit?gid=1017185011#gid=1017185011"

# ===== Google接続 =====
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

gc = gspread.authorize(creds)
spreadsheet = gc.open_by_url(SPREADSHEET_URL)

# 👉 シート名ここ確認！！
sheet = spreadsheet.worksheet("管理")

# ===== Discord =====
intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_open():
    value = sheet.acell("A1").value

    try:
        return int(value) > 0
    except:
        return False

@client.event
async def on_ready():
    print("BOT起動成功🔥")

    while True:
        try:
            is_open = await check_open()

            if is_open:
                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game(name="開店中")
                )
                print("開店中に変更")
            else:
                await client.change_presence(
                    status=discord.Status.idle,
                    activity=discord.Game(name="閉店中")
                )
                print("閉店中に変更")

        except Exception as e:
            print("エラー発生:", e)

        await asyncio.sleep(60)

client.run(TOKEN)
