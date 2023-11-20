from rest_framework import serializers
from django.conf import settings

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attrs):
        max_students = settings.MAX_STUDENTS_PER_COURSE
        try:
            if (
                self.context['request'].method in ['POST', 'PATCH', 'PUT'] and len(attrs['students']) > max_students or
                self.context['request'].method in ['PATCH', 'PUT'] and
                len(set(attrs['students'] + list(Student.objects.filter(course__id=self.instance.pk)))) > max_students
            ):
                raise serializers.ValidationError(detail=f"Students on course must be no more than 20", )
        except KeyError:
            pass
        return attrs

    def update(self, instance, validated_data):
        course = super().update(instance, validated_data)
        try:
            students = validated_data.pop('students')
            for student in students:
                course.students.add(student)
        except KeyError:
            pass
        return course
