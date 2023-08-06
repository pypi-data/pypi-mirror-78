import json
from typing import Dict, List
from functools import lru_cache
# from concurrent.futures.thread import ThreadPoolExecutor

from django.db import connection

from remo_app.remo.models import AnnotationSet, Tag, Annotation, NewAnnotation
from remo_app.remo.use_cases.jobs.update_annotation_set_statistics import count_tags, \
    get_or_create_annotation_set_statistics


class TagStore:

    @staticmethod
    @lru_cache(maxsize=1000)
    def get_tag(name: str) -> Tag:
        name = name.strip().lower()
        if name:
            tag, _ = Tag.objects.get_or_create(name=name)
            return tag

    @staticmethod
    @lru_cache(maxsize=1000)
    def _get_or_create_annotation(image_id: int, annotation_set_id: int, dataset_id: int, task_type: str) -> int:
        annotation_id, created = TagStore._raw_get_or_create_annotation(image_id, annotation_set_id)
        if created:
            TagStore._raw_create_new_annotation(image_id, annotation_set_id, dataset_id, task_type)
        return annotation_id

    @staticmethod
    def _raw_create_new_annotation(image_id: int, annotation_set_id: int, dataset_id: int, task_type: str):
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO new_annotations (image_id, annotation_set_id, dataset_id, status, task, classes, tags, data)
            VALUES (%s, %s, %s, -1, %s, %s, %s, %s)
            ON CONFLICT (image_id, annotation_set_id) DO NOTHING
            """, [image_id, annotation_set_id, dataset_id, task_type, '[]', '[]', '{"objects": []}'])

    @staticmethod
    @lru_cache(maxsize=1000)
    def _raw_get_or_create_annotation(image_id: int, annotation_set_id: int) -> (int, bool):
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO annotations (image_id, annotation_set_id, created_at, updated_at, status)
            VALUES (%s, %s, now(), now(), -1)
            ON CONFLICT (image_id, annotation_set_id) DO NOTHING
            RETURNING *
            """, [image_id, annotation_set_id])
            entry = cursor.fetchone()
            if entry:
                return entry[0], True

            cursor.execute("""
            SELECT id
            FROM annotations
            WHERE image_id = %s AND annotation_set_id = %s
            """, [image_id, annotation_set_id])
            return cursor.fetchone()[0], False

    @staticmethod
    def _get_annotation(image, annotation_set):
        return Annotation.objects.filter(image=image, annotation_set=annotation_set).first()

    @staticmethod
    def _create_annotation(image, annotation_set):
        return Annotation.objects.create(
            image=image,
            annotation_set=annotation_set
        )

    @staticmethod
    def _create_new_annotation(annotation):
        NewAnnotation.create_empty_annotation(annotation)

    @staticmethod
    def update_annotation_set_tags_statistics(annotation_set: AnnotationSet):
        stat = get_or_create_annotation_set_statistics(annotation_set)
        stat.tags = count_tags(annotation_set.id)
        stat.save()

    @staticmethod
    def add_tag_to_image(image_id: int, annotation_set_id: int, dataset_id: int, task_type: str, name: str):
        tag = TagStore.get_tag(name)
        if not tag:
            return
        annotation_id = TagStore._get_or_create_annotation(image_id, annotation_set_id, dataset_id, task_type)
        TagStore._raw_create_annotation_tag(tag.id, image_id, annotation_id, annotation_set_id)

    @staticmethod
    def _raw_create_annotation_tag(tag_id: int, image_id: int, annotation_id: int, annotation_set_id: int):
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO annotation_tags (image_id, annotation_id, annotation_set_id, tag_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (annotation_id, tag_id) DO NOTHING
            """, [image_id, annotation_id, annotation_set_id, tag_id])

    @staticmethod
    def _raw_get_images(dataset_id: int, image_names: List[str]):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT id, original_name
            FROM dataset_images
            WHERE dataset_id = %s AND original_name IN %s
            """, [dataset_id, tuple(image_names)])
            return {item[1]: item[0] for item in cursor.fetchall()}

    @staticmethod
    def add_tags_to_annotation_set(image_tags: Dict[str, List[str]], annotation_set_id: int) -> List[str]:
        missing_images = set()
        annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
        annotation_set_id = annotation_set.id
        dataset_id = annotation_set.dataset.id
        task_type = annotation_set.task.type

        images = []
        image_dict = TagStore._raw_get_images(dataset_id, image_tags.keys())

        def _add_tags_to_image(item):
            img_name, tags = item
            img_id = image_dict.get(img_name)
            if not img_id:
                missing_images.add(img_name)
                return

            for tag in tags:
                TagStore.add_tag_to_image(img_id, annotation_set_id, dataset_id, task_type, tag)
            images.append((img_id, tags))

        # TODO: UNCOMMENT THIS LATER instead of list(map(...))
        # with ThreadPoolExecutor(max_workers=4) as executor:
        #     executor.map(_add_tags_to_image, image_tags.items())
        list(map(_add_tags_to_image, image_tags.items()))

        TagStore.update_annotation_set_tags_statistics(annotation_set)

        def _add_tags_new_annotation(item):
            img_id, tags = item
            TagStore._get_or_create_annotation(img_id, annotation_set_id, dataset_id, task_type)
            TagStore._raw_add_tags_to_new_annotation(img_id, annotation_set_id, tags)

        # TODO: UNCOMMENT THIS LATER instead of list(map(...))
        # with ThreadPoolExecutor(max_workers=4) as executor:
        #     executor.map(_add_tags_new_annotation, images)
        list(map(_add_tags_new_annotation, images))

        return list(missing_images)

    @staticmethod
    def _raw_add_tags_to_new_annotation(image_id: int, annotation_set_id: int, tags: List[str]):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT tags
            FROM new_annotations
            WHERE image_id = %s AND annotation_set_id = %s
            """, [image_id, annotation_set_id])
            existing_tags = cursor.fetchone()[0]

            new_tags = list(set(existing_tags).union(tags))

            cursor.execute("""
            UPDATE new_annotations
            SET tags = %s
            WHERE image_id = %s AND annotation_set_id = %s
            """, [json.dumps(new_tags), image_id, annotation_set_id])

