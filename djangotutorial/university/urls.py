from rest_framework.routers import DefaultRouter
from django.urls import include, path
from . import views

router = DefaultRouter()
router.register("university", views.UniversityViewSet)
router.register("course", views.CourseViewSet)
router.register("university-course", views.UniversityCourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/courses/", views.UniversityViewList.as_view())
]