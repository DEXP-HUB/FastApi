import os

from dotenv import load_dotenv

from authx import AuthXConfig


load_dotenv()


config = AuthXConfig(
    JWT_SECRET_KEY=str(os.getenv('JWT_SECRET_KEY')),
    JWT_ACCESS_COOKIE_NAME=str(os.getenv('JWT_ACCESS_COOKIE_NAME')),
    JWT_REFRESH_COOKIE_NAME=str(os.getenv('JWT_REFRESH_COOKIE_NAME')),
    JWT_TOKEN_LOCATION=['cookies']
)
