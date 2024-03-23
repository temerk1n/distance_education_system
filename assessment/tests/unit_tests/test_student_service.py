import uuid

from django.test import TestCase

from assessment.models import Student
from assessment.services.students_service import StudentsService


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