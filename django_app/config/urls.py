from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # 앱 단위로 위임
    path("places/", include("places.urls", namespace="places")),
    path("api/", include("api.urls", namespace="api")),
]