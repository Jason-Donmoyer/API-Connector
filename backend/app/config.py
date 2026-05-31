from dotenv import load_dotenv
import os

load_dotenv()

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

