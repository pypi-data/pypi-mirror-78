from remo_app.remo.models import Dataset, AnnotationSetStatistics


class UsageStats:
    @staticmethod
    def collect_stats():
        n_datasets = Dataset.objects.count()
        dataset_stats = [{
                'dataset_id': dataset.id,
                'n_images': dataset.quantity,
                'size_in_bytes': dataset.size_in_bytes,
                'n_annotation_sets': dataset.annotation_sets.count()
            } for dataset in Dataset.objects.all()]

        def calc_tag_objects(tags):
            if len(tags) == 0:
                return 0
            return sum(pair[1] for pair in tags)

        annotation_set_stats = [{
            'dataset_id': stat.dataset.id,
            'n_images': stat.dataset.quantity,
            'images_stats': {
                'annotated': stat.total_annotated_images,
                'done': stat.done_images,
                'on_hold': stat.skipped_images,
                'todo': stat.todo_images,
            },
            'task': stat.annotation_set.task.name,
            'n_classes': stat.total_classes,
            'n_objects': stat.total_annotation_objects,
            'n_tags': len(stat.tags),
            'n_tag_objects': calc_tag_objects(stat.tags),
        } for stat in AnnotationSetStatistics.objects.all()]

        return n_datasets, dataset_stats, annotation_set_stats
