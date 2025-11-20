import reflex as rx
from typing import Optional
from app.models import Payment, Athlete, Setting
import sqlmodel
from sqlmodel import select
import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
import logging


class PaymentData(rx.Base):
    id: int
    athlete_id: int
    athlete_name: str
    amount: float
    payment_type: str
    status: str
    payment_date: str
    month_year: str
    notes: str


class PaymentState(rx.State):
    payments: list[PaymentData] = []
    athletes: list[Athlete] = []
    filtered_payments: list[PaymentData] = []
    search_query: str = ""
    status_filter: str = "all"
    type_filter: str = "all"
    total_income: float = 0.0
    monthly_revenue: float = 0.0
    unpaid_count: int = 0
    is_open: bool = False
    current_payment_id: Optional[int] = None
    form_athlete_id: str = ""
    form_amount: float = 500.0
    form_type: str = "Monthly Fee"
    form_status: str = "Paid"
    form_date: str = datetime.date.today().isoformat()
    form_month: int = datetime.date.today().month
    form_year: int = datetime.date.today().year
    form_notes: str = ""

    @rx.event
    async def load_data(self):
        with rx.session() as session:
            self.athletes = session.exec(
                select(Athlete)
                .where(Athlete.is_active == True)
                .order_by(Athlete.full_name)
            ).all()
            query = select(Payment, Athlete).where(Payment.athlete_id == Athlete.id)
            results = session.exec(query).all()
            self.payments = []
            now = datetime.datetime.now()
            current_month_revenue = 0.0
            total_inc = 0.0
            unpaid = 0
            for payment, athlete in results:
                month_year = "-"
                if payment.month_covered and payment.year_covered:
                    month_year = f"{datetime.date(2000, payment.month_covered, 1).strftime('%B')} {payment.year_covered}"
                p_data = PaymentData(
                    id=payment.id,
                    athlete_id=athlete.id,
                    athlete_name=athlete.full_name,
                    amount=payment.amount,
                    payment_type=payment.payment_type,
                    status=payment.status,
                    payment_date=payment.payment_date.strftime("%Y-%m-%d"),
                    month_year=month_year,
                    notes=payment.notes or "",
                )
                self.payments.append(p_data)
                total_inc += (
                    payment.amount if payment.status in ["Paid", "Partial"] else 0
                )
                if (
                    payment.month_covered == now.month
                    and payment.year_covered == now.year
                ):
                    current_month_revenue += (
                        payment.amount if payment.status in ["Paid", "Partial"] else 0
                    )
                if payment.status in ["Unpaid", "Overdue"]:
                    unpaid += 1
            self.total_income = total_inc
            self.monthly_revenue = current_month_revenue
            self.unpaid_count = unpaid
            self.payments.sort(key=lambda x: x.payment_date, reverse=True)
            self.filter_payments()

    @rx.event
    def filter_payments(self):
        filtered = self.payments
        if self.search_query:
            filtered = [
                p
                for p in filtered
                if self.search_query.lower() in p.athlete_name.lower()
            ]
        if self.status_filter != "all":
            filtered = [p for p in filtered if p.status == self.status_filter]
        if self.type_filter != "all":
            filtered = [p for p in filtered if p.payment_type == self.type_filter]
        self.filtered_payments = filtered

    @rx.event
    def set_search(self, query: str):
        self.search_query = query
        self.filter_payments()

    @rx.event
    def set_status_filter(self, value: str):
        self.status_filter = value
        self.filter_payments()

    @rx.event
    def set_type_filter(self, value: str):
        self.type_filter = value
        self.filter_payments()

    @rx.event
    def set_form_amount(self, value: str):
        if not value:
            self.form_amount = 0.0
            return
        try:
            self.form_amount = float(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def set_form_month(self, value: str):
        if not value:
            return
        try:
            self.form_month = int(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def set_form_year(self, value: str):
        if not value:
            return
        try:
            self.form_year = int(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def open_add_modal(self):
        self.current_payment_id = None
        self.form_athlete_id = ""
        self.form_amount = 500.0
        self.form_type = "Monthly Fee"
        self.form_status = "Paid"
        self.form_date = datetime.date.today().isoformat()
        self.form_month = datetime.date.today().month
        self.form_year = datetime.date.today().year
        self.form_notes = ""
        self.is_open = True

    @rx.event
    def open_edit_modal(self, payment: PaymentData):
        self.current_payment_id = payment.id
        self.form_athlete_id = str(payment.athlete_id)
        self.form_amount = payment.amount
        self.form_type = payment.payment_type
        self.form_status = payment.status
        self.form_date = payment.payment_date
        with rx.session() as session:
            p_obj = session.get(Payment, payment.id)
            if p_obj:
                self.form_month = p_obj.month_covered or datetime.date.today().month
                self.form_year = p_obj.year_covered or datetime.date.today().year
        self.form_notes = payment.notes
        self.is_open = True

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    async def save_payment(self):
        if not self.form_athlete_id:
            return
        with rx.session() as session:
            data = {
                "athlete_id": int(self.form_athlete_id),
                "amount": self.form_amount,
                "payment_type": self.form_type,
                "payment_date": datetime.datetime.fromisoformat(self.form_date),
                "month_covered": self.form_month,
                "year_covered": self.form_year,
                "status": self.form_status,
                "notes": self.form_notes,
            }
            if self.current_payment_id:
                payment = session.get(Payment, self.current_payment_id)
                for key, value in data.items():
                    setattr(payment, key, value)
                session.add(payment)
            else:
                payment = Payment(**data)
                session.add(payment)
            session.commit()
        self.is_open = False
        return PaymentState.load_data

    @rx.event
    async def delete_payment(self, id: int):
        with rx.session() as session:
            payment = session.get(Payment, id)
            if payment:
                session.delete(payment)
                session.commit()
        return PaymentState.load_data

    @rx.event
    async def download_receipt(self, payment_id: int):
        try:
            with rx.session() as session:
                payment = session.get(Payment, payment_id)
                athlete = session.get(Athlete, payment.athlete_id)
                if not payment or not athlete:
                    return
                upload_dir = rx.get_upload_dir()
                upload_dir.mkdir(parents=True, exist_ok=True)
                filename = f"receipt_{payment.id}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
                file_path = upload_dir / filename
                c = canvas.Canvas(file_path, pagesize=A4)
                width, height = A4
                red_color = colors.HexColor("#DC2626")
                dark_gray = colors.HexColor("#1F2937")
                c.setFillColor(red_color)
                c.rect(0, height - 3 * cm, width, 3 * cm, fill=1, stroke=0)
                c.setFillColor(colors.white)
                c.setFont("Helvetica-Bold", 24)
                c.drawString(2 * cm, height - 1.8 * cm, "GALIA CLUB KARATE")
                c.setFont("Helvetica", 12)
                c.drawString(2 * cm, height - 2.5 * cm, "Official Payment Receipt")
                c.setFillColor(dark_gray)
                c.setFont("Helvetica", 10)
                c.drawString(
                    width - 7 * cm, height - 4.5 * cm, f"Receipt #: {payment.id:06d}"
                )
                c.drawString(
                    width - 7 * cm,
                    height - 5 * cm,
                    f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}",
                )
                c.setFont("Helvetica-Bold", 14)
                c.drawString(2 * cm, height - 5 * cm, "Received From:")
                c.setFont("Helvetica", 12)
                c.drawString(2 * cm, height - 5.7 * cm, athlete.full_name)
                if athlete.age_category_id:
                    pass
                table_y = height - 8 * cm
                c.setStrokeColor(colors.lightgrey)
                c.line(2 * cm, table_y, width - 2 * cm, table_y)
                c.setFont("Helvetica-Bold", 10)
                c.drawString(2.5 * cm, table_y - 0.8 * cm, "Description")
                c.drawString(width - 5 * cm, table_y - 0.8 * cm, "Amount")
                c.line(2 * cm, table_y - 1.2 * cm, width - 2 * cm, table_y - 1.2 * cm)
                c.setFont("Helvetica", 10)
                desc = f"{payment.payment_type}"
                if payment.month_covered:
                    month_name = datetime.date(2000, payment.month_covered, 1).strftime(
                        "%B"
                    )
                    desc += f" - {month_name} {payment.year_covered}"
                c.drawString(2.5 * cm, table_y - 2 * cm, desc)
                c.drawString(
                    width - 5 * cm, table_y - 2 * cm, f"{payment.amount:,.2f} DA"
                )
                c.line(2 * cm, table_y - 3 * cm, width - 2 * cm, table_y - 3 * cm)
                c.setFont("Helvetica-Bold", 12)
                c.drawString(width - 8 * cm, table_y - 4 * cm, "Total Paid:")
                c.setFillColor(red_color)
                c.drawString(
                    width - 5 * cm, table_y - 4 * cm, f"{payment.amount:,.2f} DA"
                )
                c.setFillColor(colors.gray)
                c.setFont("Helvetica-Oblique", 8)
                c.drawCentredString(
                    width / 2,
                    2 * cm,
                    "Thank you for your payment. Keep this receipt for your records.",
                )
                c.drawCentredString(
                    width / 2, 1.5 * cm, "Galia Club Manager - Generated System Receipt"
                )
                c.save()
                return rx.download(url=f"/_upload/{filename}")
        except Exception as e:
            logging.exception(f"PDF Generation Error: {e}")