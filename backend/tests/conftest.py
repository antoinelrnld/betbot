import os

os.environ.setdefault(
    "BETBOT_DATABASE_URL",
    "postgresql+asyncpg://betbot:test@localhost:5432/test",
)
