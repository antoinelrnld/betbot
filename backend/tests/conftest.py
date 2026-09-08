import os

os.environ["BETBOT_APP_ENV"] = "test"
os.environ["BETBOT_APP_HOST"] = "127.0.0.1"
os.environ["BETBOT_APP_PORT"] = "8000"
os.environ["BETBOT_DEBUG"] = "false"
os.environ["BETBOT_DATABASE_URL"] = (
    "postgresql+asyncpg://betbot:test@localhost:5432/test"
)
