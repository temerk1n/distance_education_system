import uuid

from django.db import models


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    submitted_works_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ' ' + self.last_name


class PracticalWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitting_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    file = models.FileField(null=True, upload_to="Uploaded Files/")
    mark_date = models.DateTimeField(auto_now_add=False, null=True)
    mark = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return self.title + ' ' + self.submitting_date.__str__()


class Operation:
    id: uuid.UUID
    done: bool

    def __init__(self, id: uuid.UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result

    def __eq__(self, other: "Operation") -> bool:
        return (
            self.id == other.id
            and self.done == other.done
            and self.result == other.result
        )

    def __repr__(self) -> str:
        return str(
            {
                "id": self.id,
                "done": self.done,
                "result": self.result,
            }
        )
