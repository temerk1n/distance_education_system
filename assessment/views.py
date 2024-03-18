from uuid import UUID

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from assessment.models import PracticalWork, Student
from assessment.serializers import WorkSerializer, StudentSerializer, MarkWorkQuerySerializer
from assessment.services.students_service import StudentsService
from assessment.services.work_check_service import WorkCheckService


class WorksViewSet(ModelViewSet):
    work_service = WorkCheckService()
    lookup_field = 'id'

    serializer_class = WorkSerializer
    queryset = PracticalWork.objects.all()

    def partial_update(self, request, id: UUID = None):
        body = MarkWorkQuerySerializer(data=request.data)
        if not body.is_valid():
            raise ValidationError(body.errors)

        self.work_service.check_work(id, **body.validated_data)
        return Response(request.data)



class StudentsViewSet(ViewSet):
    students_service = StudentsService()

    def create(self, request):
        body = StudentSerializer(data=request.data)
        if not body.is_valid():
            raise ValidationError(body.errors)
        created_student: Student = self.students_service.add_student(Student(**body.validated_data))
        return Response(data=StudentSerializer(created_student).data, status=status.HTTP_201_CREATED)

    def retrieve(self, _, id: UUID = None):
        try:
            student: Student = self.students_service.get_student(id)
            return Response(data=StudentSerializer(student).data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, _):
        students = self.students_service.get_all_students()
        return Response(data=StudentSerializer(students, many=True).data, status=status.HTTP_200_OK)

    def destroy(self, _, id: UUID = None):
        self.students_service.delete_student(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
