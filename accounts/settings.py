import sys
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = os.getenv("AWS_REGION", None)
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", None)
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID", None)

TABLE_NAME = "User"
VALID_USER_TYPES = ["consumer", "provider"]
VALID_SKILL_TYPES = ["driver", "electrician", "plumber", \
    "carpenter", "house maid", "baby sitter", \
    "elder care", "cook", "nanny", "beautician", \
    "painter", "delivery boy", "gardener",  \
    "cleaner", "pest control", "decorators"]

if (AWS_ACCESS_KEY_ID is None) or (AWS_SECRET_ACCESS_KEY is None) or (AWS_REGION is None) or (COGNITO_USER_POOL_ID is None) or (COGNITO_APP_CLIENT_ID is None):
    print("Please set environment variables !!!")
    sys.exit(1)

