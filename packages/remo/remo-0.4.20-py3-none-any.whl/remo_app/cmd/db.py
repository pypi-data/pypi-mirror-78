import os

from .log import Log


def manage(argv):
    from django.core.management import execute_from_command_line

    argv = 'manage.py ' + argv
    argv = argv.split()
    execute_from_command_line(argv)


def migrate():
    Log.msg('* Prepare database')
    manage('migrate')


def is_database_uptodate():
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connections, DEFAULT_DB_ALIAS

    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)


def make_db_url(db):
    engine = db.get('engine')
    if engine != 'postgres':
        Log.exit(f"""Not supported DB engine - {engine}.

Please use 'postgres'.
""", report=True)

    host, name, password, port, user = db.get('host'), db.get('name'), db.get('password'), db.get('port'), db.get('user')
    return f'{engine}://{user}:{password}@{host}:{port}/{name}'


def set_db_url(url):
    os.environ['DATABASE_URL'] = url

