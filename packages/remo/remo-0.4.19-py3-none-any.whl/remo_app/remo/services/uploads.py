import os
import logging
import threading
from uuid import uuid4
from typing import List, Dict
from datetime import datetime
from multiprocessing import get_context
from multiprocessing.queues import Queue

from django.conf import settings

from remo_app.remo.api.constants import TaskType
from remo_app.remo.models import Dataset, ImageFolder
from remo_app.remo.services.processing import process_upload_session
from remo_app.remo.use_cases.annotation.class_encoding.class_encoding import AbstractClassEncoding
from remo_app.remo import utils

logger = logging.getLogger('remo_app')


class UploadErrors:
    def __init__(self, filename: str = ''):
        self.filename = filename
        self.errors: List[str] = []

    def to_dict(self) -> dict:
        return {'filename': self.filename, 'errors': self.errors}

    def add_errors(self, errors: List[str]):
        self.errors.extend(errors)

    def log_errors(self):
        if not self.errors:
            return

        msg = self.errors[0] if len(self.errors) == 1 else '\n * ' + '\n * '.join(self.errors)
        msg = f'{self.filename}: {msg}'
        logger.error(msg)


class UploadWarnings:
    def __init__(self, filename: str = ''):
        self.filename = filename
        self.warnings: List[str] = []

    def to_dict(self) -> dict:
        return {'filename': self.filename, 'warnings': self.warnings}

    def add_warnings(self, warnings: List[str]):
        self.warnings.extend(warnings)

    def log_warnings(self):
        if not self.warnings:
            return

        msg = self.warnings[0] if len(self.warnings) == 1 else '\n * ' + '\n * '.join(self.warnings)
        msg = f'{self.filename}: {msg}'
        logger.warning(msg)


class UploadDataInfo:
    def __init__(self, total: int = 0):
        self.pending = total
        self.total = total
        self.successful = 0
        self.failed = 0
        self.errors: Dict[str, UploadErrors] = {}
        self.warnings: Dict[str, UploadWarnings] = {}

    @property
    def rest(self) -> int:
        return self.total - self.pending

    def progress_status(self) -> str:
        return f'{self.rest} of {self.total}'

    def to_dict(self) -> dict:
        return {
            'pending': self.pending,
            'total': self.total,
            'successful': self.successful,
            'failed': self.failed,
            'errors': list(map(lambda item: item.to_dict(), self.errors.values())),
            'warnings': list(map(lambda item: item.to_dict(), self.warnings.values())),
        }

    def set_total(self, total: int = 0):
        self.total = total + self.failed
        self.pending = total

    def progress(self, n_items: int = 1):
        self.pending -= n_items

    def done(self, done: bool = True, n_items: int = 1, errors: Dict[str, List[str]] = None, warnings: Dict[str, List[str]] = None):
        if done:
            self.successful += n_items
        else:
            self.failed += n_items
        self.add_errors(errors)
        self.add_warnings(warnings)

    def add_errors(self, errors: Dict[str, List[str]] = None):
        if not errors:
            return

        for filename, errs in errors.items():
            upload_errors = self.errors.get(filename, UploadErrors(filename))
            upload_errors.add_errors(errs)
            self.errors[filename] = upload_errors

    def add_warnings(self, warnings: Dict[str, List[str]] = None):
        if not warnings:
            return

        for filename, warns in warnings.items():
            upload_warnings = self.warnings.get(filename, UploadWarnings(filename))
            upload_warnings.add_warnings(warns)
            self.warnings[filename] = upload_warnings

    def log_errors(self):
        for err in self.errors.values():
            err.log_errors()

    def log_warnings(self):
        for warn in self.warnings.values():
            warn.log_warnings()


class UploadStats:
    def __init__(self):
        self.items = 0
        self.size = 0

    def to_dict(self) -> dict:
        return {
            'items': self.items,
            'size': self.size,
            'human_size': utils.human_size(self.size)
        }

    def add_item(self, file_size: int):
        self.items += 1
        self.size += file_size


class UploadStatsInfo:
    def __init__(self):
        self.total = UploadStats()
        self.images = UploadStats()
        self.annotations = UploadStats()
        self.archives = UploadStats()

    def to_dict(self) -> dict:
        return {
            'total': self.total.to_dict(),
            'images': self.images.to_dict(),
            'annotations': self.annotations.to_dict(),
            'archives': self.archives.to_dict(),
        }

    def add_image(self, file_size: int):
        self.total.add_item(file_size)
        self.images.add_item(file_size)

    def add_annotation(self, file_size: int):
        self.total.add_item(file_size)
        self.annotations.add_item(file_size)

    def add_archive(self, file_size: int):
        self.total.add_item(file_size)
        self.archives.add_item(file_size)


