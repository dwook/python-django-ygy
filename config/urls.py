from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("master-admin/", admin.site.urls),
    path("", include("common.urls", namespace="common")),
    path("api/", include("api.urls", namespace="api")),
    path("users/", include("users.urls", namespace="users")),
    path("groups/", include("groups.urls", namespace="groups")),
    path("restaurants/", include("restaurants.urls", namespace="restaurants")),
    path("orders/", include("orders.urls", namespace="orders")),
]
# 로컬에서 static 또는 uploads의 파일들을 사용하기 위해 설정
# seetings에 DEBUG가 로컬은 True라 적용되지만, AWS는 DEBUG 환경변수가 없기 때문에 False
# 실제 AWS에 배포할 때는 별도로 파일 서버(S3)를 생성하고 거기에 올릴 것임
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
