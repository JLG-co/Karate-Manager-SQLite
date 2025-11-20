import reflex as rx
from typing import Optional
from app.models import Athlete, BeltRank, BeltPromotion
import sqlmodel
import datetime
import logging


class BeltProgressionState(rx.State):
    is_open: bool = False
    current_athlete: Optional[Athlete] = None
    current_athlete_name: str = ""
    promotion_history: list[BeltPromotion] = []
    available_belts: list[BeltRank] = []
    form_to_belt_id: str = ""
    form_date: str = datetime.date.today().isoformat()
    form_examiner: str = ""
    form_notes: str = ""

    @rx.event
    async def open_modal(self, athlete: Athlete):
        self.current_athlete = athlete
        self.current_athlete_name = athlete.full_name
        self.is_open = True
        await self.load_data()

    @rx.event
    async def load_data(self):
        if not self.current_athlete:
            return
        with rx.session() as session:
            self.current_athlete = session.get(Athlete, self.current_athlete.id)
            self.available_belts = session.exec(
                sqlmodel.select(BeltRank).order_by(BeltRank.rank_order)
            ).all()
            self.promotion_history = session.exec(
                sqlmodel.select(BeltPromotion)
                .where(BeltPromotion.athlete_id == self.current_athlete.id)
                .order_by(BeltPromotion.promotion_date.desc())
            ).all()

    @rx.event
    def set_form_to_belt_id(self, value: str):
        self.form_to_belt_id = value

    @rx.event
    def set_form_date(self, value: str):
        self.form_date = value

    @rx.event
    def set_form_examiner(self, value: str):
        self.form_examiner = value

    @rx.event
    def set_form_notes(self, value: str):
        self.form_notes = value

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    async def add_promotion(self):
        if not self.current_athlete or not self.form_to_belt_id:
            return
        try:
            with rx.session() as session:
                new_belt_id = int(self.form_to_belt_id)
                promotion = BeltPromotion(
                    athlete_id=self.current_athlete.id,
                    from_belt_id=self.current_athlete.current_belt_rank_id,
                    to_belt_id=new_belt_id,
                    promotion_date=datetime.datetime.fromisoformat(self.form_date),
                    examiner_name=self.form_examiner,
                    notes=self.form_notes,
                )
                session.add(promotion)
                athlete = session.get(Athlete, self.current_athlete.id)
                athlete.current_belt_rank_id = new_belt_id
                session.add(athlete)
                session.commit()
            self.form_to_belt_id = ""
            self.form_examiner = ""
            self.form_notes = ""
            await self.load_data()
            from app.states.athlete_state import AthleteState

            state = await self.get_state(AthleteState)
            await state.load_athletes()
        except Exception as e:
            logging.exception(f"Error adding promotion: {e}")

    @rx.event
    async def delete_promotion(self, promotion_id: int):
        try:
            with rx.session() as session:
                promotion = session.get(BeltPromotion, promotion_id)
                if promotion:
                    session.delete(promotion)
                    session.commit()
            await self.load_data()
        except Exception as e:
            logging.exception(f"Error deleting promotion: {e}")

    @rx.var
    def belt_map(self) -> dict[int, str]:
        return {b.id: b.name for b in self.available_belts}

    @rx.var
    def belt_color_map(self) -> dict[int, str]:
        return {b.id: b.color for b in self.available_belts}