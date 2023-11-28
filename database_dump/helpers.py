import logging
from datetime import datetime
import os
import subprocess
from django.conf import settings

logger = logging.getLogger(__name__)

def make_database_dump(username=None, database_name=None, password=None, dump_dir=None):

    if username is None:
        username = settings.DATABASES['default']['USER']

    if database_name is None:
        database_name = settings.DATABASES['default']['NAME']

    if password is None:
        password = settings.DATABASES['default']['PASSWORD']

    if dump_dir is None:
        dump_dir = os.path.join(settings.BASE_DIR, 'dumps')

    # Ensure the dump directory exists
    os.makedirs(dump_dir, exist_ok=True)

    # Create the dump file name
    file_name = datetime.now().strftime('deployment_dump_%Y_%m_%d_%H:%M.sql')
    file_path = os.path.join(dump_dir, file_name)

    # Set the PGPASSWORD environment variable to avoid password prompt
    os.environ['PGPASSWORD'] = password

    command_array = ['pg_dump', '-h', 'localhost', '--username=' + username, '--dbname=' + database_name, '-F', 'c', '-Z', '9', '-f', file_path]
    command_str = ' '.join(command_array)
    logger.warning(f'ABOUT RUN COMMAND: {command_str}')
    subprocess.run(command_array, check=True)

    # Check for more than 5 files in the dumps directory
    dump_files = sorted(os.listdir(dump_dir))

    while len(dump_files) > 10:
        # Remove the oldest file
        to_remove = dump_files[0]
        logger.warning(f'ABOUT DELETE FILE: {to_remove}')
        os.remove(os.path.join(dump_dir, to_remove))
        dump_files = sorted(os.listdir(dump_dir))

    logger.warning(f'Dump {file_path} created with success!')
