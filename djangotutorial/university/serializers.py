from rest_framework import serializers
from .models import University, Course, UniversityCourse


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        read_only_fields = ["id"]
        fields = [
            "name",
            "country"
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ["id"]
        fields = [
            "id",
            "title",
            "description"
        ]


class UniversityCourseSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = UniversityCourse
        read_only_fields = ["id"]
        fields = [
            "id",
            "course",
            "university",
            "semester",
            "duration_weeks"
        ]


class CourseUniversitySerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = UniversityCourse
        read_only_fields = ["id"]
        fields = [
            "id",
            "course",
            "semester",
            "duration_weeks",
        ]


class CourseStatsSerializer(serializers.Serializer):
    total_courses = serializers.IntegerField()
    average_duration = serializers.FloatField()
