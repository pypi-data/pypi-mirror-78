import os
import uuid


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', uuid.uuid4().hex)