import os
from dotenv import load_dotenv

# Load .env file from the current directory
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
HUGO_CONTENT_DIR = os.path.abspath(os.getenv('HUGO_CONTENT_DIR', 'content/posts'))
INTERESTS = ['DevOps', 'Systems Administration', 'Bitcoin', 'Linux', 'Engineering', 'Science']
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
