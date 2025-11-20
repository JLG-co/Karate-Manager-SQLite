import reflex as rx
from typing import Optional
import logging
import os
import shutil
import datetime
import io
import zipfile
import base64
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.utils import ImageReader
from sqlmodel import select
from app.models import Setting, Athlete, BeltRank, Payment
import sqlmodel


class SettingsState(rx.State):
    monthly_fee: str = "500"
    yearly_license: str = "300"
    last_backup_date: str = "Never"
    backup_status: str = ""
    restore_status: str = ""
    id_card_status: str = ""

    @rx.event
    async def load_settings(self):
        with rx.session() as session:
            m_fee = session.exec(
                select(Setting).where(Setting.key == "monthly_fee")
            ).first()
            y_lic = session.exec(
                select(Setting).where(Setting.key == "yearly_license")
            ).first()
            if m_fee:
                self.monthly_fee = m_fee.value
            if y_lic:
                self.yearly_license = y_lic.value

    @rx.event
    async def save_settings(self):
        with rx.session() as session:
            m_fee = session.exec(
                select(Setting).where(Setting.key == "monthly_fee")
            ).first()
            if m_fee:
                m_fee.value = self.monthly_fee
                session.add(m_fee)
            else:
                session.add(
                    Setting(
                        key="monthly_fee",
                        value=self.monthly_fee,
                        description="Monthly subscription fee",
                    )
                )
            y_lic = session.exec(
                select(Setting).where(Setting.key == "yearly_license")
            ).first()
            if y_lic:
                y_lic.value = self.yearly_license
                session.add(y_lic)
            else:
                session.add(
                    Setting(
                        key="yearly_license",
                        value=self.yearly_license,
                        description="Annual license fee",
                    )
                )
            session.commit()
        rx.toast("Settings saved successfully.")

    @rx.event
    def set_monthly_fee(self, value: str):
        self.monthly_fee = value

    @rx.event
    def set_yearly_license(self, value: str):
        self.yearly_license = value

    @rx.event
    async def backup_database(self):
        try:
            db_path = "reflex.db"
            if not os.path.exists(db_path):
                self.backup_status = "Database file not found."
                return
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backup_{timestamp}.zip"
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(db_path, arcname="reflex.db")
            memory_file.seek(0)
            data = memory_file.getvalue()
            self.last_backup_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.backup_status = "Backup created successfully."
            return rx.download(data=data, filename=filename)
        except Exception as e:
            logging.exception(f"Backup error: {e}")
            self.backup_status = f"Backup failed: {str(e)}"

    @rx.event
    async def handle_restore_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        try:
            file = files[0]
            content = await file.read()
            try:
                with zipfile.ZipFile(io.BytesIO(content)) as zf:
                    if "reflex.db" not in zf.namelist():
                        self.restore_status = (
                            "Invalid backup: reflex.db not found in archive."
                        )
                        return
                    with open("reflex.db", "wb") as f:
                        f.write(zf.read("reflex.db"))
            except zipfile.BadZipFile as e:
                logging.exception(f"Restore error (BadZipFile): {e}")
                self.restore_status = (
                    "Invalid file format. Please upload a valid ZIP backup."
                )
                return
            self.restore_status = "Database restored successfully. Please restart the application to apply changes."
            rx.toast("Restore complete. Restart required.")
        except Exception as e:
            logging.exception(f"Restore error: {e}")
            self.restore_status = f"Restore failed: {str(e)}"

    def _draw_id_card(self, c, athlete: Athlete, belt_name: str, x: float, y: float):
        width = 85.6 * mm
        height = 53.98 * mm
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.setFillColor(colors.white)
        c.roundRect(x, y, width, height, 3 * mm, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#DC2626"))
        c.rect(x, y + height - 12 * mm, width, 12 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x + width / 2, y + height - 8 * mm, "GALIA CLUB KARATE")
        c.setFillColor(colors.lightgrey)
        c.rect(x + 4 * mm, y + 15 * mm, 25 * mm, 30 * mm, fill=1, stroke=1)
        c.setFillColor(colors.gray)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + 16.5 * mm, y + 30 * mm, "PHOTO")
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 33 * mm, y + 40 * mm, athlete.full_name)
        c.setFont("Helvetica", 10)
        c.drawString(x + 33 * mm, y + 34 * mm, f"Rank: {belt_name}")
        c.drawString(x + 33 * mm, y + 29 * mm, f"ID: {athlete.id:05d}")
        valid_date = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime(
            "%Y-%m-%d"
        )
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.gray)
        c.drawString(x + 33 * mm, y + 24 * mm, f"Valid until: {valid_date}")
        qr_data = f"GALIA:{athlete.id}:{athlete.full_name}"
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        qr_img.save(img_buffer)
        img_buffer.seek(0)
        c.drawImage(
            ImageReader(img_buffer),
            x + width - 22 * mm,
            y + 4 * mm,
            width=18 * mm,
            height=18 * mm,
        )
        c.setFillColor(colors.HexColor("#1F2937"))
        c.rect(x, y, width, 3 * mm, fill=1, stroke=0)

    @rx.event
    async def generate_id_card(self, athlete_id: int):
        try:
            with rx.session() as session:
                athlete = session.get(Athlete, athlete_id)
                if not athlete:
                    return
                belt = (
                    session.get(BeltRank, athlete.current_belt_rank_id)
                    if athlete.current_belt_rank_id
                    else None
                )
                belt_name = belt.name if belt else "Unranked"
                upload_dir = rx.get_upload_dir()
                upload_dir.mkdir(parents=True, exist_ok=True)
                filename = f"ID_Card_{athlete.id}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
                file_path = upload_dir / filename
                c = canvas.Canvas(file_path, pagesize=A4)
                page_w, page_h = A4
                card_w = 85.6 * mm
                card_h = 53.98 * mm
                x = (page_w - card_w) / 2
                y = (page_h - card_h) / 2
                self._draw_id_card(c, athlete, belt_name, x, y)
                c.save()
                return rx.download(url=f"/_upload/{filename}")
        except Exception as e:
            logging.exception(f"ID Card Generation Error: {e}")
            self.id_card_status = f"Error: {e}"

    @rx.event
    async def generate_all_id_cards(self):
        try:
            with rx.session() as session:
                athletes = session.exec(
                    select(Athlete)
                    .where(Athlete.is_active == True)
                    .order_by(Athlete.full_name)
                ).all()
                belt_ranks = {
                    b.id: b.name for b in session.exec(select(BeltRank)).all()
                }
                upload_dir = rx.get_upload_dir()
                upload_dir.mkdir(parents=True, exist_ok=True)
                filename = (
                    f"All_ID_Cards_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
                )
                file_path = upload_dir / filename
                c = canvas.Canvas(file_path, pagesize=A4)
                page_w, page_h = A4
                card_w = 85.6 * mm
                card_h = 53.98 * mm
                margin_x = 15 * mm
                margin_y = 15 * mm
                spacing_x = 5 * mm
                spacing_y = 5 * mm
                col = 0
                row = 0
                cols_per_page = 2
                rows_per_page = 4
                current_x = margin_x
                current_y = page_h - margin_y - card_h
                for athlete in athletes:
                    belt_name = belt_ranks.get(athlete.current_belt_rank_id, "Unranked")
                    self._draw_id_card(c, athlete, belt_name, current_x, current_y)
                    col += 1
                    if col >= cols_per_page:
                        col = 0
                        row += 1
                        current_x = margin_x
                        current_y -= card_h + spacing_y
                    else:
                        current_x += card_w + spacing_x
                    if row >= rows_per_page:
                        c.showPage()
                        col = 0
                        row = 0
                        current_x = margin_x
                        current_y = page_h - margin_y - card_h
                c.save()
                self.id_card_status = "Batch generation complete."
                return rx.download(url=f"/_upload/{filename}")
        except Exception as e:
            logging.exception(f"Batch ID Generation Error: {e}")
            self.id_card_status = f"Error: {e}"