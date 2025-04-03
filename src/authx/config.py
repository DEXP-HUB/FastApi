import os

from authx import AuthXConfig

from configparser import ConfigParser



config = ConfigParser()
config.read('src\config.ini')


config_authx = AuthXConfig(
    JWT_SECRET_KEY = config['Authx']['JWT_SECRET_KEY'],
    JWT_ACCESS_COOKIE_NAME = config['Authx']['JWT_ACCESS_COOKIE_NAME'],
    JWT_REFRESH_COOKIE_NAME = config['Authx']['JWT_REFRESH_COOKIE_NAME'],
    JWT_TOKEN_LOCATION = [config['Authx']['JWT_TOKEN_LOCATION']],
    JWT_COOKIE_CSRF_PROTECT = False
)
