from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from .models import University, Course, UniversityCourse
from .serializers import UniversitySerializer, CourseSerializer, UniversityCourseSerializer, \
    CourseUniversitySerializer, CourseStatsSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    search_fields = ["title"]
    filterset_fields = {
        "id": ["in"],
        "title": ["exact", "contains"],
    }


class UniversityCourseViewSet(ModelViewSet):
    queryset = UniversityCourse.objects.all()
    serializer_class = UniversityCourseSerializer

    search_fields = ["course__title", "university__name"]
    ordering_fields = ["duration_weeks"]
    filterset_fields = {
        "id": ["in"],
        "course__title": ["exact", "contains"],
        "semester": ["exact", "contains"]
    }



class UniversityViewSet(ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    search_fields = ["name"]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return University.objects.all()
        else:
            return UniversityCourse.objects.filter(university_id=pk)

    @action(detail=True, methods=['get'], url_name='courses', serializer_class=UniversityCourseSerializer)
    def courses(self, request, pk=None):
        courses = UniversityCourse.objects.filter(university_id=pk)
        courses_serializer = self.get_serializer(courses, many=True)

        return Response(courses_serializer.data)

    @action(detail=True, methods=['get'], url_name='course-stats', serializer_class=CourseStatsSerializer)
    def course_stats(self, request, pk=None):
        courses = UniversityCourse.objects.filter(university_id=pk)

        total_count = courses.count()
        average_duration = courses.aggregate(avg_duration=Avg('duration_weeks'))['avg_duration'] or 0

        return Response({
            'total_count': total_count,
            'average_duration': average_duration
        })


class UniversityViewList(ListAPIView):
    serializer_class = CourseUniversitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["course__title"]
    ordering_fields = ["duration_weeks"]
    filterset_fields = {
        "id": ["in"],
        "course__title": ["exact", "contains"],
        "semester": ["exact", "contains"]
    }

    def get_queryset(self):
        university_id = self.kwargs["pk"]
        return UniversityCourse.objects.filter(university_id=university_id)
