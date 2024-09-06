import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SCENARIO_API_KEY = os.getenv("SCENARIO_API_KEY")
SCENARIO_SECRET_KEY = os.getenv("SCENARIO_SECRET_KEY")
TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
MESHY_API_KEY = os.getenv("MESHY_API_KEY")
