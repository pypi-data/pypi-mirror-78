import os
import platform

from abc import abstractmethod, ABCMeta
from functools import lru_cache
from typing import List

import requests
from django.conf import settings

from remo_app.cmd.shell import Shell
from remo_app.cmd.uuid import get_uuid
from remo_app.version import __version__


@lru_cache()
def conda_version() -> str:
    if not os.getenv('CONDA_PREFIX', ''):
        return 'N/A'

    conda_exe = os.getenv('CONDA_EXE')
    if not conda_exe:
        return 'N/A'
    try:
        return Shell.output('conda --version', show_command=False)
    except:
        return 'N/A'


class Payload(metaclass=ABCMeta):
    @abstractmethod
    def to_dict(self):
        raise NotImplementedError()

    def timestamp(self, timestamp) -> str:
        if not timestamp:
            return None
        return timestamp.isoformat()


class InstallationData(Payload):
    def __init__(self, successful=False, finished=False, cloud_platform: str = None):
        self.uuid = get_uuid()
        self.version = __version__
        self.platform = platform.platform()
        self.cloud_platform = cloud_platform
        self.python = platform.python_version()
        self.conda = conda_version()
        self.successful = successful
        self.finished = finished

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'version': self.version,
            'platform': self.platform,
            'cloud_platform': self.cloud_platform,
            'python': self.python,
            'conda': self.conda,
            'successful': self.successful,
            'finished': self.finished,
        }


class StatsData(Payload):
    def __init__(self, srv_id: str, n_datasets: int, dataset_stats=[], annotation_set_stats=[]):
        self.uuid = get_uuid()
        self.srv_id = srv_id
        self.n_datasets = n_datasets
        self.dataset_stats = dataset_stats
        self.annotation_set_stats = annotation_set_stats

    def to_dict(self):
        return {
            'srv_id': self.srv_id,
            'uuid': self.uuid,
            'n_datasets': self.n_datasets,
            'dataset_stats': self.dataset_stats,
            'annotation_set_stats': self.annotation_set_stats,
        }


class UsageData(Payload):
    def __init__(self, srv_id: str, version: str, started_at, n_checks: int, last_check_at=None, stopped_at=None):
        self.uuid = get_uuid()
        self.srv_id = srv_id
        self.version = version
        self.started_at = started_at
        self.stopped_at = stopped_at
        self.last_check_at = last_check_at
        self.n_checks = n_checks

    def to_dict(self):
        return {
            'srv_id': self.srv_id,
            'uuid': self.uuid,
            'version': self.version,
            'started_at': self.timestamp(self.started_at),
            'stopped_at': self.timestamp(self.stopped_at),
            'last_check_at': self.timestamp(self.last_check_at),
            'n_checks': self.n_checks,
        }


class ErrorData(Payload):
    def __init__(self, command: str = None, error: str = None, stacktrace: str = None, console_log: List = None):
        self.uuid = get_uuid()
        self.version = __version__
        self.platform = platform.platform()
        self.python = platform.python_version()
        self.conda = conda_version()
        self.shell_command = command
        self.system_error = error
        self.stacktrace = stacktrace
        self.console_log = console_log

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'version': self.version,
            'platform': self.platform,
            'python': self.python,
            'conda': self.conda,
            'shell_command': self.shell_command,
            'system_error': self.system_error,
            'stacktrace': self.stacktrace,
            'console_log': self.console_log
        }


class Stats:
    @staticmethod
    def _send_request(endpoint: str, payload: Payload) -> bool:
        url = f'{settings.REMO_STATS_SERVER}/api/v1/ui/aggregate/1/{endpoint}/'
        try:
            resp = requests.post(url=url, json=payload.to_dict(), timeout=2)
            return resp.status_code == 200
        except:
            pass
        return False

    @staticmethod
    def _send_installation_info(payload: Payload) -> bool:
        return Stats._send_request('installations', payload)

    @staticmethod
    def send_stats_info(srv_id: str, n_datasets: int, dataset_stats=[], annotation_set_stats=[]) -> bool:
        return Stats._send_request('stats', StatsData(srv_id, n_datasets, dataset_stats, annotation_set_stats))

    @staticmethod
    def send_usage_info(srv_id: str, version: str, started_at, n_checks: int, last_check_at=None, stopped_at=None) -> bool:
        return Stats._send_request('usage', UsageData(srv_id, version, started_at, n_checks, last_check_at=last_check_at, stopped_at=stopped_at))

    @staticmethod
    def start_installation(cloud_platform: str = None):
        Stats._send_installation_info(InstallationData(cloud_platform=cloud_platform))

    @staticmethod
    def finish_installation(successful=False):
        Stats._send_installation_info(InstallationData(finished=True, successful=successful))

    @staticmethod
    def send_error(command: str = None, error: str = None, stacktrace: str = None, console_log: List = None):
        return Stats._send_request('errors', ErrorData(command, error, stacktrace, console_log))
