import json
import logging
from datetime import timedelta
import iso8601

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from remo_app.remo.models.downloads import AgrStats, AgrInstallations, AgrUsage, AgrErrors

logger = logging.getLogger('remo_app')


class AggregateStats(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        return Response({'msg': 'Hello'})

    @staticmethod
    def client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]

        return request.META.get('REMOTE_ADDR', '')

    @staticmethod
    def parse_payload(request):
        try:
            data = json.loads(request.body)
        except Exception:
            return Response({'error': 'failed to parse payload'}, status=status.HTTP_400_BAD_REQUEST), None

        return None, data

    @staticmethod
    def parse_payload_with_srv_id(request, model):
        err, data = AggregateStats.parse_payload(request)
        if err:
            return err, None, None

        id = data.get('srv_id')
        if not id:
            return Response({'error': 'failed to parse srv_id'}, status=status.HTTP_400_BAD_REQUEST), data, None

        obj = model.objects.filter(id=id).first()
        if not obj:
            obj = model.objects.create(id=id)

        return None, data, obj

    @action(['post'], detail=True, url_path='stats')
    def stats(self, request, *args, **kwargs):
        err, data, stats = self.parse_payload_with_srv_id(request, AgrStats)
        if err:
            return err

        try:
            stats.uuid = data.get('uuid', '')
            stats.n_datasets = data.get('n_datasets', 0)
            stats.dataset_stats = data.get('dataset_stats', [])
            stats.annotation_set_stats = data.get('annotation_set_stats', [])

            stats.client_ip = self.client_ip(request)
            stats.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(['post'], detail=True, url_path='installations')
    def installations(self, request, *args, **kwargs):
        err, data = AggregateStats.parse_payload(request)
        if err:
            return err

        id = data.get('uuid')
        if not id:
            return Response({'error': 'failed to parse uuid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            finished = data.get('finished', False)
            stats = AgrInstallations.objects.filter(uuid=id).last() if finished else None
            if not stats:
                stats = AgrInstallations.objects.create(uuid=id)

            if finished:
                stats.successful = data.get('successful', False)
                stats.finished_at = timezone.now()
            else:
                stats.version = data.get('version', '')
                stats.platform = data.get('platform', '')
                stats.cloud_platform = data.get('cloud_platform', '')
                stats.python = data.get('python', '')
                stats.conda = data.get('conda', 'N/A')

            stats.client_ip = self.client_ip(request)
            stats.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def parse_timestamp(s: str):
        if not s:
            return None
        return iso8601.parse_date(s)

    @action(['post'], detail=True, url_path='usage')
    def usage(self, request, *args, **kwargs):
        err, data, stats = self.parse_payload_with_srv_id(request, AgrUsage)
        if err:
            return err

        try:
            stats.uuid = data.get('uuid', '')
            stats.version = data.get('version', '')
            started_at, stopped_at = self.parse_timestamp(data.get('started_at')), self.parse_timestamp(data.get('stopped_at'))
            last_check_at, n_checks = self.parse_timestamp(data.get('last_check_at')), data.get('n_checks', 0)
            stats.started_at = started_at

            stats.overall_duration = self.calc_overall_duration(started_at, stopped_at, last_check_at)
            stats.actual_usage = self.calc_actual_usage(n_checks)
            stats.synced_check = n_checks

            stats.client_ip = self.client_ip(request)
            stats.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def calc_overall_duration(started_at, stopped_at, last_check_at):
        if stopped_at:
            return stopped_at - started_at
        if last_check_at:
            return last_check_at - started_at

    @staticmethod
    def calc_actual_usage(n_checks):
        if n_checks <= 0:
            return None

        intervals = [1, 3, 5, 10, 30, 60]
        accumulated = [sum(intervals[:i+1]) for i in range(len(intervals))]

        minutes = accumulated[-1]
        if n_checks <= len(accumulated):
            minutes = accumulated[n_checks - 1]
        else:
            minutes += 120 * (n_checks - len(accumulated))

        return timedelta(minutes=minutes)

    @action(['post'], detail=True, url_path='errors')
    def errors(self, request, *args, **kwargs):
        err, data = AggregateStats.parse_payload(request)
        if err:
            return err

        id = data.get('uuid')
        if not id:
            return Response({'error': 'failed to parse uuid'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            AgrErrors.objects.create(
                uuid=id,
                version=data.get('version', ''),
                platform=data.get('platform', ''),
                python=data.get('python', ''),
                conda=data.get('conda', 'N/A'),
                shell_command=data.get('shell_command'),
                system_error=data.get('system_error'),
                stacktrace=data.get('stacktrace'),
                console_log=data.get('console_log', []),
                client_ip=self.client_ip(request),
            ).save()
            return Response(status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
