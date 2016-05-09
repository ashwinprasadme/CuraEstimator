import os
# __file__ refers to the file settings.py
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, '/var/www/CuraEstimator/CuraEstimator/static')
APP_UPLOAD = os.path.join(APP_ROOT, '/var/www/CuraEstimator/CuraEstimator/static/cura/uploads')
APP_SLIC3R = os.path.join(APP_ROOT, '/var/www/CuraEstimator/CuraEstimator/static/cura')
