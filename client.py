from os import getenv
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv("./config.env")
url = getenv("URL")
key = getenv("API_KEY")

s_client: Client = create_client(url, key)