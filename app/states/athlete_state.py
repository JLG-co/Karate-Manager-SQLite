import reflex as rx
from typing import Optional
from app.models import Athlete, AgeCategory, BeltRank
import sqlmodel
import csv
import io
import logging


class AthleteState(rx.State):
    athletes: list[Athlete] = []
    available_age_categories: list[AgeCategory] = []
    available_belts: list[BeltRank] = []
    search_query: str = ""
    filter_age_category_id: str = "all"
    filter_belt_rank_id: str = "all"
    is_open: bool = False
    current_athlete_id: Optional[int] = None
    form_full_name: str = ""
    form_dob: str = ""
    form_gender: str = "Male"
    form_phone: str = ""
    form_guardian: str = ""
    form_age_category_id: str = ""
    form_belt_rank_id: str = ""
    is_upload_open: bool = False
    upload_error: str = ""
    upload_success: str = ""

    @rx.event
    async def load_athletes(self):
        query = sqlmodel.select(Athlete).where(Athlete.is_active == True)
        if self.search_query:
            query = query.where(Athlete.full_name.contains(self.search_query))
        if self.filter_age_category_id and self.filter_age_category_id != "all":
            query = query.where(
                Athlete.age_category_id == int(self.filter_age_category_id)
            )
        if self.filter_belt_rank_id and self.filter_belt_rank_id != "all":
            query = query.where(
                Athlete.current_belt_rank_id == int(self.filter_belt_rank_id)
            )
        with rx.session() as session:
            self.athletes = session.exec(query).all()
            self.available_age_categories = session.exec(
                sqlmodel.select(AgeCategory)
            ).all()
            self.available_belts = session.exec(
                sqlmodel.select(BeltRank).order_by(BeltRank.rank_order)
            ).all()

    @rx.event
    def set_search(self, query: str):
        self.search_query = query
        return AthleteState.load_athletes

    @rx.event
    def set_filter_age(self, value: str):
        self.filter_age_category_id = value
        return AthleteState.load_athletes

    @rx.event
    def set_filter_belt(self, value: str):
        self.filter_belt_rank_id = value
        return AthleteState.load_athletes

    @rx.event
    def open_add_modal(self):
        self.current_athlete_id = None
        self.form_full_name = ""
        self.form_dob = ""
        self.form_gender = "Male"
        self.form_phone = ""
        self.form_guardian = ""
        self.form_age_category_id = ""
        self.form_belt_rank_id = ""
        self.is_open = True

    @rx.event
    def open_edit_modal(self, athlete: Athlete):
        self.current_athlete_id = athlete.id
        self.form_full_name = athlete.full_name
        self.form_dob = athlete.date_of_birth
        self.form_gender = athlete.gender
        self.form_phone = athlete.phone or ""
        self.form_guardian = athlete.guardian_name or ""
        self.form_age_category_id = (
            str(athlete.age_category_id) if athlete.age_category_id else ""
        )
        self.form_belt_rank_id = (
            str(athlete.current_belt_rank_id) if athlete.current_belt_rank_id else ""
        )
        self.is_open = True

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    def open_upload_modal(self):
        self.is_upload_open = True
        self.upload_error = ""
        self.upload_success = ""

    @rx.event
    def close_upload_modal(self):
        self.is_upload_open = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        try:
            file = files[0]
            upload_data = await file.read()
            csv_text = upload_data.decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(csv_text))
            added_count = 0
            with rx.session() as session:
                for row in csv_reader:
                    if not row.get("full_name"):
                        continue
                    athlete = Athlete(
                        full_name=row.get("full_name", ""),
                        date_of_birth=row.get("date_of_birth", ""),
                        gender=row.get("gender", "Male"),
                        phone=row.get("phone", ""),
                        guardian_name=row.get("guardian_name", ""),
                        guardian_phone=row.get("guardian_phone", ""),
                        is_active=True,
                    )
                    session.add(athlete)
                    added_count += 1
                session.commit()
            self.upload_success = f"Successfully imported {added_count} athletes."
            self.upload_error = ""
            return AthleteState.load_athletes
        except Exception as e:
            logging.exception(f"Error importing CSV: {e}")
            self.upload_error = f"Error importing CSV: {str(e)}"
            self.upload_success = ""

    @rx.event
    async def save_athlete(self):
        with rx.session() as session:
            age_cat_id = (
                int(self.form_age_category_id)
                if self.form_age_category_id and self.form_age_category_id != ""
                else None
            )
            belt_rank_id = (
                int(self.form_belt_rank_id)
                if self.form_belt_rank_id and self.form_belt_rank_id != ""
                else None
            )
            if self.current_athlete_id:
                athlete = session.get(Athlete, self.current_athlete_id)
                if athlete:
                    athlete.full_name = self.form_full_name
                    athlete.date_of_birth = self.form_dob
                    athlete.gender = self.form_gender
                    athlete.phone = self.form_phone
                    athlete.guardian_name = self.form_guardian
                    athlete.age_category_id = age_cat_id
                    athlete.current_belt_rank_id = belt_rank_id
                    session.add(athlete)
            else:
                new_athlete = Athlete(
                    full_name=self.form_full_name,
                    date_of_birth=self.form_dob,
                    gender=self.form_gender,
                    phone=self.form_phone,
                    guardian_name=self.form_guardian,
                    age_category_id=age_cat_id,
                    current_belt_rank_id=belt_rank_id,
                )
                session.add(new_athlete)
            session.commit()
        self.is_open = False
        return AthleteState.load_athletes

    @rx.event
    async def delete_athlete(self, id: int):
        with rx.session() as session:
            athlete = session.get(Athlete, id)
            if athlete:
                athlete.is_active = False
                session.add(athlete)
                session.commit()
        return AthleteState.load_athletes