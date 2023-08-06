import json

import logging
import os
from multiprocessing import Process
import atexit

import requests

from . import postgres
from .config import Config
from .killer import is_port_in_use, try_to_terminate_another_remo_app, kill_background_process, terminate_electron_app
from .log import Log
from .shell import Shell
from ..config.config import CloudPlatformOptions


def delayed_browse(config, debug=False):
    if config.viewer == 'electron':
        from .viewer.electron import browse
    else:
        from .viewer.browser import browse

    url = build_url(config)
    browse(url, debug)


def build_url(config, initial_page='datasets'):
    page = initial_page.strip('/')
    return '{}/{}/'.format(config.get_host_address(), page)


def backup_job():
    from remo_app.config.standalone.wsgi import application
    from remo_app.remo.use_cases.usage_stats.jobs import run_periodic_backup
    run_periodic_backup(120, postgres.get_instance())


def check_db_connection_job():
    from remo_app.config.standalone.wsgi import application
    from remo_app.remo.use_cases.usage_stats.jobs import run_periodic_check_db_connection
    run_periodic_check_db_connection(5, postgres.get_instance())


def stop_db_server():
    pg = postgres.get_instance()
    if pg.is_need_to_stop:
        pg.stop()


def get_public_url():
    try:
        resp = requests.get('http://localhost:4040/api/tunnels').json()
        tunnels = resp.get('tunnels')
        if not tunnels:
            return

        url = tunnels[0].get('public_url')
        if url:
            return url.replace('http://', 'https://')
    except Exception:
        return


def run_server(config, debug=False, background_job=None, with_browser=True):
    debug = debug or config.debug
    if debug:
        os.environ['DJANGO_DEBUG'] = 'True'
    from remo_app.config.standalone.wsgi import application

    colab = config.cloud_platform == CloudPlatformOptions.colab
    if config.is_local_server() and is_port_in_use(config.port):
        if colab:
            Log.msg(f'Remo app running locally on http://localhost:{config.port}')
            public_url = get_public_url()
            if public_url:
                config.public_url = public_url
                config.save()
                Log.msg(f"""
You can access Remo from browser on {public_url}

To be able use Remo in Colab Notebook, do the following:
```
import remo

remo.open_ui()
```
""")
            return

        Log.error(f'Failed to start remo-app, port {config.port} already in use.', report=True)

        ok = try_to_terminate_another_remo_app(config)
        if not ok:
            Log.msg(f'You can change default port in config file: {Config.path()}')
            return
    else:
        terminate_electron_app()

    if config.is_local_server():
        processes = []

        if colab:
            backup_process = Process(target=backup_job)
            backup_process.start()
            processes.append(backup_process)
        else:
            check_db_connection_process = Process(target=check_db_connection_job)
            check_db_connection_process.start()
            processes.append(check_db_connection_process)

        if with_browser and not colab:
            ui_process = Process(target=delayed_browse, args=(config, debug), daemon=True)
            ui_process.start()
            processes.append(ui_process)

        background_process = Process(target=background_job)
        background_process.start()
        processes.append(background_process)

        atexit.register(stop_db_server)
        atexit.register(kill_background_process, *processes)

        start_server(application, config.port)

    else:
        Log.msg(f'Remo is running on remote server: {config.get_host_address()}')
        if with_browser:
            delayed_browse(config, debug)


def start_server(application, port: str = Config.default_port):
    from waitress import serve

    logging.basicConfig()
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.ERROR)

    Log.msg(f'Remo app running on http://localhost:{port}. Press Control-C to stop it.')
    serve(application, _quiet=True, port=port, threads=3)

