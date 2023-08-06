import logging

import sys
from datetime import datetime

from django.contrib import auth
from rest_auth.app_settings import TokenSerializer, create_token
from rest_auth.models import TokenModel
from remo_app.config.config import Config, CloudPlatformOptions

logger = logging.getLogger('remo_app')


class LocalUserMiddleware:
    def __init__(self, get_response):
        self._check_expiry_date()
        self.get_response = get_response
        self.password = None
        self.is_on_colab = False
        self._init_password()

    @staticmethod
    def _check_expiry_date():
        if datetime.now() > datetime.strptime('2020-10-01', '%Y-%m-%d'):
            print("""
            Current version is expired.
            Please contact hello@remo.ai to get new version.
            """)
            sys.exit(0)

    def _init_password(self):
        if Config.is_exists():
            config = Config.load()
            self.password = config.user_password
            self.is_on_colab = config.cloud_platform == CloudPlatformOptions.colab

    def _get_user_password(self):
        if not self.password:
            self._init_password()
        return self.password

    def _login_user(self, request):
        token = None
        if hasattr(request, 'user'):
            user = request.user
            try:
                User = auth.get_user_model()
                user = User.objects.filter(is_superuser=True).first()
                user = auth.authenticate(request, username=user.username, password=self._get_user_password())
                if user:
                    request.user = user
                    token = create_token(TokenModel, user, TokenSerializer)
                    auth.login(request, user)
            except Exception as err:
                logger.error(f'LocalUserMiddleware failed to login_user: {err}')

        return token

    def __call__(self, request):
        token = None
        url = request.path_info
        ignored = ['/version', '/static']
        if all(not url.startswith(prefix) for prefix in ignored) and 'authToken' not in request.COOKIES:
            token = self._login_user(request)

        # Code to be executed for each request/response after
        # the view is called.
        response = self.get_response(request)
        if token:
            response.cookies['authToken'] = token
            if self.is_on_colab:
                response.cookies['authToken']['samesite'] = 'None'
                response.cookies['authToken']['secure'] = True

        return response
