import os
import platform
import subprocess
import sys

from .log import Log
from remo_app.config import get_remo_home


def install_cert_path():
    if os.getenv('CONDA_PREFIX'):
        return

    output = subprocess.check_output([sys.executable, '-m', 'certifi'])
    cert_path = output.decode("utf-8").strip()
    os.environ["SSL_CERT_FILE"] = cert_path
    os.environ["REQUESTS_CA_BUNDLE"] = cert_path


def setup_vips():
    if platform.platform() == 'Windows':
        vips_bin_path = str(os.path.join(get_remo_home(), 'libs', 'vips', 'vips-dev-8.8', 'bin'))
        if os.path.exists(vips_bin_path):
            os.environ["PATH"] = vips_bin_path + os.pathsep + os.environ["PATH"]
        else:
            Log.warn('vips library was not detected, try to run: python -m remo_app init', report=True)
