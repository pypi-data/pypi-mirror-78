from django.db import models
from django.utils import timezone
from jsonfield import JSONField

from remo_app.remo.stores.collect_stats import UsageStats


class Download(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=1000, null=True)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'downloads'


class UserVersion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=20, null=True)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'user_versions'


class LocalUsage(models.Model):
    # srv_id = uuid_id
    srv_id = models.CharField(max_length=50, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=20, null=True)
    last_check_at = models.DateTimeField(null=True)
    n_checks = models.PositiveIntegerField(default=0)
    stopped_at = models.DateTimeField(null=True)
    synced_check = models.IntegerField(default=-1)

    class Meta:
        db_table = 'local_usage'

    def check_usage(self):
        """ On save, update timestamps """
        self.last_check_at = timezone.now()
        self.n_checks += 1
        return self.save()


class LocalStats(models.Model):
    # srv_id = uuid_id
    srv_id = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    n_datasets = models.PositiveIntegerField(default=0)
    # dataset_stats = [
    #   {n_images: int, size_in_bytes: int, n_annotation_sets: int},
    # ]
    dataset_stats = JSONField(null=True)
    # annotation_set_stats = [
    #   {task: str, n_classes: int, n_objects: int, n_tags: int},
    # ]
    annotation_set_stats = JSONField(null=True)
    synced = models.BooleanField(default=False)

    class Meta:
        db_table = 'local_stats'

    def collect_data(self):
        self.n_datasets, self.dataset_stats, self.annotation_set_stats = UsageStats.collect_stats()
        self.save()


class AgrInstallations(models.Model):
    uuid = models.CharField(max_length=50, null=True)
    version = models.CharField(max_length=20, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)
    successful = models.BooleanField(default=False)
    platform = models.CharField(max_length=50, null=True)
    cloud_platform = models.CharField(max_length=50, null=True)
    python = models.CharField(max_length=20, null=True)
    conda = models.CharField(max_length=20, null=True)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'agr_installations'


class AgrUsage(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    uuid = models.CharField(max_length=50, null=True)
    version = models.CharField(max_length=20, null=True)
    started_at = models.DateTimeField(null=True)
    overall_duration = models.DurationField(null=True)
    actual_usage = models.DurationField(null=True)
    synced_check = models.IntegerField(default=-1)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'agr_usage'


class AgrStats(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    uuid = models.CharField(max_length=50, null=True)
    snapshot_time = models.DateTimeField(auto_now_add=True)
    n_datasets = models.PositiveIntegerField(default=0)
    # dataset_stats = [
    #   {n_images: int, size_in_bytes: int, n_annotation_sets: int},
    # ]
    dataset_stats = JSONField(null=True)
    # annotation_set_stats = [
    #   {task: str, n_classes: int, n_objects: int, n_tags: int},
    # ]
    annotation_set_stats = JSONField(null=True)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'agr_stats'


class AgrErrors(models.Model):
    uuid = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=20, null=True)
    platform = models.CharField(max_length=50, null=True)
    python = models.CharField(max_length=20, null=True)
    conda = models.CharField(max_length=20, null=True)
    shell_command = models.TextField(null=True)
    system_error = models.TextField(null=True)
    stacktrace = models.TextField(null=True)
    console_log = JSONField(null=True)
    client_ip = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'agr_errors'
