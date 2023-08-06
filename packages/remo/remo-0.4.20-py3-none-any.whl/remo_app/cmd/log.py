import sys
import traceback
from abc import ABCMeta
from typing import List

import typer


class ErrorReporter(metaclass=ABCMeta):
    @staticmethod
    def send_error(command: str = None, error: str = None, stacktrace: str = None, console_log: List = None):
        raise NotImplementedError()


class Log:
    reporter: ErrorReporter = None

    @staticmethod
    def set_reporter(reporter: ErrorReporter):
        Log.reporter = reporter

    @staticmethod
    def send_error(command: str = None, error: str = None, stacktrace: str = None, console_log: List = None):
        Log.reporter.send_error(command, error, stacktrace, console_log)

    @staticmethod
    def grab_stacktrace() -> str:
        exc_type, exc_value, exc_tb = sys.exc_info()
        return ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))

    @staticmethod
    def stacktrace(show_stacktrace=True):
        stacktrace = Log.grab_stacktrace()
        if show_stacktrace:
            Log.msg(stacktrace)
        Log.send_error(stacktrace=stacktrace)

    @staticmethod
    def exit_msg(msg: str, report=False, exception=False):
        Log.msg(msg, report=report, exception=exception)
        raise typer.Exit()

    @staticmethod
    def exit_warn(msg: str, report=False, exception=False):
        Log.exit(msg, status='WARNING', report=report, exception=exception)

    @staticmethod
    def exit(msg: str, status='ERROR', report=False, exception=False):
        Log.error(msg, status=status, report=report, exception=exception)
        Log.msg("""
If you need further help, you can also reach out to us at https://discuss.remo.ai - make sure to copy paste the error log above.
""")
        raise typer.Exit()

    @staticmethod
    def run_again(msg: str, report=False, exception=False):
        Log.exit(f"""{msg}
and then run again `python -m remo_app init`
""", report=report, exception=exception)

    @staticmethod
    def installation_aborted(msg: str = '', report=False, exception=False):
        Log.exit(f"""{msg}
Installation aborted.
""", report=report, exception=exception)

    @staticmethod
    def warn(msg: str, report=False, exception=False):
        Log.error(msg, status='WARNING', report=report, exception=exception)

    @staticmethod
    def error(msg: str, status='ERROR', report=False, exception=False):
        Log.msg(f'{status}: {msg}', report=report, exception=exception)

    @staticmethod
    def msg(msg: str, nl=True, report=False, exception=False):
        typer.echo(msg, nl=nl)
        kwargs = {}
        if report:
            kwargs['error'] = msg

        if exception:
            kwargs['stacktrace'] = Log.grab_stacktrace()

        if kwargs:
            Log.send_error(**kwargs)

    @staticmethod
    def stage(msg: str, marker='[-]'):
        Log.msg(f'\n{marker} {msg}')

    @staticmethod
    def completed(components_installed=True):
        msg_end = 'components installed' if components_installed else 'requirements already satisfied'
        Log.msg(f"\nCompleted - {msg_end}\n{'-' * 50}")
