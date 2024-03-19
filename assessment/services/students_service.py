from uuid import UUID

from django.shortcuts import get_object_or_404

from assessment.models import Student


class StudentsService:
    def add_student(self, student: Student) -> Student:
        student.save()
        return Student.objects.get(id=student.id)

    def get_student(self, id: UUID) -> Student | Student.DoesNotExist:
        return Student.objects.get(id=id)

    def get_all_students(self) -> list[Student]:
        return Student.objects.all()

    def delete_student(self, id: UUID) -> None:
        Student.objects.filter(id=id).delete()
