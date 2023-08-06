import os
import platform
import time
from datetime import datetime

from .log import Log
from .installer import PostgresInstaller, Shell
from remo_app.remo.stores.version_store import Version
from .uuid import read_single_value_from_file, write_single_value_to_file
from ..config import get_remo_home


class WindowsPostgresInstaller(PostgresInstaller):
    def _stop(self) -> bool:
        return Shell.ok("pg_ctl stop", exit_on_error=True)

    def restart(self) -> bool:
        self._set_env_vars()
        if not Shell.ok("pg_ctl --version"):
            Log.exit('failed to restart postgres, pg_ctl was not found in the PATH', report=True)

        return Shell.ok("pg_ctl restart", show_command=True, show_output=True, exit_on_error=True)

    def is_running(self):
        return Shell.ok("psql -U postgres -l")

    def _launch(self):
        Log.msg("Launching postgres ... ", nl=False)

        for _ in range(2):
            if Shell.ok("pg_ctl start"):
                break
            time.sleep(2)

        if not Shell.ok("pg_ctl status"):
            Shell.ok("pg_ctl restart")
            time.sleep(2)

        if not Shell.ok("pg_ctl status"):
            Log.exit('failed to launch postgres', report=True)
        Log.msg("done")

    def _install(self):
        Shell.run("scoop install postgresql@12.2", show_command=True, exit_on_error=True)
        self._set_env_vars()

    def _create_db_and_user(self, dbname, username, password):
        Shell.run(
            f"""psql -U postgres -c "create user {username} with encrypted password '{password}';" """,
            show_command=True,
        )
        Shell.run(f"""psql -U postgres -c "create database {dbname};" """, show_command=True)
        Shell.run(
            f"""psql -U postgres -c "grant all privileges on database {dbname} to {username};" """,
            show_command=True,
        )
        return self.db_params(database=dbname, user=username, password=password)

    def _drop_db(self, database: str):
        Shell.run(f"""psql -U postgres -c "drop database {database};" """, show_output=True, exit_on_error=True)

    def _is_installed(self) -> bool:
        if self._is_psql_in_path():
            return True

        self._set_env_vars()
        return self._is_psql_in_path()

    def _is_psql_in_path(self) -> bool:
        return Shell.ok("psql --version")

    def _get_postgres_dir(self) -> str:
        for path in (
            '%PROGRAMFILES%\\PostgreSQL',
            '%PROGRAMFILES(x86)%\\PostgreSQL',
            '%USERPROFILE%\\scoop\\apps\\postgresql',
        ):
            full_path = os.path.expandvars(path)
            if os.path.exists(full_path):
                return full_path

    def _get_postgres_version_dir(self, postgres_dir: str) -> str:
        versions = os.listdir(postgres_dir)
        if len(versions) > 1:
            versions.sort(key=Version.to_num, reverse=True)
        return os.path.join(postgres_dir, versions[0])

    def _set_env_vars(self):
        path = self._get_postgres_dir()
        if not path:
            return

        postgres = self._get_postgres_version_dir(path)
        bin = os.path.join(postgres, 'bin')
        if os.path.exists(bin) and bin not in os.environ["PATH"]:
            os.environ["PATH"] = bin + os.pathsep + os.environ["PATH"]

        data = os.path.join(postgres, 'data')
        if os.getenv('PGDATA') and not os.path.exists(os.getenv('PGDATA')):
            os.environ.pop('PGDATA')
        if os.path.exists(data) and not os.getenv('PGDATA'):
            os.environ['PGDATA'] = data


class LinuxPostgresInstaller(PostgresInstaller):
    def _stop(self) -> bool:
        if not Shell.ok('sudo service postgresql stop'):
            return Shell.ok('sudo systemctl stop postgresql', exit_on_error=True)
        return True

    def restart(self) -> bool:
        if not Shell.ok('sudo service postgresql restart', show_command=True, show_output=True):
            return Shell.ok('sudo systemctl restart postgresql', show_command=True, show_output=True, exit_on_error=True)
        return True

    def _is_installed(self):
        return Shell.ok("psql --version")

    def _install(self):
        Shell.run('sudo apt-get install -y -qq postgresql', show_command=True)

    def is_running(self):
        return Shell.ok("service postgresql status")

    def _launch(self):
        Log.msg("Launching postgres ... ", nl=False)
        if not Shell.ok('sudo service postgresql start'):
            Shell.run('sudo systemctl start postgresql', exit_on_error=True)
        Log.msg("done")

    def _drop_db(self, database: str):
        Shell.run(f"""sudo -u postgres psql -c "drop database {database};" """, show_output=True, exit_on_error=True)

    def _create_db_and_user(self, dbname, username, password):
        Shell.run(
            f"""sudo -u postgres psql -c "create user {username} with encrypted password '{password}';" """,
            show_command=True,
        )
        Shell.run(f"""sudo -u postgres psql -c "create database {dbname};" """, show_command=True)
        Shell.run(
            f"""sudo -u postgres psql -c "grant all privileges on database {dbname} to {username};" """,
            show_command=True,
        )
        return self.db_params(database=dbname, user=username, password=password)

    def restore(self):
        backup_dir = os.path.join(get_remo_home(), 'backup')
        backup_db = os.path.join(backup_dir, 'remo.bak')
        os.makedirs(backup_dir, exist_ok=True)
        if os.path.exists(backup_db):
            Log.msg(f'Restoring Remo db from: {backup_db}')
            Shell.run(f"sudo -u postgres psql {self.dbname} < '{backup_db}'")

    def backup(self, force=False, skip_check=False):
        if not skip_check:
            backup_pid_path = os.path.join(get_remo_home(), 'backup', 'backup.pid')
            current_pid = str(os.getpid())

            if os.path.exists(backup_pid_path):
                pid_from_file = read_single_value_from_file(backup_pid_path)
                if not pid_from_file or force:
                    write_single_value_to_file(current_pid, backup_pid_path)
                elif pid_from_file != current_pid:
                    return
            else:
                write_single_value_to_file(current_pid, backup_pid_path)

        backup_dir = os.path.join(get_remo_home(), 'backup')
        backup_db = os.path.join(backup_dir, 'remo.bak')
        os.makedirs(backup_dir, exist_ok=True)
        if force and os.path.exists(backup_db):
            os.rename(backup_db, f'{backup_db} - {datetime.now()}')

        Log.msg('Backup Remo db')
        Shell.run(f"sudo -u postgres pg_dump {self.dbname} > '{backup_db}'", show_command=True, show_output=True)


