import reflex as rx
from typing import Optional
from app.models import Competition, CompetitionResult, Athlete
import sqlmodel
import datetime
import logging


class CompetitionState(rx.State):
    competitions: list[Competition] = []
    search_query: str = ""
    is_open: bool = False
    is_manage_open: bool = False
    current_competition_id: Optional[int] = None
    current_competition_name: str = ""
    form_name: str = ""
    form_date: str = datetime.date.today().isoformat()
    form_location: str = ""
    form_description: str = ""

    @rx.event
    async def load_competitions(self):
        with rx.session() as session:
            query = sqlmodel.select(Competition)
            if self.search_query:
                query = query.where(Competition.name.contains(self.search_query))
            query = query.order_by(Competition.date.desc())
            self.competitions = session.exec(query).all()

    @rx.event
    def set_search(self, query: str):
        self.search_query = query
        return CompetitionState.load_competitions

    @rx.event
    def open_add_modal(self):
        self.current_competition_id = None
        self.form_name = ""
        self.form_date = datetime.date.today().isoformat()
        self.form_location = ""
        self.form_description = ""
        self.is_open = True

    @rx.event
    def open_edit_modal(self, competition: Competition):
        self.current_competition_id = competition.id
        self.form_name = competition.name
        self.form_date = competition.date.strftime("%Y-%m-%d")
        self.form_location = competition.location
        self.form_description = competition.description or ""
        self.is_open = True

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    def close_manage_modal(self):
        self.is_manage_open = False

    @rx.event
    async def open_manage_modal(self, competition: Competition):
        self.current_competition_id = competition.id
        self.current_competition_name = competition.name
        self.is_manage_open = True
        from app.states.competition_result_state import CompetitionResultState

        result_state = await self.get_state(CompetitionResultState)
        result_state.current_competition_id = competition.id
        return CompetitionResultState.load_data

    @rx.event
    async def save_competition(self):
        if not self.form_name or not self.form_date:
            return
        try:
            with rx.session() as session:
                comp_date = datetime.datetime.strptime(self.form_date, "%Y-%m-%d")
                if self.current_competition_id:
                    comp = session.get(Competition, self.current_competition_id)
                    if comp:
                        comp.name = self.form_name
                        comp.date = comp_date
                        comp.location = self.form_location
                        comp.description = self.form_description
                        session.add(comp)
                else:
                    comp = Competition(
                        name=self.form_name,
                        date=comp_date,
                        location=self.form_location,
                        description=self.form_description,
                    )
                    session.add(comp)
                session.commit()
            self.is_open = False
            return CompetitionState.load_competitions
        except Exception as e:
            logging.exception(f"Error saving competition: {e}")

    @rx.event
    async def delete_competition(self, id: int):
        try:
            with rx.session() as session:
                comp = session.get(Competition, id)
                if comp:
                    results = session.exec(
                        sqlmodel.select(CompetitionResult).where(
                            CompetitionResult.competition_id == id
                        )
                    ).all()
                    for r in results:
                        session.delete(r)
                    session.delete(comp)
                    session.commit()
            return CompetitionState.load_competitions
        except Exception as e:
            logging.exception(f"Error deleting competition: {e}")