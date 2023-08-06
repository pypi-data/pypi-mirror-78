import warnings
from typing import List
import shutil
import os
import time
import platform
import json
from pathlib import Path
import requests

from .downloader import Download
from .log import Log
from .pip import Pip
from .shell import Shell
from .viewer import electron
from remo_app.config import get_remo_home
from remo_app.remo.stores.version_store import Version
from remo_app.config.config import Config


class PostgresInstaller:
    username = 'remo'
    dbname = 'remo'
    userpass = 'remo'

    def __init__(self):
        self.is_need_to_stop = False

    @staticmethod
    def _install_psycopg2():
        Pip.install('psycopg2')

    @staticmethod
    def _is_installed_psycopg2():
        try:
            warnings.simplefilter("ignore")
            import psycopg2
        except Exception:
            return False
        return True

    def install(self) -> (dict, bool):
        installation_complete = False
        if not self._is_installed():
            self._install()
            installation_complete = self._is_installed()
        if not self._is_installed():
            Log.run_again('failed to install postgres, try to install it manually', report=True)

        if not self._is_installed_psycopg2():
            self._install_psycopg2()
        if not self._is_installed_psycopg2():
            Log.run_again(
                """failed to install psycopg2 pip package.
You can try to install it manually with `pip install psycopg2`""",
                report=True,
            )

        if not self.is_running():
            self._launch()

        db = self._create_db_and_user(self.dbname, self.username, self.userpass)
        db_params = json.dumps(db, indent=2, sort_keys=True)
        if not self.can_connect(self.dbname, self.username, self.userpass):
            Log.exit(
                f"""
Failed connect to database:
{db_params}
""",
                report=True,
            )

        Log.msg(
            f"""
Postgres database connection parameters:
{db_params}
"""
        )
        return db, installation_complete

    def on_start_check(self, db_params):
        if self.can_connect(**db_params):
            return

        if not self._is_installed():
            Log.exit(
                """postgres not installed

Please run: python -m remo_app init
""",
                report=True,
            )

        if not self.is_running():
            self._launch()

        if not self._is_installed_psycopg2():
            self._install_psycopg2()

        if not self.can_connect(**db_params):
            Log.exit(
                f"""failed connect to database.
Please check `db_url` value in config file: {Config.path()}.""",
                report=True,
            )

        self.is_need_to_stop = True

    @staticmethod
    def db_params(database='', user='', password='', host='localhost', port='5432'):
        return {
            'engine': 'postgres',
            'user': user,
            'password': password,
            'host': host,
            'port': port,
            'name': database,
        }

    @staticmethod
    def can_connect(database='', user='', password='', host='localhost', port='5432', **kwargs):
        try:
            warnings.simplefilter("ignore")
            import psycopg2

            conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        except Exception:
            Log.stacktrace(show_stacktrace=False)
            return False
        conn.close()
        return True

    def _is_installed(self):
        raise NotImplementedError()

    def is_running(self):
        raise NotImplementedError()

    def _launch(self):
        raise NotImplementedError()

    def _install(self):
        raise NotImplementedError()

    def _create_db_and_user(self, dbname, username, password):
        raise NotImplementedError()

    def _drop_db(self, database: str):
        raise NotImplementedError()

    def restart(self) -> bool:
        raise NotImplementedError()

    def stop(self):
        if not self._stop():
            Log.exit("failed to stop postgres server, please stop it manually.", report=True)

    def _stop(self) -> bool:
        raise NotImplementedError()

    def drop_database(self, db_params):
        if not self.restart():
            Log.exit('failed to drop remo database, unable to restart postgres', report=True)

        for _ in range(5):
            if self.can_connect(**db_params):
                break
            time.sleep(1)

        if self.can_connect(**db_params):
            self._drop_db(db_params.get('database'))
        else:
            Log.exit(
                f"""failed connect to database.
Please check that `db_url` value in the config file {Config.path()} is correct.""",
                report=True,
            )

    def backup(self, force=False, skip_check=False):
        Log.msg(f'Backup not implemented for OS: {platform.platform()}')

    def restore(self):
        Log.msg(f'Backup not implemented for OS: {platform.platform()}')


