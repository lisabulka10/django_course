
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from common.views import HealthCheckView


schema_view = get_schema_view(
    openapi.Info(
        title="Polls API",
        default_version='v1',
        description="Polls application documentation",
    ),
    public=True
)

urlpatterns = [
    path("api/polls/", include("polls.urls")),
    path('api/universities/', include('university.urls')),
    path('admin/', admin.site.urls),
    path("healthcheck/", HealthCheckView.as_view(), name="healthcheck"),
    path("swagger.<format>/", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
