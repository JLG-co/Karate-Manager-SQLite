import reflex as rx
from typing import Optional
from app.models import Athlete, Attendance
import sqlmodel
import datetime
import logging


class AttendanceItem(rx.Base):
    athlete_id: int
    full_name: str
    belt_name: str
    status: str = "None"
    time: str = ""
    record_id: Optional[int] = None


class AttendanceState(rx.State):
    today_attendance: list[AttendanceItem] = []
    search_query: str = ""
    checkin_date: str = datetime.date.today().isoformat()
    present_count: int = 0
    absent_count: int = 0
    late_count: int = 0
    total_count: int = 0

    @rx.event
    async def load_today_status(self):
        query_date = datetime.datetime.fromisoformat(self.checkin_date)
        with rx.session() as session:
            athletes = session.exec(
                sqlmodel.select(Athlete)
                .where(Athlete.is_active == True)
                .order_by(Athlete.full_name)
            ).all()
            attendance_records = session.exec(
                sqlmodel.select(Attendance).where(
                    (Attendance.date >= query_date)
                    & (Attendance.date < query_date + datetime.timedelta(days=1))
                )
            ).all()
            attendance_map = {r.athlete_id: r for r in attendance_records}
            from app.models import BeltRank

            belts = {
                b.id: b.name for b in session.exec(sqlmodel.select(BeltRank)).all()
            }
            items = []
            present = 0
            absent = 0
            late = 0
            for athlete in athletes:
                record = attendance_map.get(athlete.id)
                status = record.status if record else "None"
                if status == "Present":
                    present += 1
                elif status == "Absent":
                    absent += 1
                elif status == "Late":
                    late += 1
                belt_name = (
                    belts.get(athlete.current_belt_rank_id, "Unranked")
                    if athlete.current_belt_rank_id
                    else "Unranked"
                )
                items.append(
                    AttendanceItem(
                        athlete_id=athlete.id,
                        full_name=athlete.full_name,
                        belt_name=belt_name,
                        status=status,
                        time=record.class_time if record and record.class_time else "",
                        record_id=record.id if record else None,
                    )
                )
            self.total_count = len(athletes)
            self.present_count = present
            self.absent_count = absent
            self.late_count = late
            self.today_attendance = items

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_checkin_date(self, date: str):
        self.checkin_date = date
        return AttendanceState.load_today_status

    @rx.event
    async def mark_status(self, athlete_id: int, status: str):
        query_date = datetime.datetime.fromisoformat(self.checkin_date)
        now_time = datetime.datetime.now().strftime("%H:%M")
        try:
            with rx.session() as session:
                existing = session.exec(
                    sqlmodel.select(Attendance).where(
                        (Attendance.athlete_id == athlete_id)
                        & (Attendance.date >= query_date)
                        & (Attendance.date < query_date + datetime.timedelta(days=1))
                    )
                ).first()
                if existing:
                    existing.status = status
                    if status != "None":
                        existing.class_time = now_time
                    session.add(existing)
                elif status != "None":
                    new_record = Attendance(
                        athlete_id=athlete_id,
                        date=query_date,
                        status=status,
                        class_time=now_time,
                    )
                    session.add(new_record)
                session.commit()
            return AttendanceState.load_today_status
        except Exception as e:
            logging.exception(f"Error marking attendance: {e}")

    @rx.var
    def filtered_attendance(self) -> list[AttendanceItem]:
        if not self.search_query:
            return self.today_attendance
        return [
            item
            for item in self.today_attendance
            if self.search_query.lower() in item.full_name.lower()
        ]

    @rx.var
    def attendance_rate(self) -> int:
        if self.total_count == 0:
            return 0
        return int((self.present_count + self.late_count) / self.total_count * 100)