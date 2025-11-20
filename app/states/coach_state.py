import reflex as rx
from typing import Optional
from app.models import Coach
import sqlmodel


class CoachState(rx.State):
    coaches: list[Coach] = []
    is_open: bool = False
    current_coach_id: Optional[int] = None
    form_name: str = ""
    form_spec: str = ""
    form_phone: str = ""
    form_email: str = ""

    @rx.event
    async def load_coaches(self):
        with rx.session() as session:
            self.coaches = session.exec(
                sqlmodel.select(Coach).where(Coach.is_active == True)
            ).all()

    @rx.event
    def open_add_modal(self):
        self.current_coach_id = None
        self.form_name = ""
        self.form_spec = ""
        self.form_phone = ""
        self.form_email = ""
        self.is_open = True

    @rx.event
    def open_edit_modal(self, coach: Coach):
        self.current_coach_id = coach.id
        self.form_name = coach.full_name
        self.form_spec = coach.specialization or ""
        self.form_phone = coach.phone
        self.form_email = coach.email or ""
        self.is_open = True

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    async def save_coach(self):
        with rx.session() as session:
            if self.current_coach_id:
                coach = session.get(Coach, self.current_coach_id)
                if coach:
                    coach.full_name = self.form_name
                    coach.specialization = self.form_spec
                    coach.phone = self.form_phone
                    coach.email = self.form_email
                    session.add(coach)
            else:
                new_coach = Coach(
                    full_name=self.form_name,
                    specialization=self.form_spec,
                    phone=self.form_phone,
                    email=self.form_email,
                )
                session.add(new_coach)
            session.commit()
        self.is_open = False
        return CoachState.load_coaches

    @rx.event
    async def delete_coach(self, id: int):
        with rx.session() as session:
            coach = session.get(Coach, id)
            if coach:
                coach.is_active = False
                session.add(coach)
                session.commit()
        return CoachState.load_coaches