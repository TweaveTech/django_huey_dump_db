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