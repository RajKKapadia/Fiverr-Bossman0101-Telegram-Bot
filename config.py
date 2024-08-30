import os

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())

# OpenAI client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
