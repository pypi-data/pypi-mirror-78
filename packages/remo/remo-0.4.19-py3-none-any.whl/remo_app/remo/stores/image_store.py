from remo_app.remo.models import Dataset, DatasetImage, AnnotationSet, NewAnnotation


class ImageStore:

    @staticmethod
    def get_image(dataset_id: int, file_name: str) -> DatasetImage:
        return DatasetImage.objects.filter(dataset_id=dataset_id, original_name=file_name).first()

    @staticmethod
    def total_images_in_dataset(dataset_id: int):
        return DatasetImage.objects.filter(dataset_id=dataset_id).count()

    @staticmethod
    def images_with_annotations(annotation_set_id: int):
        return sum(
            1
            for item in NewAnnotation.objects.filter(
                annotation_set_id=annotation_set_id
            ).all()
            if item.has_annotation()
        )

    @staticmethod
    def images_without_annotations(annotation_set_id: int):
        annotation_set = AnnotationSet.objects.get(id=annotation_set_id)
        return ImageStore.total_images_in_dataset(annotation_set.dataset.id) - ImageStore.images_with_annotations(annotation_set_id)
