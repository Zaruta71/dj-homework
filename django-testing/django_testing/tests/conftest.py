import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import *


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_bakery():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_bakery():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture(autouse=True)
def setting_student(settings):
    settings.MAX_STUDENTS_PER_COURSE = 5
    return settings.MAX_STUDENTS_PER_COURSE
