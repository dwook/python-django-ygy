from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("groups/", include("groups.urls", namespace="groups")),
    path("users/", include("users.urls", namespace="users")),
]
# 로컬에서 static 또는 uploads의 파일들을 사용하기 위해 설정
# 실제 AWS에 배포할 때는 별도로 파일 서버(S3)를 생성하고 거기에 올릴 것임
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
