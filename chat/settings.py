import os
import dotenv
import logging

dotenv.load_dotenv()

LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
LOG_FILE = os.getenv('LOG_FILE', 'chat_logs.log')
