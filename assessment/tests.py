import time
from datetime import timedelta
from unittest import TestCase
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.test import APIRequestFactory, APITestCase

from assessment.models import Student, PracticalWork
from assessment.services.students_service import StudentsService
from assessment.services.work_check_service import WorkCheckService
from assessment.views import StudentsViewSet


# Unit тесты
class StudentServiceTests(TestCase):
    def setUp(self) -> None:
        self.service = StudentsService()

        self.student = Student(name='John', last_name='Wick')
        self.student.save()

    def test_add_student(self):
        student = Student(name='Water', last_name='Rock')
        added_student = self.service.add_student(student)
        self.assertEqual(student, added_student)

    def test_get_student_success(self):
        id = self.student.id
        found_student = self.service.get_student(id)
        self.assertEqual(self.student, found_student)

    def test_get_student_not_found(self):
        id = uuid.uuid4()
        with self.assertRaises(Student.DoesNotExist):
            self.service.get_student(id)


class WorkCheckServiceTests(TestCase):
    def setUp(self) -> None:
        self.service = WorkCheckService()

        self.student = Student(name='John', last_name='Wick')
        self.student.save()

        self.work = PracticalWork(student_id=self.student.id, title="Test title", file='Uploaded Files/test_work.txt')
        self.work.save()

    def test_add_work(self):
        work = PracticalWork(student_id=self.student.id, title="New Title", file='Uploaded Files/test_work.txt')
        added_work = self.service.add_work(work)
        self.assertEqual(work, added_work)

    def test_get_work(self):
        id = self.work.id
        found_work = self.service.get_work_by_id(id)
        self.assertEqual(self.work, found_work)

    def test_get_work_not_found(self):
        id = uuid.uuid4()
        with self.assertRaises(PracticalWork.DoesNotExist):
            self.service.get_work_by_id(id)

    def test_mark_work(self):
        self.service.mark_work(self.work.id, 50)
        self.assertEqual(PracticalWork.objects.get(id=self.work.id).mark, 50)

    def test_mark_work_invalid(self):
        with self.assertRaises(ValueError):
            self.service.mark_work(self.work.id, 124124)

    def test_get_submitted_works(self):
        work1 = PracticalWork(student_id=self.student.id, title="New Title1", file='Uploaded Files/work1.txt')
        work1.save()
        work2 = PracticalWork(student_id=self.student.id, title="New Title2", file='Uploaded Files/work2.txt')
        work2.save()
        works = [self.work, work1, work2]
        works_ids = list(map(lambda x: x.id, works)).sort()
        returned_works = self.service.get_submitted_works(offset=0, limit=3)
        returned_works_ids = list(map(lambda x: x.id, returned_works)).sort()
        self.assertEqual(works_ids, returned_works_ids)

    def test_get_submitted_works_by_student_id(self):
        student = Student(name='TestName', last_name="TestLastName")
        student.save()
        work1 = PracticalWork(student_id=student.id, title="New Title1", file='Uploaded Files/work1.txt')
        work1.save()
        work2 = PracticalWork(student_id=student.id, title="New Title2", file='Uploaded Files/work2.txt')
        work2.save()

        returned_works = self.service.get_submitted_works(offset=0, limit=3, student_id=student.id)
        self.assertEqual(len(returned_works), 2)

    def test_get_submitted_works_by_date(self):
        student = Student(name='TestName2', last_name="TestLastName2")
        student.save()

        work1 = PracticalWork(student_id=student.id, title="Old1", file='Uploaded Files/work1.txt')
        work1.save()
        work2 = PracticalWork(student_id=student.id, title="Old2", file='Uploaded Files/work2.txt')
        work2.save()

        returned_works = self.service.get_submitted_works(offset=0, limit=10, student_id=student.id,
                                                          from_date=timezone.now()-timedelta(days=5),
                                                          to_date=timezone.now())
        self.assertEqual(len(returned_works), 2)


# Компонентные тесты
class DistanceEducationSystemTests(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

        self.student1 = Student.objects.create(name='John', last_name='Wick')
        self.student2 = Student.objects.create(name='Water', last_name='Rock')

    def test_student_creation_success(self):
        request = self.factory.post("/students", {'name': 'TestName', 'last_name': 'TestLastName'})
        response = StudentsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_creation_fail(self):
        request = self.factory.post("/students", {'name': 'TestName', 'last': ''})
        response = StudentsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # def test_get_student_success(self):
    #     request = self.factory.get(f'/students/{self.student1.id}')
    #     response = StudentsViewSet.as_view({'get': 'retrieve'})(request)
    #     self.assertEqual(response.data, self.student1)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_deletion_success(self):
        request = self.factory.delete(f'/students/{self.student2.id}')
        response = StudentsViewSet.as_view({'delete': 'destroy'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


