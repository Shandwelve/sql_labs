import os
from pathlib import Path

from dotenv import load_dotenv

from core.connector import DatabaseConnector

base_path = Path()
basedir = str(base_path.cwd())
env_path = base_path.cwd() / '.env'

load_dotenv(env_path)

database = DatabaseConnector(database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'))

