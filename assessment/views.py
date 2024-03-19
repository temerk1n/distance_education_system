from uuid import UUID

from django.utils import timezone
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.viewsets import ViewSet

from assessment.models import PracticalWork, Student
from assessment.serializers import WorkSerializer, StudentSerializer, MarkWorkQuerySerializer, WorkRequestSerializer, \
    GetWorksQuerySerializer, OperationSerializer, GetOperationQuerySerializer, NewStudentSerializer
from assessment.services.operations_service import OperationsService
from assessment.services.students_service import StudentsService
from assessment.services.work_check_service import WorkCheckService


@extend_schema_view(
    create=extend_schema(
        summary="Post new work",
        request=WorkRequestSerializer,
        responses={
            status.HTTP_201_CREATED: None,
            status.HTTP_400_BAD_REQUEST: ReturnDict,
        },
        auth=False,
    ),
    retrieve=extend_schema(
        summary="Get work by id",
        responses={
            status.HTTP_200_OK: WorkSerializer,
            status.HTTP_204_NO_CONTENT: None,
        },
        auth=False,
    ),
    partial_update=extend_schema(
        summary="Mark work by id",
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: ReturnDict,
            status.HTTP_422_UNPROCESSABLE_ENTITY: None,
        },
        auth=False,
    ),
    request_works=extend_schema(
        summary="Request get works operation",
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_400_BAD_REQUEST: ReturnDict,
        },
        auth=False,
    ),
    list=extend_schema(
        summary="Get works list",
        responses={
            status.HTTP_200_OK: WorkSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: ReturnDict,
            status.HTTP_404_NOT_FOUND: None,
        },
        auth=False,
    ),
)
class WorksViewSet(ViewSet):
    work_service = WorkCheckService()
    operations_service = OperationsService()

    def create(self, request):
        body = WorkRequestSerializer(data=request.data)
        if not body.is_valid():
            raise ValidationError(body.errors)

        self.work_service.add_work(PracticalWork(**body.validated_data))
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, id: UUID = None):
        try:
            work: PracticalWork = self.work_service.get_work_by_id(id)
            return Response(data=WorkSerializer(work).data, status=status.HTTP_200_OK)
        except NotFound:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, id: UUID = None):
        body = MarkWorkQuerySerializer(data=request.data)
        if not body.is_valid():
            raise ValidationError(body.errors)

        try:
            self.work_service.mark_work(id, **body.validated_data)
            return Response(status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={'detail': str(e)})

    @action(detail=False, methods=['GET'])
    def request_works(self, request):
        query = GetWorksQuerySerializer(data=request.query_params)
        if not query.is_valid():
            raise ValidationError(query.errors)
        operation_id = self.operations_service.execute_operation(self.work_service.get_submitted_works, timezone.now(),
                                                                 query.validated_data)
        operation = self.operations_service.get_operation(operation_id)

        return Response(data=OperationSerializer(operation).data, status=status.HTTP_200_OK)

    def list(self, request):
        query = GetOperationQuerySerializer(data=request.query_params)
        if not query.is_valid():
            raise ValidationError(query.errors)

        operation = self.operations_service.get_operation(UUID(query.data.get("id")))
        if operation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(data=OperationSerializer(operation).data, status=status.HTTP_200_OK)


@extend_schema_view(
    create=extend_schema(
        summary="Post new student",
        request=NewStudentSerializer,
        responses={
            status.HTTP_201_CREATED: StudentSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ReturnDict,
        },
        auth=False,
    ),
    retrieve=extend_schema(
        summary="Get student by id",
        responses={
            status.HTTP_200_OK: StudentSerializer,
            status.HTTP_404_NOT_FOUND: None
        },
        auth=False,
    ),
    list=extend_schema(
        summary="Get students list",
        responses={
            status.HTTP_200_OK: StudentSerializer(many=True),
        },
        auth=False,
    ),
    destroy=extend_schema(
        summary="Delete student by id",
        responses={
            status.HTTP_200_OK: None,
        },
        auth=False,
    ),
)
class StudentsViewSet(ViewSet):
    students_service = StudentsService()

    def create(self, request):
        body = NewStudentSerializer(data=request.data)
        if not body.is_valid():
            return Response(data=body.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        created_student: Student = self.students_service.add_student(Student(**body.validated_data))
        return Response(data=StudentSerializer(created_student).data, status=status.HTTP_201_CREATED)

    def retrieve(self, _, id: UUID = None):
        student: Student = self.students_service.get_student(id)
        return Response(data=StudentSerializer(student).data, status=status.HTTP_200_OK)


    def list(self, _):
        students = self.students_service.get_all_students()
        return Response(data=StudentSerializer(students, many=True).data, status=status.HTTP_200_OK)

    def destroy(self, _, id: UUID = None):
        self.students_service.delete_student(id)
        return Response(status=status.HTTP_200_OK)
