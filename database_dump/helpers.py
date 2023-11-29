from django.conf import settings
from datetime import datetime

import os
import subprocess

import logging
logger = logging.getLogger(__name__)


def make_database_dump(username=None, database_name=None, password=None, dump_dir=None, delete_after=None):
    '''

    :param username: The username that have access to the db
    :param database_name: The name of the db
    :param password: Password of the db
    :param dump_dir: The absolute path where to put the dumps (default will be base dir / dumps)
    :param delete_after: The max number of dumps present in the folder. After reach that number the older will start getting deleted
    '''

    if username is None:
        username = settings.DATABASES['default']['USER']

    if database_name is None:
        database_name = settings.DATABASES['default']['NAME']

    if password is None:
        password = settings.DATABASES['default']['PASSWORD']

    dump_dir = settings.DATABASE_DUMP['path']
    delete_after = settings.DATABASE_DUMP['delete_after']

    # Create the dump-dir, or skip if it is already present.
    os.makedirs(dump_dir, exist_ok=True)

    # Create the dump file name
    file_name = datetime.now().strftime('deployment_dump_%Y_%m_%d_%H:%M.sql')
    file_path = os.path.join(dump_dir, file_name)

    # Set the PGPASSWORD environment variable to avoid password prompt
    os.environ['PGPASSWORD'] = password

    command_array = ['pg_dump', '-h', 'localhost', '--username=' + username, '--dbname=' + database_name, '-F', 'c', '-Z', '9', '-f', file_path]
    command_str = ' '.join(command_array)
    logger.warning(f'ABOUT TO RUN COMMAND: {command_str}')
    subprocess.run(command_array, check=True)

    # Check for more than 5 files in the dumps directory
    dump_files = sorted(os.listdir(dump_dir))

    while len(dump_files) > delete_after:
        # Remove the oldest file
        to_remove = dump_files[0]
        logger.warning(f'ABOUT DELETE FILE: {to_remove}')
        os.remove(os.path.join(dump_dir, to_remove))
        dump_files = sorted(os.listdir(dump_dir))

    logger.warning(f'Dump {file_path} created with success!')
