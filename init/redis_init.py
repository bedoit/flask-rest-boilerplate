from redis import Redis
from init.flask_init import app

redis = Redis(host=app.config['REDIS_HOST'], password=app.config['REDIS_PASSWORD'])