class UploadSessionStatus:
    not_complete = 'not complete'
    pending = 'pending'
    in_progress = 'in progress'
    done = 'done'
    failed = 'failed'

    def __init__(self, id: str, dataset: Dataset, user, total_images: int = 0, total_annotations: int = 0):
        self.id = id
        self.created_at = datetime.now()
        self.finished_at = None

        self.status = self.not_complete
        self.status_details = ''
        self.images = UploadDataInfo(total_images)
        self.annotations = UploadDataInfo(total_annotations)
        self.errors = []
        self.warnings = []
        self.upload_stats = UploadStatsInfo()

        self.user = user
        self.dataset: Dataset = dataset
        self.annotation_task: TaskType = None
        self.annotation_set_id: int = None
        self.skip_new_classes: bool = None
        self.class_encoding: AbstractClassEncoding = None
        self.folder: ImageFolder = None
        self.urls: List[str] = []
        self.local_files: List[str] = []

        self.worker = None

    def get_substatus(self) -> str:
        if 'Processing images' in self.status_details:
            if self.status_details.find('filecount') != -1:
                return self.status_details.replace('filecount', self.images.progress_status())
            return f'{self.status_details}: {self.images.progress_status()} files'

        if 'Processing annotation files' in self.status_details:
            if self.status_details.find('filecount') != -1:    
                return self.status_details.replace('filecount', self.annotations.progress_status())
            return f'{self.status_details}: {self.annotations.progress_status()} files'

        return self.status_details

    def timestamp(self, timestamp):
        if not timestamp:
            return None
        return f'{timestamp.isoformat()}Z'

    def to_dict(self) -> dict:
        return {
            'session_id': self.id,
            'created_at': self.timestamp(self.created_at),
            'finished_at': self.timestamp(self.finished_at),
            'dataset': {'id': self.dataset.id, 'name': self.dataset.name} if self.dataset else {},
            'status': self.status,
            'substatus': self.get_substatus(),
            'images': self.images.to_dict(),
            'annotations': self.annotations.to_dict(),
            'errors': self.errors,
            'warnings': self.warnings,
            'uploaded': self.upload_stats.to_dict()
        }

    def uploaded(self, image_file_size: int = None, annotation_file_size: int = None, archive_file_size: int  = None):
        if image_file_size:
            self.upload_stats.add_image(image_file_size)
        if annotation_file_size:
            self.upload_stats.add_annotation(annotation_file_size)
        if archive_file_size:
            self.upload_stats.add_archive(archive_file_size)

    def dir_path(self):
        return os.path.join(settings.TMP_DIR, 'uploads', self.id)

    def can_append(self, dataset: Dataset, user) -> bool:
        if self.status != self.not_complete:
            return False

        if not (self.user and user and self.user.id == user.id):
            return False

        return bool(self.dataset and dataset and self.dataset.id == dataset.id)

    def append(
        self,
        dataset: Dataset = None,
        user=None,
        annotation_task: TaskType = None,
        annotation_set_id: int = None,
        skip_new_classes: bool = None,
        class_encoding: AbstractClassEncoding = None,
        folder: ImageFolder = None,
        urls: List[str] = None,
        url_errors: List[Dict[str, str]] = None,
        file_errors: List[Dict[str, str]] = None,
        url_warnings: List[Dict[str, str]] = None,
        file_warnings: List[Dict[str, str]] = None,
        local_files: List[str] = None,
        **kwargs,
    ):
        if not self.can_append(dataset, user):
            return

        if self.annotation_task is None:
            self.annotation_task = annotation_task

        if self.annotation_set_id is None:
            self.annotation_set_id = annotation_set_id

        if self.skip_new_classes is None:
            self.skip_new_classes = skip_new_classes

        if self.class_encoding is None:
            self.class_encoding = class_encoding

        if self.folder is None:
            self.folder = folder

        if urls:
            self.urls.extend(urls)

        if url_errors:
            self.errors.extend(url_errors)

        if file_errors:
            self.errors.extend(file_errors)

        if url_warnings:
            self.warnings.extend(url_warnings)

        if file_warnings:
            self.errors.extend(file_warnings)

        if local_files:
            self.local_files.extend(local_files)

    def set_total(self, images: int = 0, annotations: int = 0):
        self.images.set_total(images)
        self.annotations.set_total(annotations)

    def put_in_progress(self):
        if self.status != UploadSessionStatus.in_progress:
            self.status = UploadSessionStatus.in_progress

    def set_in_progress_details(self, details: str):
        self.status_details = details

    def done_progress(
        self,
        done: bool = True,
        images: int = 0,
        annotations: int = 0,
        image_errors: Dict[str, List[str]] = None,
        annotation_errors: Dict[str, List[str]] = None,
        image_warnings: Dict[str, List[str]] = None,
        annotation_warnings: Dict[str, List[str]] = None,
    ):
        self.images.done(done, images, image_errors, image_warnings)
        self.annotations.done(done, annotations, annotation_errors, annotation_warnings)

    def progress(
        self,
        images: int = 0,
        annotations: int = 0,
    ):
        self.images.progress(images)
        self.annotations.progress(annotations)

    def append_error(self, error=None):
        if error:
            self.errors.append({'type': 'error', 'error': str(error)})

    def append_warning(self, warning=None):
        if warning:
            self.warnings.append({'type': 'warning', 'warning': str(warning)})

    def append_file_error(self, filename: str, error: str):
        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        err = {filename: [error]}
        if extension in settings.IMAGE_FILE_EXTENSIONS:
            self.images.done(done=False, errors=err)
        elif extension in settings.ANNOTATION_FILE_EXTENSIONS:
            self.annotations.done(done=False, errors=err)
        else:
            self.errors.append({'type': 'file', 'value': filename, 'error': error})

    def append_file_warning(self, filename: str, warning: str):
        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        warn = {filename: [warning]}
        if extension in settings.IMAGE_FILE_EXTENSIONS:
            self.images.done(done=False, warnings=warn)
        elif extension in settings.ANNOTATION_FILE_EXTENSIONS:
            self.annotations.done(done=False, warnings=warn)
        else:
            self.warnings.append({'type': 'file', 'value': filename, 'warning': warning})

    def log_errors(self):
        for err in self.errors:
            msg = err["error"] if 'value' not in err else f'{err["value"]}: {err["error"]}'
            logger.error(msg)

        self.images.log_errors()
        self.annotations.log_errors()

    def log_warnings(self):
        for warn in self.warnings:
            msg = warn["warning"] if 'value' not in warn else f'{warn["value"]}: {warn["warning"]}'
            logger.warning(msg)

        self.images.log_warnings()
        self.annotations.log_warnings()

    def has_errors(self):
        return bool(self.errors or self.images.errors or self.annotations.errors)

    def has_warnings(self):
        return bool(self.warnings or self.images.warnings or self.annotations.warnings)

    def finish(self, error=None):
        self.finished_at = datetime.now()
        self.append_error(error)
        self.status = UploadSessionStatus.failed if self.has_errors() else UploadSessionStatus.done
        self.set_in_progress_details('')

        if not self.has_errors():
            logger.info('Data upload completed')
        else:
            logger.info('Data upload completed with some errors:')
            self.log_errors()

        if self.has_warnings():
            self.log_warnings()

    def start(self):
        if self.status != self.not_complete:
            return False
        self.status = self.pending

        ctx = get_context('spawn')
        queue = ctx.Queue()
        self.worker = ctx.Process(
            target=process_upload_session,
            args=(
                queue,
                self.user,
                self.dir_path(),
                self.local_files,
                self.dataset,
                self.folder,
                self.annotation_task,
                self.annotation_set_id,
                self.class_encoding,
                self.skip_new_classes,
                self.urls,
            ),
        )
        self.worker.start()
        threading.Thread(target=update_progress, args=(queue, self), daemon=True).start()
        return True


