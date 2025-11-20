import reflex as rx
from typing import Optional
from app.models import CompetitionResult, Athlete, Competition
import sqlmodel
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
import datetime


class ResultItem(rx.Base):
    id: int
    athlete_id: int
    athlete_name: str
    category: str
    result: str


class CompetitionResultState(rx.State):
    results: list[ResultItem] = []
    available_athletes: list[Athlete] = []
    current_competition_id: Optional[int] = None
    form_athlete_id: str = ""
    form_category: str = "Kumite"
    form_result: str = "Registered"

    @rx.event
    async def load_data(self):
        if not self.current_competition_id:
            return
        with rx.session() as session:
            self.available_athletes = session.exec(
                sqlmodel.select(Athlete)
                .where(Athlete.is_active == True)
                .order_by(Athlete.full_name)
            ).all()
            query = sqlmodel.select(CompetitionResult, Athlete).where(
                (CompetitionResult.competition_id == self.current_competition_id)
                & (CompetitionResult.athlete_id == Athlete.id)
            )
            db_results = session.exec(query).all()
            self.results = [
                ResultItem(
                    id=r.id,
                    athlete_id=a.id,
                    athlete_name=a.full_name,
                    category=r.category,
                    result=r.result,
                )
                for r, a in db_results
            ]

    @rx.event
    def set_form_athlete_id(self, value: str):
        self.form_athlete_id = value

    @rx.event
    def set_form_category(self, value: str):
        self.form_category = value

    @rx.event
    def set_form_result(self, value: str):
        self.form_result = value

    @rx.event
    async def add_result(self):
        if not self.current_competition_id or not self.form_athlete_id:
            return
        try:
            with rx.session() as session:
                existing = session.exec(
                    sqlmodel.select(CompetitionResult).where(
                        (
                            CompetitionResult.competition_id
                            == self.current_competition_id
                        )
                        & (CompetitionResult.athlete_id == int(self.form_athlete_id))
                        & (CompetitionResult.category == self.form_category)
                    )
                ).first()
                if existing:
                    existing.result = self.form_result
                    session.add(existing)
                else:
                    new_result = CompetitionResult(
                        competition_id=self.current_competition_id,
                        athlete_id=int(self.form_athlete_id),
                        category=self.form_category,
                        result=self.form_result,
                    )
                    session.add(new_result)
                session.commit()
            self.form_athlete_id = ""
            return CompetitionResultState.load_data
        except Exception as e:
            logging.exception(f"Error adding result: {e}")

    @rx.event
    async def update_result_status(self, result_id: int, new_status: str):
        try:
            with rx.session() as session:
                res = session.get(CompetitionResult, result_id)
                if res:
                    res.result = new_status
                    session.add(res)
                    session.commit()
            return CompetitionResultState.load_data
        except Exception as e:
            logging.exception(f"Error updating result: {e}")

    @rx.event
    async def delete_result(self, result_id: int):
        try:
            with rx.session() as session:
                res = session.get(CompetitionResult, result_id)
                if res:
                    session.delete(res)
                    session.commit()
            return CompetitionResultState.load_data
        except Exception as e:
            logging.exception(f"Error deleting result: {e}")

    @rx.event
    async def generate_pdf(self):
        if not self.current_competition_id:
            return
        try:
            with rx.session() as session:
                comp = session.get(Competition, self.current_competition_id)
                if not comp:
                    return
                upload_dir = rx.get_upload_dir()
                upload_dir.mkdir(parents=True, exist_ok=True)
                filename = f"competition_{comp.id}_results.pdf"
                file_path = upload_dir / filename
                c = canvas.Canvas(file_path, pagesize=A4)
                width, height = A4
                c.setFillColor(colors.HexColor("#DC2626"))
                c.rect(0, height - 3 * cm, width, 3 * cm, fill=1, stroke=0)
                c.setFillColor(colors.white)
                c.setFont("Helvetica-Bold", 24)
                c.drawString(2 * cm, height - 1.8 * cm, "GALIA CLUB KARATE")
                c.setFont("Helvetica", 14)
                c.drawString(2 * cm, height - 2.5 * cm, f"Results: {comp.name}")
                c.setFillColor(colors.black)
                c.setFont("Helvetica", 10)
                c.drawString(
                    2 * cm, height - 4 * cm, f"Date: {comp.date.strftime('%Y-%m-%d')}"
                )
                c.drawString(2 * cm, height - 4.5 * cm, f"Location: {comp.location}")
                y = height - 6 * cm
                c.setFont("Helvetica-Bold", 10)
                c.drawString(2 * cm, y, "Athlete")
                c.drawString(8 * cm, y, "Category")
                c.drawString(14 * cm, y, "Result")
                c.line(2 * cm, y - 0.2 * cm, width - 2 * cm, y - 0.2 * cm)
                y -= 1 * cm
                c.setFont("Helvetica", 10)
                for item in self.results:
                    if y < 2 * cm:
                        c.showPage()
                        y = height - 2 * cm
                    c.drawString(2 * cm, y, item.athlete_name)
                    c.drawString(8 * cm, y, item.category)
                    if item.result == "Gold":
                        c.setFillColor(colors.gold)
                    elif item.result == "Silver":
                        c.setFillColor(colors.gray)
                    elif item.result == "Bronze":
                        c.setFillColor(colors.brown)
                    else:
                        c.setFillColor(colors.black)
                    c.drawString(14 * cm, y, item.result)
                    c.setFillColor(colors.black)
                    y -= 0.8 * cm
                c.save()
                return rx.download(url=f"/_upload/{filename}")
        except Exception as e:
            logging.exception(f"PDF Generation Error: {e}")