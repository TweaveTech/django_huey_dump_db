# django_huey_dump_db
A simple helper function that allow to create a dump of a current database

IMPORTANT! For now is working with only **PostgreSQL** database.

## Quickstart

1. Install the app via the git-url
2. add `database_dump` to the installed apps
3. Add the following settings to your django settings file:

```
	DATABASE_DUMP = {
		'crontab: {'minute:"*"},
		'path': '/my/path',
		'delete_after': 10,
	}
```

4. Whenever you want to generate a url: `from database_dump.helpers import make_database_dump`
5. You can give custom arguments to it or if is not provided it will get the required aguments from settings file.

## How to restore?

1. Make sure you login into psql and create a new database with CREATE DATABASE %database_name%;
2. There are 2 ways to restore the dump:

   - pg_restore -U %username% -h %hostname% -d %database_name% -v %dump_path%
   - psql %database_name% < %dump_path%

Try to use first one and if it gives any errors try the second one.

## Notes:

- Assumtion is made that postgres used > 11 as --no-comment is used