def update_progress(queue: Queue, session: UploadSessionStatus):
    while True:
        try:
            values = queue.get()
        except Exception as err:
            logger.error(f'Crashed progress updater thread: {err}')
            break

        if not isinstance(values, dict):
            continue

        if 'finish' in values:
            session.finish()
            return

        if 'in_progress' in values:
            session.put_in_progress()
            continue

        if 'in_progress_details' in values:
            session.set_in_progress_details(values['in_progress_details'])
            continue

        if 'total' in values:
            session.set_total(**values['total'])
            continue

        if 'progress' in values:
            session.progress(**values['progress'])
            continue

        if 'done' in values:
            session.done_progress(**values['done'])
            continue

        if 'error' in values:
            session.append_error(values['error'])
            continue

        if 'warning' in values:
            session.append_warning(values['warning'])
            continue


class Uploads:
    def __init__(self):
        self.lock = threading.Lock()
        self.sessions: Dict[str, UploadSessionStatus] = {}

    def get_session(self, id: str) -> UploadSessionStatus:
        with self.lock:
            return self.sessions.get(id)

    def list_sessions(self) -> List[UploadSessionStatus]:
        with self.lock:
            sessions = list(self.sessions.values())
            sessions.sort(key=lambda item: item.created_at, reverse=True)
            return sessions

    def get_or_create_session(self, session_id: str = None, dataset: Dataset = None, user=None) -> UploadSessionStatus:
        with self.lock:
            if session_id:
                return self.sessions.get(session_id)

            session_id = str(uuid4())
            while session_id in self.sessions or os.path.exists(os.path.join(settings.TMP_DIR, 'uploads', session_id)):
                session_id = str(uuid4())

            session = UploadSessionStatus(session_id, dataset, user)
            self.sessions[session_id] = session
            return session

    def start_session(self, id: str) -> bool:
        with self.lock:
            if id not in self.sessions:
                return False
            return self.sessions[id].start()

    def append_session(self, id: str, **kwargs):
        with self.lock:
            session = self.sessions.get(id)
            if session:
                session.append(**kwargs)


uploads = Uploads()
