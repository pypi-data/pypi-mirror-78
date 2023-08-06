import os
import uuid
from functools import lru_cache
from pathlib import Path

UUID_VAR = 'REMO_UUID'
UUID_FILE_PATH = str(Path.home().joinpath('tmp', '.remo', 'uuid'))


@lru_cache()
def get_uuid() -> str:
    value = os.getenv(UUID_VAR)
    if value:
        return value
    value = read_uuid_from_file()
    if value:
        return value

    value = str(uuid.uuid4())
    os.environ[UUID_VAR] = value
    write_uuid_to_file(value)
    return value


def set_uuid(uuid: str):
    os.environ[UUID_VAR] = uuid
    write_uuid_to_file(uuid)


def write_uuid_to_file(uuid: str):
    write_single_value_to_file(uuid, UUID_FILE_PATH)


def read_uuid_from_file() -> str:
    return read_single_value_from_file(UUID_FILE_PATH)


def write_single_value_to_file(value: str, path: str):
    dir_name = os.path.dirname(path)
    os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w') as f:
        f.write(value)


def read_single_value_from_file(path: str) -> str:
    if os.path.exists(path):
        with open(path) as f:
            return f.readline()
