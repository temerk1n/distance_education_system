from datetime import datetime
from typing import Set, List
from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils import timezone

from ..models import Student, PracticalWork


class WorkCheckService:
    def add_work(self, work: PracticalWork) -> PracticalWork:
        work.save()
        return PracticalWork.objects.get(id=work.id)

    def get_work_by_id(self, id: UUID) -> PracticalWork:
        return PracticalWork.objects.get(id=id)

    def mark_work(self, id: UUID, mark: int) -> None:
        work: PracticalWork = get_object_or_404(PracticalWork, id=id)

        if 0 <= mark <= 100:
            work.mark = mark
            work.mark_date = timezone.now()
            self.send_notification(work)
            work.save()
        else:
            raise ValueError("Оценка должна быть от 0 до 100")

    def send_notification(self, work: PracticalWork) -> None:
        student = Student.objects.get(pk=work.student_id)
        print(f"\nСтуденту {student.last_name} была выставлена оценка {work.mark} в {work.mark_date}")

    def get_submitted_works(
            self, offset: int, limit: int,
            from_date: datetime = None, to_date: datetime = None,
            student_id: UUID = None
    ) -> list[PracticalWork]:
        works = []
        if student_id:
            works = PracticalWork.objects.filter(student_id=student_id)
        elif from_date and to_date:
            print((from_date, to_date))
            if student_id:
                works = PracticalWork.objects.filter(student_id=student_id, submitting_date__range=[from_date, to_date])
            else:
                works = PracticalWork.objects.filter(submitting_date__range=[from_date, to_date])
        else:
            works = PracticalWork.objects.all()

        return list(works)[offset:offset + limit]
