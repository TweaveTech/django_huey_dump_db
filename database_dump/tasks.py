from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from django.conf import settings

from .helpers import make_database_dump
from .exceptions import NotCompatibleError

try:
    import hueyx
    raise NotCompatibleError("Not compatible with hueyx")
except ModuleNotFoundError:
    pass


@db_periodic_task(crontab(**settings.DATABASE_DUMP['crontab']))
def make_database_dump_task():
    return make_database_dump()
