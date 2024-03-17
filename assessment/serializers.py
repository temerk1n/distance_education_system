from rest_framework import serializers

from assessment.models import Student, PracticalWork


# GET /works
class GetWorksQuerySerializer(serializers.Serializer):
    offset = serializers.IntegerField(min_value=0, default=0)
    limit = serializers.IntegerField(min_value=1, default=10)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    student_id = serializers.UUIDField(required=False)


# POST /students
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


# POST /works
class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticalWork
        fields = '__all__'


# PATCH /works/{work_id}
class MarkWorkQuerySerializer(serializers.Serializer):
    mark = serializers.IntegerField()
