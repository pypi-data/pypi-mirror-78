from django.conf import settings
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from queryset_sequence import QuerySetSequence
from django.db.models import Q
from rest_framework import serializers
from rest_framework.utils.urls import replace_query_param

from remo_app.remo.services.search import Search, Direct
from remo_app.remo.use_cases.annotation_tasks import parse_annotation_task
from remo_app.remo.use_cases.classes import capitalize_class_name

from remo_app.remo.api.viewsets import BaseNestedModelViewSet
from remo_app.remo.models import (
    Dataset,
    Annotation,
    NewAnnotation,
    DatasetImage,
    ImageFolder,
    ImageFolderStatistics,
    AnnotationSet,
)


class BriefUserDatasetFolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    dataset_id = serializers.IntegerField(source='dataset.id', read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    preview = serializers.SerializerMethodField()
    total_images = serializers.SerializerMethodField()
    top3_classes = serializers.SerializerMethodField()
    total_classes = serializers.SerializerMethodField()

    class Meta:
        model = ImageFolder
        fields = (
            'id',
            'name',
            'dataset_id',
            'updated_at',
            'created_at',
            'preview',
            'total_images',
            'top3_classes',
            'total_classes',
        )

    def get_preview(self, instance):
        img = instance.contents.first()
        if img:
            return img.image_object.preview.url if img.image_object.preview else None

        return None

    def get_total_images(self, instance):
        return instance.contents.count()

    def get_top3_classes(self, instance):
        stats = ImageFolderStatistics.objects.filter(image_folder=instance).first()
        if not stats:
            return []
        return stats.statistics.get('top3_classes', [])

    def get_total_classes(self, instance):
        stats = ImageFolderStatistics.objects.filter(image_folder=instance).first()
        if not stats:
            return 0
        return stats.statistics.get('total_classes', 0)


class DatasetImageSerializer(serializers.ModelSerializer):
    view = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    name = serializers.CharField(source='original_name')
    dimensions = serializers.SerializerMethodField()
    size_in_bytes = serializers.IntegerField(source='image_object.size')
    annotations = serializers.SerializerMethodField()

    class Meta:
        model = DatasetImage
        fields = ('id', 'view', 'preview', 'name', 'annotations', 'dimensions', 'size_in_bytes', 'created_at')

    def get_view(self, instance):
        return instance.view_url()

    def get_preview(self, instance):
        return instance.preview_url()

    def get_dimensions(self, instance):
        return [instance.image_object.width, instance.image_object.height]

    def get_annotations(self, instance):
        all_annotations = []
        indexes = {}
        annotation_sets = AnnotationSet.objects.filter(dataset=instance.dataset)
        for annotation_set in annotation_sets:
            indexes[annotation_set.id] = len(all_annotations)
            all_annotations.append(
                {
                    'annotation_set_id': annotation_set.id,
                    'coordinates': [],
                    'classes': [],
                    'object_classes': [],
                    'tags': [],
                }
            )

        annotation_sets = (
            Annotation.objects.filter(image=instance,).values_list('annotation_set__pk', flat=True).distinct()
        )

        for annotation_set_id in annotation_sets:
            annotations = self.get_annotation_set_annotations(instance, annotation_set_id)
            all_annotations[indexes[annotation_set_id]].update(annotations)

        return all_annotations

    def get_annotation_set_annotations(self, instance, annotation_set_id):
        coordinates, object_classes = self.get_coordinates(instance, annotation_set_id)
        annotations = {
            'coordinates': coordinates,
            'object_classes': object_classes,
            'classes': [],
            'tags': self.get_tags(instance, annotation_set_id),
        }

        if not coordinates:
            annotations['classes'] = self.get_classes(instance, annotation_set_id)

        return annotations

    def get_classes(self, instance, annotation_set_id):
        annotation = NewAnnotation.objects.filter(
            image=instance, annotation_set__pk=annotation_set_id
        ).first()

        classes = []
        if annotation and annotation.classes:
            classes = annotation.classes

        return classes


    def get_tags(self, instance, annotation_set_id):
        annotation = NewAnnotation.objects.filter(
            image=instance, annotation_set__pk=annotation_set_id
        ).first()

        tags = []
        if annotation and annotation.tags:
            tags = annotation.tags

        return tags

    def get_coordinates(self, instance, annotation_set_id):
        annotation = NewAnnotation.objects.filter(
            image=instance, annotation_set__pk=annotation_set_id
        ).first()

        coordinates = []
        object_classes = []
        if annotation and annotation.data and annotation.data.get('objects'):
            for obj in annotation.data.get('objects'):
                coordinates.append(obj.get('coordinates', []))
                object_classes.append(obj.get('classes', []))

        if len(coordinates) == 1 and len(coordinates[0]) == 0:
            coordinates = []

        return coordinates, object_classes


class DatasetContentsSerializer(serializers.Serializer):
    record_type = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()

    def get_record_type(self, instance):
        return self._get_instance_type(instance)

    def get_image(self, instance):
        if self._get_instance_type(instance) != 'image':
            return None

        return DatasetImageSerializer(instance, context=self.context).data

    def get_folder(self, instance):
        if self._get_instance_type(instance) != 'folder':
            return None

        return BriefUserDatasetFolderSerializer(instance, context=self.context).data

    def _get_instance_type(self, instance):
        types = {ImageFolder: 'folder', DatasetImage: 'image'}
        return types.get(type(instance))


class DatasetImageSearchContentsSerializer(serializers.Serializer):
    record_type = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()

    def get_record_type(self, instance):
        return "image"

    def get_image(self, instance):
        return DatasetImageSearchSerializer(instance, context=self.context).data

    def get_folder(self, instance):
        return None


class DatasetImageSearchSerializer(serializers.ModelSerializer):
    view = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    name = serializers.CharField(source='original_name')
    dimensions = serializers.SerializerMethodField()
    size_in_bytes = serializers.IntegerField(source='image_object.size')
    annotations = serializers.SerializerMethodField()

    class Meta:
        model = DatasetImage
        fields = ('id', 'view', 'preview', 'name', 'annotations', 'dimensions', 'size_in_bytes', 'created_at')

    def get_view(self, instance):
        return instance.view_url()

    def get_preview(self, instance):
        return instance.preview_url()

    def get_dimensions(self, instance):
        return instance.view_dimensions()

    def get_annotations(self, instance):
        # classes = set(self._context.get('classes'))
        annotation_sets = self._context.get('annotation_sets')
        if annotation_sets:
            annotation_sets = list(map(int, annotation_sets.split(',')))

        annotations = []

        for annotation in NewAnnotation.objects.filter(image=instance):
            if annotation_sets and annotation.annotation_set_id not in annotation_sets:
                continue

            data = {
                'annotation_set_id': annotation.annotation_set_id,
                'classes': annotation.classes,
                # 'classes': classes.intersection(annotation.classes),
                'tags': annotation.tags
            }

            coordinates = []
            object_classes = []
            for obj in annotation.data['objects']:
                obj_classes = obj.get('classes', [])
                # common = classes.intersection(obj_classes)
                # if not common:
                #     continue
                # object_classes.append(common)
                object_classes.append(obj_classes)
                coordinates.append(obj.get('coordinates', []))

            data['coordinates'] = coordinates
            data['object_classes'] = object_classes

            annotations.append(data)

        return annotations


class SearchDatasetContentsSerializer(serializers.Serializer):
    record_type = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    folder = serializers.SerializerMethodField()

    def get_record_type(self, instance):
        return "image"

    def get_image(self, instance):
        return SearchDatasetImageSerializer(instance, context=self.context).data

    def get_folder(self, instance):
        return None


class SearchDatasetImageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='image_id')
    view = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    name = serializers.CharField(source='image.original_name')
    dimensions = serializers.SerializerMethodField()
    size_in_bytes = serializers.IntegerField(source='image.image_object.size')
    annotations = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='image.created_at')

    class Meta:
        model = NewAnnotation
        fields = ('id', 'view', 'preview', 'name', 'annotations', 'dimensions', 'size_in_bytes', 'created_at')

    def get_view(self, instance):
        return instance.image.view_url()

    def get_preview(self, instance):
        return instance.image.preview_url()

    def get_dimensions(self, instance):
        return [instance.image.image_object.width, instance.image.image_object.height]

    def get_annotations(self, instance):
        coordinates = []
        object_classes = []
        classes = set()
        for obj in instance.data['objects']:
            coordinates.append(obj.get('coordinates', []))
            obj_classes = obj.get('classes')
            object_classes.append(obj_classes)

            if obj_classes:
                classes = classes.union(obj_classes)

        return [
            {
                'annotation_set_id': instance.annotation_set_id,
                'coordinates': coordinates,
                'object_classes': object_classes,
                'classes': list(classes),
            }
        ]


