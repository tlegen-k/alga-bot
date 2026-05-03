import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID: int = int(os.environ["ADMIN_CHAT_ID"])
DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