class MacPostgresInstaller(PostgresInstaller):
    postgres_version = 'postgresql@10'

    def _get_postgres_homebrew_mxcl(self) -> str:
        postgres_exe_path = Shell.output('which postgres')
        postgres_dir = os.path.dirname(os.path.dirname(postgres_exe_path))
        files = list(filter(lambda name: name.startswith('homebrew'), os.listdir(postgres_dir)))
        if files:
            return os.path.join(postgres_dir, files[0])

    def _stop(self) -> bool:
        return Shell.ok(f'brew services stop {self._get_postgres_version()}', exit_on_error=True)

    def restart(self) -> bool:
        return Shell.ok(f'brew services restart {self._get_postgres_version()}', show_command=True, show_output=True, exit_on_error=True)

    def _is_installed(self):
        if Shell.ok("postgres --version"):
            return True
        self._add_postgres_to_path()
        return Shell.ok("postgres --version")

    def _get_postgres_version(self):
        files = list(filter(lambda name: name.startswith('postgresql'), os.listdir('/usr/local/Cellar/')))
        if files:
            return files[0]
        return self.postgres_version

    def _add_postgres_to_path(self):
        postgres_version = self._get_postgres_version()
        if os.path.exists(f'/usr/local/opt/{postgres_version}/bin'):
            os.environ['PATH'] = f"/usr/local/opt/{postgres_version}/bin:{os.getenv('PATH')}"

    def is_running(self):
        if Shell.ok("psql -l"):
            return True
        self._add_postgres_to_path()
        return Shell.ok("psql -l")

    def _install(self):
        Shell.run(f'brew install {self._get_postgres_version()}', show_command=True, exit_on_error=True)
        shell_exe_path = os.getenv('SHELL')
        shell_name = os.path.basename(shell_exe_path)
        shell_rc_path = os.path.expanduser(f'~/.{shell_name}rc')
        Shell.run(f"""echo 'export PATH="/usr/local/opt/{self._get_postgres_version()}/bin:$PATH"' >> {shell_rc_path}""", exit_on_error=True)
        self._add_postgres_to_path()

    def _launch(self):
        homebrew_mxcl = self._get_postgres_homebrew_mxcl()
        if not homebrew_mxcl:
            Log.exit_msg("Failed to launch postgres server, please start it manually.", report=True)

        Log.msg("Launching postgres ... ", nl=False)
        Shell.run(f'launchctl load {homebrew_mxcl}', exit_on_error=True)

        for _ in range(5):
            if self.is_running():
                break
            time.sleep(1)

        if not self.is_running():
            Shell.ok(f'brew services start {self._get_postgres_version()}', exit_on_error=True)
            for _ in range(5):
                if self.is_running():
                    break
                time.sleep(1)

        if self.is_running():
            Log.msg("done")
        else:
            Log.exit("Failed to launch postgres", report=True)

    def _drop_db(self, database: str):
        Shell.run(f'dropdb {database}', show_output=True, show_command=True)

    def _create_db_and_user(self, dbname, username, password):
        Shell.run('createdb $USER', show_command=True)
        Shell.run(
            f"""psql -c "create user {username} with encrypted password '{password}';" """, show_command=True
        )
        Shell.run(f'createdb {dbname} -O {username}', show_command=True)
        return self.db_params(database=dbname, user=username, password=password)


def get_instance() -> PostgresInstaller:
    installer = installers.get(platform.system())
    if not installer:
        Log.exit_warn(f'current operation system - {platform.system()}, is not supported.', report=True)

    return installer


installers = {
    'Windows': WindowsPostgresInstaller(),
    'Linux': LinuxPostgresInstaller(),
    'Darwin': MacPostgresInstaller(),
}
