import sys
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = os.getenv("AWS_REGION", None)
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", None)
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID", None)
S3_BUCKET = os.getenv("S3_BUCKET", None)
S3_URL = os.getenv("S3_BUCKET", None)
CLOUD_FRONT_URL = os.getenv("CLOUD_FRONT_URL", None)

TABLE_NAME = "Users"
VALID_USER_TYPES = ["consumer", "provider"]
VALID_SKILL_TYPES = ["driver", "electrician", "plumber", \
    "carpenter", "house maid", "baby sitter", \
    "elder care", "cook", "nanny", "beautician", \
    "painter", "delivery boy", "gardener",  \
    "cleaner", "pest control", "decorators"]
CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:4200',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'X-CSRFToken',
    'x-csrftoken',
    'X-XSRF-TOKEN',
    'XSRF-TOKEN',
    'csrfmiddlewaretoken',
    'csrftoken',
    'X-CSRF'
]

if AWS_ACCESS_KEY_ID is None:
    print("Please set AWS_ACCESS_KEY_ID !!!")
    sys.exit(1)
elif AWS_SECRET_ACCESS_KEY is None:
    print("Please set AWS_SECRET_ACCESS_KEY !!!")
    sys.exit(1)
elif AWS_REGION is None:
    print("Please set AWS_REGION !!!")
    sys.exit(1)
elif COGNITO_USER_POOL_ID is None:
    print("Please set COGNITO_USER_POOL_ID !!!")
    sys.exit(1)
elif COGNITO_APP_CLIENT_ID is None:
    print("Please set COGNITO_APP_CLIENT_ID !!!")
    sys.exit(1)
elif S3_BUCKET is None:
    print("Please set S3_BUCKET !!!")
    sys.exit(1)
elif S3_URL is None:
    print("Please set S3_URL !!!")
    sys.exit(1)
elif CLOUD_FRONT_URL is None:
    print("Please set CLOUD_FRONT_URL !!!")
    sys.exit(1)

