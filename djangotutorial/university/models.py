from django.db import models


class University(models.Model):
    name = models.CharField(max_length=300)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.title


class UniversityCourse(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='university_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses_university')
    semester = models.CharField(max_length=50)
    duration_weeks = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'semester', 'university'], name='unique course and semester and university')
        ]

    def __str__(self):
        return f'{self.university}: {self.course}, {self.semester}, {self.duration_weeks} weeks'
