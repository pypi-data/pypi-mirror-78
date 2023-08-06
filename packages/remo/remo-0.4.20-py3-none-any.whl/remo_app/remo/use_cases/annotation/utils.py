import os


def get_base_image_name(full_image_name: str):
    if not full_image_name:
        return ''
    return os.path.basename(full_image_name)
