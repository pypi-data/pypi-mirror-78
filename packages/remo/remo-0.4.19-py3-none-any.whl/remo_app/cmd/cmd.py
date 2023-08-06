import requests
import time

import os
import typer

from . import postgres
from .db import migrate, is_database_uptodate, make_db_url, set_db_url
from .fmt import table
from .installer import get_instance
from .config import create_config, create_or_update_user
from .killer import list_and_confirm_kill_remo, is_remo_server_running
from .log import Log
from .logo import logo_msg, system_logo
from .runtime import install_cert_path, setup_vips
from .server import run_server, delayed_browse, get_public_url
from .checker import check_runtime_requirements
from .uuid import set_uuid
from .version import show_new_available_version
from remo_app import __version__
from remo_app.config import get_remo_home
from remo_app.config.config import Config, set_remo_home, default_colab_remo_home, default_remo_home, \
    ViewerOptions, CloudPlatformOptions
from remo_app.remo.services.stats import Stats

Log.set_reporter(Stats)


app = typer.Typer(add_completion=False, add_help_option=False)


def set_remo_home_from_default_remo_config() -> bool:
    if os.path.exists(Config.default_path()):
        config = Config.safe_load(Config.default_path(), exit_on_error=False)
        if config and config.remo_home:
            set_remo_home(config.remo_home)
            return True


def init_remo_home(colab: bool = False, remo_home: str = None, skip_dir_create=False):
    if not set_remo_home_from_default_remo_config():
        if not remo_home:
            remo_home = default_colab_remo_home if colab else default_remo_home
        set_remo_home(remo_home, skip_dir_create=skip_dir_create)


@app.command(add_help_option=False, options_metavar='')
def init(colab: bool = typer.Option(default=False), remo_home: str = typer.Option(default=None)):
    init_remo_home(colab, remo_home, skip_dir_create=True)
    init_remo_uuid()

    installer = get_instance(colab)
    if colab:
        if not installer.is_gdrive_mounted(get_remo_home()):
            Log.msg(f"""
We detected that Remo home dir not located on Google Drive.

To mount the Google Drive, do the following:
```
from google.colab import drive
drive.mount("/gdrive")
```
""")
            if typer.confirm("Do you want to stop initialization, and first mount GDrive?", default=True):
                raise typer.Exit()

    Log.msg('Initiailizing Remo:')
    Stats.start_installation(cloud_platform=CloudPlatformOptions.colab if colab else None)
    dependencies = installer.dependencies()
    if dependencies:
        fmt_deps_list = '\n   * '.join(dependencies)
        msg = f"""
This will download and install the following packages as needed: \n   * {fmt_deps_list}

Remo Terms of Service: https://remo.ai/docs/terms/

Do you want to continue with the installation of remo?"""
        if not typer.confirm(msg, default=True):
            Log.installation_aborted()

    db = postgres.get_instance()
    db_config = installer.install(postgres=db)
    db_url = make_db_url(db_config)
    set_db_url(db_url)
    if colab:
        db.restore()
    migrate()

    config = create_config(db_url, colab)
    if config.viewer == ViewerOptions.electron:
        installer.download_electron_app()

    Stats.finish_installation(successful=True)
    Log.msg(f"""

{logo_msg('Remo successfully initialiazed.')}
""")
    if not colab:
        Log.msg(f"""
You can launch remo using the command `python -m remo_app`
    """)
    else:
        installer.start()

        if config.port != Config.default_port:
            Log.msg("Don't need to change port, colab works with default port")
            config.port = Config.default_port
            config.save()

        url = f'http://localhost:{config.port}'
        for _ in range(10):
            time.sleep(1)
            if is_remo_running(url):
                break

        please_check_for_errors_msg = """please check for errors:

!supervisorctl status
!cat /var/log/remo_app.err.log"""

        if not is_remo_running(url):
            Log.exit(f'Failed to start remo app locally, {please_check_for_errors_msg}')


        Log.msg(f'Remo app running locally on {url}')
        for _ in range(10):
            time.sleep(1)
            if get_public_url():
                break

        if not get_public_url():
            Log.exit(f'Failed to retrieve ngrok public url, {please_check_for_errors_msg}')

        config.public_url = get_public_url()
        config.save()

        Log.msg(f"""
You can access Remo from browser on {config.public_url}

To be able use Remo in Colab Notebook, do the following:
```
import remo
remo.open_ui()
```
""")


def is_remo_running(url: str) -> bool:
    """
    Do check if remo app running

    :param url: expected 'http://localhost:8123'
    """
    try:
        resp = requests.get(f'{url}/api/version').json()
        return resp.get('app') == 'remo'
    except Exception:
        return False


@app.command(add_help_option=False, options_metavar='')
def backup():
    db = postgres.get_instance()
    db.backup(force=True, skip_check=True)


def run_jobs():
    from remo_app.remo.use_cases import jobs
    Log.msg('Running background jobs:')
    for job in jobs.all_jobs:
        job()


def collect_usage_stats():
    from remo_app.config.standalone.wsgi import application
    from remo_app.remo.use_cases.usage_stats.jobs import collect_usage_info
    collect_usage_info()


