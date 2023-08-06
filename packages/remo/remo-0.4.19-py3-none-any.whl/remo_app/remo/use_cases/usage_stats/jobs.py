import psycopg2
import time

import django

import functools

import os
import signal
from threading import Thread, Event

from django.db.models import F
from django.utils import timezone
from django.db import close_old_connections, reset_queries

from remo_app.remo.models.downloads import LocalUsage, LocalStats
from remo_app.remo.services.stats import Stats
from remo_app.version import __version__


def safe():
    def wrapper(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except (django.db.utils.OperationalError, django.db.utils.InterfaceError, psycopg2.InterfaceError):
                    reset_queries()
                    close_old_connections()
                    time.sleep(1)

        return wrapper_func

    return wrapper


class Task:
    uuid = os.getenv('REMO_UUID', 'undefined')

    def on_start(self):
        pass

    def on_run(self):
        pass

    def on_stop(self):
        pass


class StoppableTask(Thread, Task):
    _stop_event = Event()

    def __init__(self):
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        super().__init__()

    def stop(self, *args, **krwars):
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()

    def sleep(self, seconds: int):
        self._stop_event.wait(seconds)

    def run(self):
        self.on_start()
        try:
            intervals = [1, 3, 5, 10, 30, 60]  # minutes
            for minutes in intervals:
                if self.is_stopped():
                    break
                self.sleep(minutes * 60)
                if not self.is_stopped():
                    self.on_run()

            two_hours = 2 * 60 * 60
            while not self.is_stopped():
                self.sleep(two_hours)
                if not self.is_stopped():
                    self.on_run()
        except KeyboardInterrupt:
            pass
        self.on_stop()


class PeriodicTask(StoppableTask):
    def __init__(self, seconds: int, callable):
        super().__init__()
        self.callable = callable
        self.seconds = seconds

    def run(self):
        self.on_start()
        try:
            while not self.is_stopped():
                self.sleep(self.seconds)
                if not self.is_stopped():
                    self.on_run()
        except KeyboardInterrupt:
            pass
        self.on_stop()

    def on_run(self):
        self.callable()


class PeriodicCheckDbConnection(PeriodicTask):
    def __init__(self, seconds: int, db):
        self.db = db
        super().__init__(seconds, self.check_db)

    def check_db(self):
        if not self.db.is_running():
            self.db.restart()
            reset_queries()
            close_old_connections()


class PeriodicBackupTask(StoppableTask):
    def __init__(self, seconds: int, db):
        super().__init__()
        self.db = db
        self.seconds = seconds

    def run(self):
        self.on_start()
        try:
            self.sleep(self.seconds)
            self.db.backup(force=True)

            while not self.is_stopped():
                self.sleep(self.seconds)
                if not self.is_stopped():
                    self.on_run()
        except KeyboardInterrupt:
            pass
        self.on_stop()

    def on_run(self):
        self.db.backup()


class UsageInfo(Task):
    def _new(self) -> LocalUsage:
        stats = LocalUsage.objects.create()
        stats.srv_id = f'{self.uuid}_{stats.id}'
        stats.version = __version__
        stats.save()
        return stats

    def _last(self) -> LocalUsage:
        stats = LocalUsage.objects.last()
        if stats:
            return stats
        return self._new()

    @safe()
    def on_start(self):
        self._new()
        self.send_data()

    @safe()
    def send_data(self):
        for stats in LocalUsage.objects.exclude(n_checks=F('synced_check')):
            self.sync(stats)

    @staticmethod
    def sync(stats: LocalUsage):
        ok = Stats.send_usage_info(
            stats.srv_id,
            stats.version,
            stats.started_at,
            stats.n_checks,
            last_check_at=stats.last_check_at,
            stopped_at=stats.stopped_at,
        )
        if ok:
            stats.synced_check = stats.n_checks
            stats.save()

    @safe()
    def on_run(self):
        stats = self._last()
        stats.check_usage()
        self.send_data()

    @safe()
    def on_stop(self):
        stats = self._last()
        stats.stopped_at = timezone.now()
        stats.save()
        self.sync(stats)


class StatsInfo(Task):
    def _new(self) -> LocalStats:
        stats = LocalStats.objects.create()
        stats.srv_id = f'{self.uuid}_{stats.id}'
        stats.save()
        return stats

    @safe()
    def on_start(self):
        stats = self._new()
        stats.collect_data()
        self.send_data()

    @safe()
    def send_data(self):
        for stats in LocalStats.objects.filter(synced=False):
            self.sync(stats)

    @staticmethod
    def sync(stats: LocalStats):
        ok = Stats.send_stats_info(
            stats.srv_id, stats.n_datasets, stats.dataset_stats, stats.annotation_set_stats,
        )
        if ok:
            stats.synced = True
            stats.save()

    @safe()
    def on_run(self):
        stats = self._new()
        stats.collect_data()
        self.send_data()

    @safe()
    def on_stop(self):
        stats = self._new()
        stats.collect_data()
        self.sync(stats)


class CollectInfo(StoppableTask):
    tasks = [StatsInfo(), UsageInfo()]

    def on_start(self):
        for task in self.tasks:
            task.on_start()

    def on_run(self):
        for task in self.tasks:
            task.on_run()

    def on_stop(self):
        for task in self.tasks:
            task.on_stop()


def collect_usage_info():
    worker = CollectInfo()
    try:
        worker.start()
        worker.join()
    except KeyboardInterrupt:
        pass


def run_periodic_backup(seconds: int, db):
    worker = PeriodicBackupTask(seconds, db)
    try:
        worker.start()
        worker.join()
    except KeyboardInterrupt:
        pass


def run_periodic_check_db_connection(seconds: int, db):
    worker = PeriodicCheckDbConnection(seconds, db)
    try:
        worker.start()
        worker.join()
    except KeyboardInterrupt:
        pass
