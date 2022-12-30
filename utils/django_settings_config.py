REDIS_CACHE = """
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config("REDIS_PASSWORD"),
        },
    }
}"""

RQ_SCHEDULER = """
RQ_QUEUES = {
    "default": {
        "HOST": "redis",
        "PORT": 6379,
        "DB": 0,
        "PASSWORD": config("REDIS_PASSWORD"),
        "DEFAULT_TIMEOUT": 360,
    }
}"""

EMAIL = """
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")"""
