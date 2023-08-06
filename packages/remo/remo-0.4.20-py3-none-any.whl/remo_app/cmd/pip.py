import os
import sys

from .log import Log
from .shell import Shell


def _get_pip_executable():
    python_dir = os.path.dirname(sys.executable)
    files = os.listdir(python_dir)
    for pip in ('pip', 'pip.exe', 'pip3', 'pip3.exe'):
        if pip in files:
            return os.path.join(python_dir, pip)

    if 'Scripts' in files:
        scripts_dir = os.path.join(python_dir, 'Scripts')
        for pip in ('pip.exe', 'pip3.exe'):
            if pip in os.listdir(scripts_dir):
                return os.path.join(scripts_dir, pip)

    pip_path = Shell.output('which pip')
    if os.path.exists(pip_path):
        return pip_path

    Log.exit('pip was not found', report=True)


class Pip:
    executable = _get_pip_executable()

    @staticmethod
    def run(command, package):
        if not Shell.ok(f'"{Pip.executable}" {command} {package}', show_command=True):
            Log.exit(f'pip failed to {command} {package}', report=True)

    @staticmethod
    def install(package):
        Pip.run('install', package)

    @staticmethod
    def uninstall(package):
        Pip.run('uninstall', package)
