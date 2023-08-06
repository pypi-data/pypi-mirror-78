import environ

env = environ.Env()

PRODUCTION = env.bool("DJANGO_PRODUCTION", default=False)
DEBUG = False if PRODUCTION else env.bool("DJANGO_DEBUG", default=True)


def prod_required_env(key, default, method="str"):
    """Throw an exception if PRODUCTION is true and key is not provided"""
    if PRODUCTION:
        default = environ.Env.NOTSET
    return getattr(env, method)(key, default)


ALLOWED_HOSTS = [prod_required_env("DJANGO_ALLOWED_HOST", default="*")]

db_config = env.db_url("DATABASE_URL", default="postgres://postgres:postgres@db/postgres")
DATABASES = {"default": db_config}