class DatasetContents(mixins.ListModelMixin, mixins.RetrieveModelMixin, BaseNestedModelViewSet):
    parent_lookup = 'datasets'
    serializer_class = DatasetContentsSerializer
    direct_name = 'direction'

    def get_parent_queryset(self):
        return Dataset.objects.filter(Q(user=self.request.user) | Q(is_public=True))

    def get_contents(self, folder_object=None):
        """
        Return contents of dataset folder
        :param folder_object: folder to list contents of, Default: root
        :return: Response object with paginated results
        """
        folders = ImageFolder.objects.filter(dataset=self.parent_pk)
        images = DatasetImage.objects.filter(dataset=self.parent_pk)

        if folder_object:
            images = images.filter(folder=folder_object)
        else:
            images = images.filter(folder__isnull=True)
        folders = folders.filter(parent=folder_object)

        queryset = QuerySetSequence(folders, images)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        image_id = self._parse_int_param(request.query_params.get('image_id'), min_value=1)
        dataset_id = self.parent_pk

        default_limit = settings.REST_FRAMEWORK['PAGE_SIZE']
        limit = self._parse_int_param(request.query_params.get('limit', default_limit), default_limit, 1)
        direction = request.query_params.get(self.direct_name)

        annotation_sets = request.query_params.get('sets')
        if annotation_sets:
            ids = annotation_sets.split(',')
            for id in ids:
                try:
                    int(id)
                except:
                    annotation_sets = None
                    break

        image_name = request.query_params.get('image_name')
        classes = request.query_params.get('classes')
        classes_not = request.query_params.get('classes_not')
        tags = request.query_params.get('tags')
        tags_not = request.query_params.get('tags_not')
        tasks = request.query_params.get('tasks')
        tasks_not = request.query_params.get('tasks_not')

        if classes or classes_not or tags or tags_not or tasks or tasks_not or image_name:
            filters, classes = self.build_filters(classes, classes_not, tags, tags_not, tasks, tasks_not, image_name)
            kw = {'context': {'request': self.request, 'view': self, 'annotation_sets': annotation_sets, 'classes': classes}}
            folder_id = None
            images, count = Search().search_images(filters, dataset_id, folder_id, image_id, limit, direction, annotation_sets)
            data = DatasetImageSearchContentsSerializer(images,  many=True, **kw).data
            resp = self._paginate_resp(data, count, limit, image_id, direction)
            return Response(resp)

        return self.get_contents(folder_object=None)

    def build_filters(self, classes=None, classes_not=None, tags=None, tags_not=None, tasks=None, tasks_not=None, image_names=None) -> list:
        if isinstance(image_names, str):
            image_names = image_names.split(',')

        if isinstance(classes, str):
            classes = classes.split(',')
        if isinstance(classes, list):
            classes = list(map(capitalize_class_name, classes))

        if isinstance(classes_not, str):
            classes_not = classes_not.split(',')
        if isinstance(classes_not, list):
            classes_not = list(map(capitalize_class_name, classes_not))

        if isinstance(tags, str):
            tags = tags.split(',')

        if isinstance(tags_not, str):
            tags_not = tags_not.split(',')

        if isinstance(tasks, str):
            tasks = tasks.split(',')
        if isinstance(tasks, list):
            # allowed only one task
            task = parse_annotation_task(tasks[0])
            tasks = [task.name] if task else []

        if isinstance(tasks_not, str):
            tasks_not = tasks_not.split(',')
        if isinstance(tasks_not, list):
            # allowed only one task
            task = parse_annotation_task(tasks_not[0])
            tasks_not = [task.name] if task else []

        filters = []
        if classes:
            for name in classes:
                if name:
                    filters.append({
                        'name': 'class',
                        'condition': 'is',
                        'pattern': name,
                    })

        if classes_not:
            for name in classes_not:
                if name:
                    filters.append({
                        'name': 'class',
                        'condition': 'is_not',
                        'pattern': name,
                    })

        if tags:
            for name in tags:
                if name:
                    filters.append({
                        'name': 'tag',
                        'condition': 'is',
                        'pattern': name,
                    })

        if tags_not:
            for name in tags_not:
                if name:
                    filters.append({
                        'name': 'tag',
                        'condition': 'is_not',
                        'pattern': name,
                    })
        if tasks:
            for name in tasks:
                if name:
                    filters.append({
                        'name': 'task',
                        'condition': 'is',
                        'pattern': name,
                    })

        if tasks_not:
            for name in tasks_not:
                if name:
                    filters.append({
                        'name': 'task',
                        'condition': 'is_not',
                        'pattern': name,
                    })

        if image_names:
            for name in image_names:
                if name:
                    filters.append({
                        'name': 'image_name',
                        'condition': 'contains',
                        'pattern': name,
                    })

        return filters, classes

    def _paginate_resp(self, data, count, limit, image_id, direction):
        next_url = None
        prev_url = None
        left, right = 0, len(data)
        if len(data) > limit:
            image_index = self._get_image_index(data, image_id)
            left, right = self.filter_range(image_index, limit, len(data))

        if left > 0 and direction != Direct.next:
            prev_url = self._create_url(data[left]['image']['id'], Direct.prev)
        if right < len(data) and direction != Direct.prev:
            next_url = self._create_url(data[right - 1]['image']['id'], Direct.next)

        results = data[left:right]

        return {'count': count, 'next': next_url, 'previous': prev_url, 'results': results}

    def _create_url(self, img_id, direction):
        current_url = self.request.get_full_path()
        url = replace_query_param(current_url, 'image_id', img_id)
        return replace_query_param(url, 'direction', direction)

    @staticmethod
    def _get_image_index(data, image_id):
        if not image_id:
            return

        for index, img in enumerate(data):
            if img['image_id'] >= image_id:
                return index

    @staticmethod
    def filter_range(img_idx: int, limit: int, size: int):
        if img_idx is None:
            return 0, limit

        half = int(limit / 2)
        left = img_idx - half
        right = img_idx + limit - half

        if left < 0:
            rest = -left
            left = 0
            right += rest
        elif right > size:
            rest = right - size
            right = size
            left -= rest

        return left, right

    @staticmethod
    def _parse_int_param(value, default=None, min_value: int = None):
        if value:
            try:
                value = int(value)
                if min_value:
                    value = max(value, min_value)
            except ValueError:
                value = default
        return value

    def retrieve(self, request, *args, **kwargs):
        # TODO: make walk contents/folder1/folder2/..., #333
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        fltr = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(ImageFolder, **fltr)
        return self.get_contents(obj)
