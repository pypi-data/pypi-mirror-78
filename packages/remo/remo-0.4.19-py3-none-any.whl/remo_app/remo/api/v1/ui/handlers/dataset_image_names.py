from django.db.models import Q
from rest_framework.response import Response

from remo_app.remo.models import DatasetImage, Dataset
from remo_app.remo.api.viewsets import BaseNestedModelViewSet


class DatasetImageNames(BaseNestedModelViewSet):
    parent_lookup = 'datasets'

    def get_parent_queryset(self):
        return Dataset.objects.filter(
            Q(user=self.request.user) | Q(is_public=True),
            is_archived=False
        )

    def list(self, request, *args, **kwargs):
        names = sorted(list(
            DatasetImage.objects.filter(dataset_id=kwargs['datasets_pk'])
                .values_list('original_name', flat=True)
                .all()
        ))
        return Response({'names': names})
