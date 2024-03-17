from uuid import UUID

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from assessment.models import PracticalWork, Student
from assessment.serializers import WorkSerializer, StudentSerializer, MarkWorkQuerySerializer
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


class StudentsViewSet(ModelViewSet):
    # work_service = WorkCheckService()

    lookup_field = 'id'

    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    # def destroy(self, request, *args, **kwargs):
    #     # print(request.)
    #     Student.objects.filter(pk=self.kwargs['id']).delete()
    #     return Response()

    # def create(self, request):
    #     body = StudentSerializer(data=request.data)
    #     if not body.is_valid():
    #         raise ValidationError(body.errors)
    #
    #     self.work_service.add_student(Student(**body.validated_data))
    #     return Response(body.data)
