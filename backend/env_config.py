#from decouple import config
from dotenv import load_dotenv
import os

def load_env():
    # Determine the environment (e.g., DJANGO_ENV environment variable)
    # Default to 'development' if not set
    environment = os.environ.get('DJANGO_ENV', 'development')
    print(environment)
    # Load the appropriate .env file based on the environment
    if environment == 'development':
        # Load the .env.dev file
        load_dotenv('.env.dev')
    elif environment == 'production':
        # Load the .env.prod file
        load_dotenv('.env.prod')
    else:
        raise ValueError("Invalid environment. Use 'development' or 'production'.")

