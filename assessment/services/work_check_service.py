from datetime import datetime
from uuid import UUID

from django.shortcuts import get_object_or_404

from ..models import Student, PracticalWork


class WorkCheckService:

    def submit_work(self, work: PracticalWork) -> None:
        work.save()

    def add_student(self, student: Student) -> None:
        student.save()

    def get_work_by_id(self, work_id: UUID) -> PracticalWork:
        work: PracticalWork = PracticalWork.objects.get(pk=work_id)
        return work

    def get_students(self, student_id: UUID) -> Student:
        student: Student = Student.objects.get(pk=student_id)
        return student

    def check_work(self, work_id: UUID, mark: int) -> None:
        work: PracticalWork = get_object_or_404(PracticalWork, id=work_id)
        if 0 <= mark <= 100:
            work.mark = mark
            work.mark_date = datetime.now()
            self.send_notification(work_id)
            work.save()
        else:
            raise ValueError("Оценка должна быть от 0 до 100")

    def send_notification(self, work_id: UUID) -> None:
        work = PracticalWork.objects.get(pk=work_id)
        student = Student.objects.get(pk=work.student_id)
        print(f"\nСтуденту {student.last_name} была выставлена оценка {work.mark} в {work.mark_date}")

    def get_submitted_works(
            self, offset: int, limit: int,
            from_date: datetime = None, to_date: datetime = None,
            student_id: UUID = None
    ) -> list[PracticalWork]:
        works: list[PracticalWork] = []
        if student_id:
            if from_date and to_date:
                works = (PracticalWork.objects
                         .filter(student_id=student_id)
                         .filter(submitting_date__gte=from_date)
                         .filter(submitting_date__lte=to_date))[offset:offset + limit]
            else:
                works = PracticalWork.objects.filter(student_id=student_id)[offset:offset + limit]
        else:
            works = PracticalWork.objects.all()[offset:offset + limit]

        return works
