"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# AWS에 배포한 애플리케이션을 실행하고 서버를 작동시킬 때 WSGI가 사용된다.
# 로컬에서는 서버를 작동시키러면 python manage.py runserver를 사용하지만,
# 실제 AWS에서는 AWS가 django.config 파일 내에 설정된 WSGIPath를 보고
# 현재 WSGIPath로 설정되어 있는 지금 이 config.wsgi를 실행시켜 서버를 작동시킨다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
