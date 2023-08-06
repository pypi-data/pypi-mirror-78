import tempfile
import subprocess
from datetime import datetime

from .log import Log


class Shell:
    history = []

    @staticmethod
    def log_command(result: subprocess.CompletedProcess):
        Shell.history.append({
            'time': datetime.utcnow().isoformat(),
            'cmd': result.args,
            'return_code': result.returncode,
            'error': result.stderr,
            'output': result.stdout
        })

    @staticmethod
    def ok(cmd: str, show_command=False, show_output=False, exit_on_error=False) -> bool:
        """
        Runs command in shell

        Args:
            cmd: command to run
            show_command: print out command to console
            show_output: print out command output to console
            exit_on_error: exits on error if True

        Returns:
            True if succeeded
        """
        result = Shell.run(cmd, show_command=show_command, show_output=show_output, exit_on_error=exit_on_error)
        return result.returncode == 0

    @staticmethod
    def run(cmd: str, show_command=False, show_output=False, exit_on_error=False) -> subprocess.CompletedProcess:
        """
        Runs command in shell

        Args:
            cmd: command to run
            show_command: print out command to console
            show_output: print out command output to console
            exit_on_error: exits on error if True

        Returns:
            subprocess.CompletedProcess
        """
        if show_command:
            Log.msg(f"$ {cmd}")

        stdout = tempfile.TemporaryFile()
        stderr = tempfile.TemporaryFile()

        result = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=stdout, stderr=stderr, bufsize=65536)
        stdout.seek(0)
        stderr.seek(0)
        result.stdout = stdout.read().decode('utf-8').strip()
        result.stderr = stderr.read().decode('utf-8').strip()
        stdout.close()
        stderr.close()
        Shell.log_command(result)

        if show_output:
            Log.msg(result.stdout)

        if exit_on_error and result.returncode:
            Log.send_error(cmd, result.stderr, console_log=Shell.history)
            if not show_command:
                Log.msg(f"$ {cmd}")

            Log.exit(result.stderr)

        return result

    @staticmethod
    def output(cmd: str, show_command=False, exit_on_error=False) -> str:
        """
        Runs command in shell and return back result

        Args:
            cmd: command to run
            show_command:  print out command to console
            exit_on_error: exits on error if True

        Returns:
            command result as string
        """

        result = Shell.run(cmd, show_command=show_command, exit_on_error=exit_on_error)
        return result.stdout