class OSInstaller:
    sqlite_url = ''
    vips_install_cmd = ''

    def get_sqlite_exe(self) -> str:
        return ''

    def is_gdrive_mounted(self, path: str) -> bool:
        pass

    def start(self):
        pass

    def install(self, postgres: PostgresInstaller):
        self.drop_electron_files()
        self.setup_remo_home()

        Log.stage('Installing OS specific tools')
        ok = self.install_os_specific_tools()
        Log.completed(ok)

        Log.stage('Installing vips lib')
        ok = self.install_vips()
        Log.completed(ok)

        Log.stage('Installing postgres')
        db_params, ok = postgres.install()
        Log.completed(ok)

        self.install_additional_packages()
        return db_params

    def uninstall(self, postgres: PostgresInstaller, db_params):
        Log.stage('Deleting database')
        postgres.drop_database(db_params)

        Log.stage('Deleting remo folder')
        self.delete_remo_home_folder()

    def install_os_specific_tools(self) -> bool:
        pass

    def install_vips(self) -> bool:
        installation_complete = False
        if not Shell.ok("vips -v"):
            Shell.run(self.vips_install_cmd, show_command=True)
            installation_complete = Shell.ok("vips -v")
        if not Shell.ok("vips -v"):
            Log.run_again(
                f"""failed to install vips library

You can try to install vips manually with the following command:
{self.vips_install_cmd}""",
                report=True,
            )
        return installation_complete

    def install_sqlite(self):
        if self.is_tool_exists('sqlite3'):
            return

        path = str(os.path.join(get_remo_home(), 'sqlite'))
        if not os.path.exists(path):
            os.makedirs(path)

        archive_path = os.path.join(path, 'sqlite.zip')
        if not os.path.exists(archive_path):
            Download(self.sqlite_url, archive_path, '* Downloading sqlite:')

            bin_path = str(os.path.join(path, 'bin'))
            if not os.path.exists(bin_path):
                os.makedirs(bin_path)
            Log.msg('* Extract sqlite')
            self.unzip(archive_path, bin_path)

        if os.path.exists(self.get_sqlite_exe()):
            os.environ["PATH"] = os.path.dirname(self.get_sqlite_exe()) + os.pathsep + os.environ["PATH"]
        else:
            Log.exit_warn(
                """automatic installation for SQLite failed. Please try to install it manually.
See instructions here https://www.sqlitetutorial.net/download-install-sqlite/""",
                report=True,
            )

    def unzip(self, archive_path: str, extract_path: str, retries: int = 3):
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path, ignore_errors=True)
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        for _ in range(retries):
            if self._unzip(archive_path, extract_path):
                break

        if not os.listdir(extract_path):
            Log.run_again(
                f"""failed to unzip {archive_path} into {extract_path}.
You can try to do it manually""",
                report=True,
            )

    def _unzip(self, archive_path: str, extract_path: str) -> bool:
        return Shell.ok(f'unzip -q "{archive_path}" -d "{extract_path}"', show_command=True)

    @staticmethod
    def is_tool_exists(tool):
        return bool(shutil.which(tool))

    @staticmethod
    def get_latest_available_electron_app_version():
        try:
            resp = requests.get(
                f'https://app.remo.ai/api/version?electron-app-platform={platform.system()}'
            ).json()
            return resp.get('version')
        except Exception:
            Log.stacktrace(show_stacktrace=False)

    @staticmethod
    def get_electron_app_version() -> str:
        path = electron.get_executable_path()
        if os.path.exists(path):
            return Shell.output(f'{path} --version')

    def is_new_electron_app_available(self) -> bool:
        latest = self.get_latest_available_electron_app_version()
        current = self.get_electron_app_version()
        return Version.to_num(latest) > Version.to_num(current)

    def download_electron_app(self):
        app_path = str(os.path.join(get_remo_home(), 'app'))
        if os.path.exists(app_path) and os.listdir(app_path):
            # skip if dir not empty
            return

        Log.stage('Installing electron app')

        archive_path = os.path.join(get_remo_home(), 'app.zip')
        if not os.path.exists(archive_path):
            url = 'https://app.remo.ai/download/latest?platform={}'.format(platform.system())
            Download(url, archive_path, '* Downloading remo app:')

        Log.msg('* Extract remo app')
        self.unzip(archive_path, app_path)

    def drop_electron_files(self):
        if not self.is_new_electron_app_available():
            return

        app_path = str(os.path.join(get_remo_home(), 'app'))
        if os.path.exists(app_path):
            shutil.rmtree(app_path, ignore_errors=True)

        archive_path = os.path.join(get_remo_home(), 'app.zip')
        if os.path.exists(archive_path):
            os.remove(archive_path)

    @staticmethod
    def setup_remo_home():
        remo_dir = get_remo_home()
        os.makedirs(remo_dir, exist_ok=True)
        Log.msg(f'Installing Remo to dir: {remo_dir}')

    def dependencies(self) -> list:
        return []

    def delete_remo_home_folder(self):
        if os.path.exists(get_remo_home()):
            shutil.rmtree(get_remo_home(), ignore_errors=True)
        if os.path.exists(get_remo_home()):
            self.delete_folder(get_remo_home())
        if os.path.exists(get_remo_home()):
            Log.warn(
                f'Remo dir {get_remo_home()} was not fully deleted, you can delete it manually', report=True
            )

    @staticmethod
    def delete_folder(path: str):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception as err:
                    Log.error(f'failed to delete file: {err}', report=True, exception=True)
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except Exception as err:
                    Log.error(f'failed to delete dir: {err}', report=True, exception=True)

    def install_additional_packages(self):
        pass


class WindowsInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-win32-x86-3310100.zip'

    def get_sqlite_exe(self) -> str:
        return str(os.path.join(get_remo_home(), 'sqlite', 'bin', 'sqlite-tools-win32-x86-3310100', 'sqlite3.exe'))

    def dependencies(self) -> list:
        return ['scoop', 'git', 'unzip', 'aria2', 'vips', 'postgres']

    def install_os_specific_tools(self) -> bool:
        self._add_scoop_to_path()
        scoop_installed = self.install_scoop()
        git_installed = self.install_tool_with_scoop('git', 'scoop install git')
        aria_installed = self.install_tool_with_scoop('aria2c', 'scoop install aria2')
        unzip_installed = self.install_tool_with_scoop('unzip', 'scoop install unzip')
        return any((scoop_installed, git_installed, aria_installed, unzip_installed))

    def install_scoop(self) -> bool:
        installation_complete = False

        if not self.is_tool_exists('scoop'):
            Log.stage('Installing scoop')

            Shell.run("""powershell.exe -Command "iwr -useb get.scoop.sh | iex" """, show_command=True)
            self._add_scoop_to_path()
            installation_complete = self.is_tool_exists('scoop')

        if not self.is_tool_exists('scoop'):
            Shell.run("""powershell.exe -Command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser; iex (new-object net.webclient).downloadstring('https://get.scoop.sh')" """, show_command=True)
            self._add_scoop_to_path()
            installation_complete = self.is_tool_exists('scoop')

        if not self.is_tool_exists('scoop'):
            Log.exit(
                """failed to install scoop - package manager.
You can try to install scoop manually. To do this, launch PowerShell and run the following commands:

----
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iex (new-object net.webclient).downloadstring('https://get.scoop.sh')
----

and then run again `python -m remo_app init`.

For more information, see:
- https://scoop.sh/
- https://www.onmsft.com/how-to/how-to-install-the-scoop-package-manager-in-windows-10""",
                report=True,
            )
        return installation_complete

    def install_tool_with_scoop(self, tool_name, install_cmd) -> bool:
        installation_complete = False
        if not self.is_tool_exists(tool_name):
            Shell.run(install_cmd, show_command=True)
            installation_complete = self.is_tool_exists(tool_name)
        if not self.is_tool_exists(tool_name):
            Log.run_again(
                f"""failed to install {tool_name}.
You can try to install {tool_name} manually.

Launch PowerShell and run the following command:
{install_cmd}""",
                report=True,
            )
        return installation_complete

    @staticmethod
    def _add_scoop_to_path():
        scoop_dir = os.path.expandvars('%userprofile%\\scoop\\shims')
        if os.path.exists(scoop_dir) and scoop_dir not in os.environ["PATH"]:
            os.environ["PATH"] = scoop_dir + os.pathsep + os.environ["PATH"]

    def install_vips(self):
        installation_complete = False
        vips_bin_dir = str(os.path.join(get_remo_home(), 'libs', 'vips', 'vips-dev-8.8', 'bin'))
        vips_bin_executable = os.path.join(vips_bin_dir, 'vips.exe')
        if not os.path.exists(vips_bin_executable):
            self.download_vips()
            installation_complete = os.path.exists(vips_bin_executable)
        if not os.path.exists(vips_bin_executable):
            Log.run_again(
                f"""failed to install vips library.
You can try to download vips archive and unpack it manually.

Do the following steps:
1. Download zip file: https://github.com/libvips/libvips/releases/download/v8.8.4/vips-dev-w64-web-8.8.4.zip
2. Unpack it to location: {str(os.path.join(get_remo_home(), 'libs', 'vips'))}
3. Check that you have binaries in: {vips_bin_dir}""",
                report=True,
            )
        os.environ["PATH"] = vips_bin_dir + os.pathsep + os.environ["PATH"]
        return installation_complete

    def download_vips(self):
        libs_path = str(os.path.join(get_remo_home(), 'libs'))
        archive_path = os.path.join(libs_path, 'vips.zip')
        url = 'https://github.com/libvips/libvips/releases/download/v8.8.4/vips-dev-w64-web-8.8.4.zip'
        Download(url, archive_path, '* Downloading vips lib:')

        vips_lib_path = str(os.path.join(libs_path, 'vips'))
        vips_bin_executable = os.path.join(vips_lib_path, 'vips-dev-8.8', 'bin', 'vips.exe')
        if not os.path.exists(vips_bin_executable):
            Log.msg('* Extract vips lib')
            self.unzip(archive_path, vips_lib_path)

    def _unzip(self, archive_path, extract_path) -> bool:
        if not (
            self._unzip_with_7z(archive_path, extract_path)
            or self._unzip_with_unzip(archive_path, extract_path)
        ):
            return self._unzip_fallback(archive_path, extract_path)
        return True

    def _unzip_with_7z(self, archive_path, extract_path) -> bool:
        if not self.is_tool_exists('7z'):
            return False
        return Shell.ok(f'7z x "{archive_path}" -o"{extract_path}"', show_command=True)

    def _unzip_with_unzip(self, archive_path, extract_path) -> bool:
        if not self.is_tool_exists('unzip'):
            return False
        return Shell.ok(f'unzip -q "{archive_path}" -d "{extract_path}"', show_command=True)

    def _unzip_fallback(self, archive_path, extract_path) -> bool:
        return Shell.ok(
            """powershell.exe -Command "Expand-Archive '{}' '{}'" """.format(archive_path, extract_path),
            show_command=True,
        )


class MacInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-osx-x86-3310100.zip'
    vips_install_cmd = 'brew install vips'

    def get_sqlite_exe(self) -> str:
        return str(os.path.join(get_remo_home(), 'sqlite', 'bin', 'sqlite-tools-osx-x86-3310100', 'sqlite3'))

    def dependencies(self) -> list:
        return ['brew', 'git', 'unzip', 'vips', 'postgres']

    def install_os_specific_tools(self) -> bool:
        if not Shell.ok("brew --version"):
            Log.run_again(
                """brew was not found.
Please install homebrew - package manager for macOS. See: https://brew.sh

Paste that in a macOS Terminal:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
""",
                report=True,
            )
        return False


class LinuxInstaller(OSInstaller):
    sqlite_url = 'https://www.sqlite.org/2020/sqlite-tools-linux-x86-3310100.zip'
    vips_install_cmd = 'sudo apt-get install -y -qq libvips-dev'

    def get_sqlite_exe(self) -> str:
        return str(os.path.join(get_remo_home(), 'sqlite', 'bin', 'sqlite-tools-linux-x86-3310100', 'sqlite3'))

    def dependencies(self) -> List[str]:
        return [
            'openssl',
            'apt-transport-https',
            'ca-certificates',
            'unzip',
            'libpq-dev',
            'python3-dev',
            'unzip',
            'vips',
            'postgres',
        ]

    def install_os_specific_tools(self) -> bool:
        Shell.run("sudo apt-get update -qq", show_command=True)
        Shell.run("sudo apt-get install -y -qq openssl", show_command=True)
        Shell.run(
            "sudo apt-get install -y -qq apt-transport-https ca-certificates unzip libpq-dev python3-dev",
            show_command=True,
        )
        return True


