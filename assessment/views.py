from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from assessment.models import PracticalWork, Student
from assessment.serializers import WorkSerializer, StudentSerializer
from assessment.services.work_check_service import WorkCheckService


class WorksViewSet(ViewSet):
    work_service = WorkCheckService()

    def create(self, request):
        body = WorkSerializer(data=request.data)

        if not body.is_valid():
            raise ValidationError(body.errors)

        work = PracticalWork(**body.validated_data)
        self.work_service.submit_work(work)
        return Response(body.data)


class StudentsViewSet(ViewSet):
    work_service = WorkCheckService()

    def create(self, request):
        body = StudentSerializer(data=request.data)
        if not body.is_valid():
            raise ValidationError(body.errors)

        self.work_service.add_student(Student(**body.validated_data))
        return Response(body.data)
