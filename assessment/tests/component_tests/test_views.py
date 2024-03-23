import uuid

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from assessment.models import Student, PracticalWork
from assessment.serializers import StudentSerializer, WorkSerializer
from assessment.views import StudentsViewSet, WorksViewSet


class DistanceEducationSystemTests(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()

        self.student1 = Student(name='John', last_name='Wick')
        self.student1.save()
        self.student2 = Student(name='Water', last_name='Rock')
        self.student2.save()

        self.work = PracticalWork(student_id=self.student1.id, title="Test title", file='Uploaded Files/test_work.txt')
        self.work.save()

    def test_student_creation_success(self):
        request = self.factory.post("/students", {'name': 'TestName', 'last_name': 'TestLastName'})
        response = StudentsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_creation_fail(self):
        request = self.factory.post("/students", {'name': 'TestName', 'last': ''})
        response = StudentsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_student_success(self):
        request = self.factory.get(f'/students/{self.student1}')
        response = StudentsViewSet.as_view({'get': 'retrieve'})(request, self.student1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, StudentSerializer(self.student1).data)

    def test_get_student_fail(self):
        id = uuid.uuid4()
        request = self.factory.get(f'students/{id}')
        with self.assertRaises(Student.DoesNotExist):
            response = StudentsViewSet.as_view({'get': 'retrieve'})(request, id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_students_list(self):
        students = [self.student1, self.student2]
        serialized = StudentSerializer(students, many=True).data
        request = self.factory.get(f'/students')
        response = StudentsViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, serialized)

    def test_student_deletion_success(self):
        request = self.factory.delete(f'/students/{self.student2.id}')
        response = StudentsViewSet.as_view({'delete': 'destroy'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_work_creation_success(self):
        with open('media/Uploaded Files/test_work.txt') as file:
            data = {'student_id': f'{self.student1.id}', 'title': "TO_DELETE", 'file': file}
            request = self.factory.post("/works", data, format='multipart')
            response = WorksViewSet.as_view({'post': 'create'})(request)
            PracticalWork.objects.get(title='TO_DELETE').delete()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_work_creation_fail(self):
        data = {'student_id': f'student_id', 'titl': "Test title", 'file': 's'}
        request = self.factory.post("/works", data)
        response = WorksViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_work_success(self):
        request = self.factory.get(f'/works/{self.work.id}')
        response = WorksViewSet.as_view({'get': 'retrieve'})(request, self.work.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, WorkSerializer(self.work).data)

    def test_get_work_fail(self):
        id = uuid.uuid4()
        request = self.factory.get(f'/works/{id}')
        with self.assertRaises(PracticalWork.DoesNotExist):
            response = WorksViewSet.as_view({'get': 'retrieve'})(request, id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_work_success(self):
        data = {"mark": 50}
        request = self.factory.patch(f'/works/{self.work.id}', data, format="json")
        response = WorksViewSet.as_view({'patch': 'partial_update'})(request, self.work.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_work_fail(self):
        request = self.factory.patch(f'/works/{self.work.id}', {"mark": 1243412})
        response = WorksViewSet.as_view({'patch': 'partial_update'})(request, self.work.id)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_request_works(self):
        request = self.factory.get('/works/request', {'offset': 0, 'limit': 10})
        response = WorksViewSet.as_view({'get': 'request_works'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