@app.command(add_help_option=False, options_metavar='')
def debug():
    config = Config.safe_load()
    run_server(config, debug=True, background_job=collect_usage_stats)


@app.command(add_help_option=False, options_metavar='')
def kill():
    config = Config.safe_load()
    list_and_confirm_kill_remo(config)


@app.command(add_help_option=False, options_metavar='')
def open():
    config = Config.safe_load()
    if is_remo_server_running(config):
        delayed_browse(config)
    else:
        Log.msg('Remo app is not running, you can run it with command: python -m remo_app')


@app.command(add_help_option=False, options_metavar='')
def remove_dataset():
    from remo_app.config.standalone.wsgi import application
    from remo_app.remo.models import Dataset
    datasets = Dataset.objects.all()
    if not datasets:
        Log.msg('No datasets found.')
        return

    Log.msg('List of existing datasets:')
    lookup = {}
    for ds in datasets:
        lookup[ds.id] = ds

    rows = [[str(ds.id), ds.name] for ds in datasets]
    Log.msg(table(['ID', 'Dataset name'], rows))

    confirm = input('\nType the dataset ID you want to delete, or type "all" to delete all of them: ')
    id = confirm.lower().strip()
    if id == 'all':
        for ds in lookup.values():
            delete_dataset(ds)
    else:
        try:
            id = int(id)
        except Exception as err:
            Log.exit(f'failed to parse dataset id: {err}', report=True)

        if id not in lookup:
            Log.exit('dataset id not found', report=True)

        delete_dataset(lookup[id])


def delete_dataset(ds):
    typer.echo(f'Deleting Dataset {ds.id} - {ds.name}... ', nl=False)
    ds.delete()
    typer.secho("DONE", fg=typer.colors.GREEN, bold=True)


@app.command(add_help_option=False, options_metavar='')
def delete():
    msg = "Do you want to delete all remo data and metadata?"
    if not typer.confirm(msg, default=True):
        Log.exit_msg('\nUninstallation aborted.')

    Log.msg('\nUninstalling Remo...')
    config = Config.safe_load()
    installer = get_instance()
    installer.uninstall(postgres.get_instance(), config.parse_db_params())
    Log.msg("""Remo data was successfully deleted

To completely remove remo, run:
$ pip uninstall remo""")


def version_callback(value: bool):
    if value:
        show_remo_version()
        raise typer.Exit()


def show_remo_version():
    Log.msg(system_logo)
    show_new_available_version()


def show_help_info():
    Log.msg(f"""
remo version: v{__version__}

Commands: you can use python -m remo_app with the following options:

  (no command)          - start server and open the default frontend
  no-browser            - start server

  init [options]        - initialize settings and download additional packages
  Options:
    --colab             - specify installation on Google Colab
    --remo-home <dir>   - set custom remo home dir location.
                          Default location: {default_remo_home},
                          on Colab default location: {default_colab_remo_home}

  kill                  - kill running remo instances
  open                  - open the Electron app
  remove-dataset        - delete datasets
  delete                - delete all the datasets and metadata
  backup                - create database backup

  --version             - show remo version
  --help                - show help info

""")


@app.command(add_help_option=False, options_metavar='')
def help():
    show_help_info()


@app.command(add_help_option=False, options_metavar='')
def version():
    show_remo_version()


def help_callback(value: bool):
    if value:
        show_help_info()
        raise typer.Exit()


@app.command(add_help_option=False, options_metavar='')
def no_browser():
    config = Config.safe_load()
    run_server(config, background_job=collect_usage_stats, with_browser=False)


def init_remo_uuid():
    if Config.is_exists():
        config = Config.safe_load()
        set_uuid(config.uuid)


@app.callback(invoke_without_command=True, options_metavar='', subcommand_metavar='')
def main(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True),
    help: bool = typer.Option(None, "--help", callback=help_callback, is_eager=True),
):
    init_remo_home()
    init_remo_uuid()

    if ctx.invoked_subcommand not in ('help', 'version', 'kill', 'backup'):

        os.environ["DJANGO_SETTINGS_MODULE"] = "remo_app.config.standalone.settings"
        Log.msg(system_logo)

        # check_installation_requirements()
        install_cert_path()

        if ctx.invoked_subcommand != 'init':
            if not Config.is_exists():
                Log.exit(f"""Remo not fully initialized, config file was not found at {get_remo_home()}.

Please run: python -m remo_app init
            """, report=True)

            setup_vips()

            config = Config.safe_load()
            if not config.db_url:
                Log.exit_msg("""
         You installed a new version of Remo that uses PostgreSQL database for faster processing.
         To use it, you need to run 'python -m remo_app init'.
WARNING: Your current data in SQLite database will be lost.

To proceed, just run: python -m remo_app init
                """)

            set_db_url(config.db_url)
            check_runtime_requirements(config.parse_db_params())

            from remo_app.config.standalone.wsgi import application
            if not is_database_uptodate():
                migrate()

            name, email, password = create_or_update_user(config.user_name, config.user_email, config.user_password)
            config.update(user_name=name, user_email=email, user_password=password)
            config.save()

    if ctx.invoked_subcommand is None:
        show_new_available_version()
        run_server(config, background_job=collect_usage_stats)
