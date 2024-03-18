from rest_framework import serializers

from assessment.models import Student, PracticalWork


class GetOperationQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)


class GetWorksQuerySerializer(serializers.Serializer):
    offset = serializers.IntegerField(min_value=0, default=0)
    limit = serializers.IntegerField(min_value=1, default=10)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    student_id = serializers.UUIDField(required=False)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticalWork
        fields = '__all__'


class WorkRequestSerializer(serializers.Serializer):
    student_id = serializers.UUIDField()
    title = serializers.CharField()
    file = serializers.FileField()


class MarkWorkQuerySerializer(serializers.Serializer):
    mark = serializers.IntegerField()


class OperationSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    done = serializers.BooleanField()
    result = serializers.ListField(child=WorkSerializer())
