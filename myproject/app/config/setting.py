import os
from starlette.config import Config

current_dir = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(current_dir, "../../.env"))

config = Config(ENV_PATH)


PORT = config('PORT', cast=int, default=8000)
HOST = config('HOST', cast=str, default='localhost')
ALLOWED_ORIGIN = config('ALLOWED_ORIGIN', cast=str,  default='*')
JWT_SECRET_KEY = config('JWT_SECRET_KEY', cast=str, default='secret-key')