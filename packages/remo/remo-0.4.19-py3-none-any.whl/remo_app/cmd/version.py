import requests

from .log import Log
from remo_app.remo.stores.version_store import Version
from remo_app import __version__


def latest_remo_version():
    try:
        resp = requests.get(f'https://app.remo.ai/api/version?check-updates-for-version={__version__}').json()
        return resp.get('version'), resp.get('msg')
    except Exception:
        Log.stacktrace(show_stacktrace=False)


def is_new_version_available():
    result = latest_remo_version()
    if not result:
        return

    latest, msg = result
    if Version.to_num(latest) > Version.to_num(__version__):
        return latest, msg


def show_new_available_version():
    result = is_new_version_available()
    if not result:
        return

    new_version, msg = result
    if new_version:
        Log.msg(f"New version available: {new_version}. Run `pip install remo --upgrade` to install it\n")
    if msg:
        Log.msg(f'{msg}\n')

