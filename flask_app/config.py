import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    FOTO_APAR = 'app/static/img/apar/foto'
    FOTO_P3K = 'app/static/img/p3k/foto'
    FOTO_HYDRANT = 'app/static/img/hydrant/foto'
    FOTO_TTD = 'app/static/img/absen/ttd'
    FOTO_APAR_TTD = 'app/static/img/apar/ttd'
    FOTO_P3K_TTD = 'app/static/img/p3k/ttd'
    FOTO_HYDRANT_TTD = 'app/static/img/hydrant/ttd'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    APA = 'XXXXX'
