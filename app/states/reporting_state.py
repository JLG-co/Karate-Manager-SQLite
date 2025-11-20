import reflex as rx
from typing import Optional
from app.models import (
    Athlete,
    Payment,
    Attendance,
    BeltPromotion,
    Competition,
    CompetitionResult,
)
import sqlmodel
import datetime
import csv
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
import logging


class ReportingState(rx.State):
    total_athletes: int = 0
    total_income: float = 0.0
    attendance_rate: float = 0.0
    promotions_count: int = 0
    report_type: str = "Athletes"
    start_date: str = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    end_date: str = datetime.date.today().isoformat()

    @rx.event
    async def load_stats(self):
        try:
            with rx.session() as session:
                self.total_athletes = len(
                    session.exec(
                        sqlmodel.select(Athlete).where(Athlete.is_active == True)
                    ).all()
                )
                payments = session.exec(sqlmodel.select(Payment)).all()
                self.total_income = sum(
                    (p.amount for p in payments if p.status in ["Paid", "Partial"])
                )
                thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
                attendance_records = session.exec(
                    sqlmodel.select(Attendance).where(
                        Attendance.date >= thirty_days_ago
                    )
                ).all()
                present = sum(
                    (1 for a in attendance_records if a.status in ["Present", "Late"])
                )
                total_records = len(attendance_records)
                self.attendance_rate = (
                    round(present / total_records * 100, 1)
                    if total_records > 0
                    else 0.0
                )
                promotions = session.exec(
                    sqlmodel.select(BeltPromotion).where(
                        BeltPromotion.promotion_date >= thirty_days_ago
                    )
                ).all()
                self.promotions_count = len(promotions)
        except Exception as e:
            logging.exception(f"Error loading stats: {e}")

    @rx.event
    def set_report_type(self, value: str):
        self.report_type = value

    @rx.event
    def set_start_date(self, value: str):
        self.start_date = value

    @rx.event
    def set_end_date(self, value: str):
        self.end_date = value

    @rx.event
    async def generate_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)
        try:
            with rx.session() as session:
                start = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
                end = datetime.datetime.strptime(
                    self.end_date, "%Y-%m-%d"
                ) + datetime.timedelta(days=1)
                if self.report_type == "Athletes":
                    writer.writerow(["ID", "Full Name", "Gender", "Phone", "Belt Rank"])
                    athletes = session.exec(
                        sqlmodel.select(Athlete).where(Athlete.is_active == True)
                    ).all()
                    for a in athletes:
                        writer.writerow(
                            [
                                a.id,
                                a.full_name,
                                a.gender,
                                a.phone,
                                a.current_belt_rank_id,
                            ]
                        )
                elif self.report_type == "Payments":
                    writer.writerow(
                        ["ID", "Athlete ID", "Amount", "Type", "Date", "Status"]
                    )
                    payments = session.exec(
                        sqlmodel.select(Payment).where(
                            (Payment.payment_date >= start)
                            & (Payment.payment_date < end)
                        )
                    ).all()
                    for p in payments:
                        writer.writerow(
                            [
                                p.id,
                                p.athlete_id,
                                p.amount,
                                p.payment_type,
                                p.payment_date,
                                p.status,
                            ]
                        )
                elif self.report_type == "Attendance":
                    writer.writerow(["Date", "Athlete ID", "Status", "Time"])
                    attendance = session.exec(
                        sqlmodel.select(Attendance).where(
                            (Attendance.date >= start) & (Attendance.date < end)
                        )
                    ).all()
                    for a in attendance:
                        writer.writerow([a.date, a.athlete_id, a.status, a.class_time])
                elif self.report_type == "Competitions":
                    writer.writerow(["Competition", "Athlete ID", "Result", "Category"])
                    results = session.exec(sqlmodel.select(CompetitionResult)).all()
                    for r in results:
                        writer.writerow(
                            [r.competition_id, r.athlete_id, r.result, r.category]
                        )
            filename = f"report_{self.report_type.lower()}_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
            return rx.download(data=output.getvalue(), filename=filename)
        except Exception as e:
            logging.exception(f"CSV Generation Error: {e}")