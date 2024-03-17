from rest_framework import serializers

from .models import Student


# GET /works
class GetWorksQuerySerializer(serializers.Serializer):
    offset = serializers.IntegerField(min_value=0, default=0)
    limit = serializers.IntegerField(min_value=1, default=10)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    student_id = serializers.UUIDField(required=False)


# POST /students
class StudentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    submitted_works_count = serializers.IntegerField()


# POST /works
class SubmitWorkBodySerializer(serializers.Serializer):
    student_id = serializers.UUIDField()
    file = serializers.FileField()


# PATCH /works/{work_id}
class MarkWorkQuerySerializer(serializers.Serializer):
    mark = serializers.IntegerField()
