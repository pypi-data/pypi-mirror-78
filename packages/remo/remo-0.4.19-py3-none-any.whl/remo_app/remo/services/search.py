from django.db import connection
from remo_app.remo.models import DatasetImage
from remo_app.remo.use_cases.query_builder import QueryBuilder, transform_filter_to_condition


class Direct:
    prev = 'prev'
    next = 'next'
    name = 'direction'
    operator = {
        prev: '<',
        next: '>',
    }

    @staticmethod
    def get_operator(direction):
        return Direct.operator.get(direction)

    @staticmethod
    def order(direction):
        return 'DESC' if direction == Direct.prev else 'ASC'


class Search:

    def raw_search(self, filters, dataset_id, folder_id, image_id, limit, direction, annotation_sets=None):
        """
        :return: image ids, total count
        """
        if filters:
            data, total_count = self.get_filtered_images(filters, direction, dataset_id, image_id, limit, annotation_sets)
        else:
            data, total_count = self.get_images(direction, dataset_id, image_id, folder_id, limit)

        return data, total_count

    def search_images(self, filters, dataset_id, folder_id, image_id, limit, direction, annotation_sets=None):
        image_ids, count = self.raw_search(filters, dataset_id, folder_id, image_id, limit, direction, annotation_sets)
        if not image_ids:
            return None, count
        queryset = DatasetImage.objects.raw(f"SELECT id FROM dataset_images WHERE id IN ({', '.join(map(str, image_ids))})")
        return queryset, count

    def get_filtered_images(self, filters, direction, dataset_id, image_id, limit, annotation_sets=None):
        if direction:
            ids = self._filter_image_ids_in_direction(filters, direction, dataset_id, image_id, limit, annotation_sets)
        else:
            ids = self._filter_image_ids(filters, dataset_id, image_id, limit, annotation_sets)

        count = self._count_filtered_images(filters, dataset_id, annotation_sets)
        return ids, count

    def get_images(self, direction, dataset_id, image_id, folder_id, limit):
        if direction:
            data = self._images_in_direction(direction, dataset_id, image_id, folder_id, limit)
        else:
            data = self._images(dataset_id, image_id, folder_id, limit)

        count = self._count_images(dataset_id, folder_id)
        return data, count

    def _query_count(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            count = cursor.fetchone()[0]
        return count

    def _query_ids(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            ids = cursor.fetchall()
        return [id[0] for id in ids]

    def _images_in_direction(self, direction, dataset_id, image_id, folder_id, limit, equal=False):
        qb = QueryBuilder("SELECT id, original_name FROM dataset_images")
        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))

        if folder_id:
            qb.condition(QueryBuilder.Condition("folder_id", "=", folder_id))

        if image_id:
            comparison = Direct.get_operator(direction)
            if equal:
                comparison += "="
            qb.condition(QueryBuilder.Condition("id", comparison, image_id))

        qb.order_by("id", Direct.order(direction))
        qb.limit(limit + 1)
        data = self._query_ids(qb.query())

        if direction == Direct.prev:
            data.reverse()

        return data

    def _count_images(self, dataset_id, folder_id):
        qb = QueryBuilder("SELECT COUNT(id) FROM dataset_images")
        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_id", "=", dataset_id))

        if folder_id:
            qb.condition(QueryBuilder.Condition("folder_id", "=", folder_id))

        return self._query_count(qb.query())

    def _images(self, dataset_id, image_id, folder_id, limit):
        if image_id:
            next = self._images_in_direction(Direct.next, dataset_id, image_id, folder_id, limit, equal=True)
            prev = self._images_in_direction(Direct.prev, dataset_id, image_id, folder_id, limit)
            return prev + next

        return self._images_in_direction(Direct.next, dataset_id, image_id, folder_id, limit)

    def _filter_image_ids_in_direction(self, filters, direction, dataset_id, image_id, limit, equal=False, annotation_sets=None):
        qb = QueryBuilder("""
        SELECT DISTINCT dataset_images.id FROM new_annotations
        RIGHT JOIN dataset_images ON new_annotations.image_id = dataset_images.id
        """)

        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_images.dataset_id", "=", dataset_id))

        if annotation_sets:
            qb.condition(QueryBuilder.Condition("new_annotations.annotation_set_id", "IN", f'({annotation_sets})'))

        if image_id:
            comparison = Direct.get_operator(direction)
            if equal:
                comparison += "="
            qb.condition(QueryBuilder.Condition("dataset_images.id", comparison, image_id))

        for filter in filters:
            qb.condition(transform_filter_to_condition(filter))

        qb.order_by("dataset_images.id", Direct.order(direction))
        qb.limit(limit + 1)

        query = qb.query()
        return self._query_ids(query)

    def _count_filtered_images(self, filters, dataset_id, annotation_sets=None):
        qb = QueryBuilder("""
        SELECT COUNT(DISTINCT dataset_images.id) FROM new_annotations
        RIGHT JOIN dataset_images ON new_annotations.image_id = dataset_images.id
        """)

        if dataset_id:
            qb.condition(QueryBuilder.Condition("dataset_images.dataset_id", "=", dataset_id))

        if annotation_sets:
            qb.condition(QueryBuilder.Condition("new_annotations.annotation_set_id", "IN", f'({annotation_sets})'))

        for filter in filters:
            qb.condition(transform_filter_to_condition(filter))

        return self._query_count(qb.query())

    def _filter_image_ids(self, filters, dataset_id, image_id, limit, annotation_sets=None):
        if image_id:
            next = self._filter_image_ids_in_direction(filters, Direct.next, dataset_id, image_id, limit, equal=True, annotation_sets=annotation_sets)
            prev = self._filter_image_ids_in_direction(filters, Direct.prev, dataset_id, image_id, limit, annotation_sets=annotation_sets)
            return prev + next

        return self._filter_image_ids_in_direction(filters, Direct.next, dataset_id, image_id, limit, annotation_sets=annotation_sets)





