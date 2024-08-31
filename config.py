import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SCENARIO_API_KEY = os.getenv("SCENARIO_API_KEY")
SCENARIO_SECRET_KEY = os.getenv("SCENARIO_SECRET_KEY")