class ColabInstaller(LinuxInstaller):
    def is_gdrive_mounted(self, path: str) -> bool:
        p = Path(path)
        root_dir = p.parts[1]
        return Shell.ok(f"cat /proc/mounts | grep /{root_dir}")

    def dependencies(self) -> List[str]:
        deps = super().dependencies()
        deps.extend(['supervisor', 'ngrok'])
        return deps

    def install_additional_packages(self):
        Log.stage('Installing additional Colab packages')

        self.install_supervisor()
        self.create_colab_supervisor_conf()

        self.install_ngrok()
        self.create_ngrok_supervisor_conf()
        Log.completed()

    def create_colab_supervisor_conf(self):
        try:
            with open('/etc/supervisor/conf.d/remo_app.conf', 'w') as f:
                f.write(
                    f"""
[program:remo_app]
command=/usr/bin/python3 -m remo_app
stderr_logfile=/var/log/remo_app.err.log
stdout_logfile=/var/log/remo_app.out.log
"""
                )
        except Exception as err:
            Log.error(f'failed to create supervisor config for remo_app: {err}', report=True, exception=True)

    def create_ngrok_supervisor_conf(self):
        app_path = os.path.join(get_remo_home(), 'tools', 'ngrok', 'ngrok')
        Shell.run(f"sudo chmod +x '{app_path}'")
        try:
            with open('/etc/supervisor/conf.d/ngrok.conf', 'w') as f:
                f.write(
                    f"""
[program:ngrok]
command='{app_path}' http 8123
stderr_logfile=/var/log/ngrok.err.log
stdout_logfile=/var/log/ngrok.out.log
"""
                )
        except Exception as err:
            Log.error(f'failed to create supervisor config for ngrok: {err}', report=True, exception=True)

    def start(self):
        Shell.run("sudo service supervisor start")

    def install_supervisor(self):
        Log.msg('* Installing supervisor')
        Shell.run("sudo apt-get install -y supervisor", show_command=True)

    def install_ngrok(self):
        Log.msg('* Installing ngrok')
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
        archive_path = os.path.join(get_remo_home(), 'tools', 'ngrok-stable-linux-amd64.zip')
        Download(url, archive_path, '* Downloading ngrok:')

        dir_path = os.path.join(get_remo_home(), 'tools', 'ngrok')
        if not os.path.exists(os.path.join(dir_path, 'ngrok')):
            self.unzip(archive_path, dir_path)


def get_instance(colab: bool = False) -> OSInstaller:
    installer = (
        ColabInstaller
        if colab
        else {'Windows': WindowsInstaller, 'Linux': LinuxInstaller, 'Darwin': MacInstaller}.get(
            platform.system()
        )
    )

    if not installer:
        Log.exit_warn(f'current operation system - {platform.system()}, is not supported.', report=True)

    arch, _ = platform.architecture()
    if arch != '64bit':
        Log.exit_warn(f'current system architecture {arch}, is not supported.', report=True)

    if colab and platform.system() != 'Linux':
        Log.exit_warn('Colab option works only for linux', report=True)

    return installer()
