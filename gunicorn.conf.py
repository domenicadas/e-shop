import os

bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"
workers = int(os.getenv('WEB_CONCURRENCY', '3'))
accesslog = '-'
errorlog = '-'
