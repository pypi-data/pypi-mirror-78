import os
import shutil

import requests

from .log import Log
from .shell import Shell


class ProgressBar:
    def __init__(self, text='Progress', total=100, response=None, full_bar_width=50):
        self.text = f'{text}:'
        self.total = total
        if response:
            content_size = self.content_size(response.headers)
            if content_size != -1:
                self.total = content_size
        self.full_bar_width = full_bar_width
        self.current_progress = 0

    def progress(self, progress=1):
        self.current_progress += progress
        self.show_progress(int(self.current_progress / self.total))

    def bar(self, percent: int):
        done = int((percent / 100) * self.full_bar_width)
        rest = self.full_bar_width - done
        return f"[{'#' * done}{' ' * rest}]"

    def show_progress(self, percent: int):
        end = '\n' if percent == 100 else '\r'
        print(f'{self.text} {self.bar(percent)} {percent}%  ', end=end)

    def done(self):
        self.show_progress(100)

    @staticmethod
    def content_size(headers):
        try:
            return int(headers.get('content-length'))
        except (KeyError, TypeError):
            return -1


class Download:
    def __init__(self, url, path, text, retries=3):
        if self.is_file_exists(path):
            return
        Log.msg(text)
        self.download(url, path, retries)

    def download(self, url, path, retries):
        self.makedir(path)

        for _ in range(retries):
            if not self.download_with_aria(url, path):
                self.download_fallback(url, path)
            if self.is_file_exists(path):
                break

        if not self.is_file_exists(path):
            Log.installation_aborted(f'failed to download file from URL {url} to location {path}', report=True)

    def makedir(self, path):
        dir_path, filename = os.path.split(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def is_file_exists(self, path) -> bool:
        return os.path.exists(path)

    def download_with_aria(self, url, path) -> bool:
        if not self.is_tool_exists('aria2c'):
            return False

        dir_path, filename = os.path.split(path)
        cmd = f'aria2c -d "{dir_path}" -o "{filename}" "{url}"'
        Shell.run(cmd, show_command=True)

        return self.is_file_exists(path)

    def download_fallback(self, url, path, chunk_size=1024 * 1024):
        with open(path, 'wb') as f:
            with requests.get(url, stream=True) as resp:
                bar = ProgressBar('Progress', total=60 * 1024 * 1024, response=resp)
                for chunk in resp.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)
                        bar.progress(len(chunk))

    @staticmethod
    def is_tool_exists(tool):
        return bool(shutil.which(tool))

