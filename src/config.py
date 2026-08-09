import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("Переменная BASE_URL не найдена в файле .env")