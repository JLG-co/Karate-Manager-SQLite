import reflex as rx
from typing import Optional
from app.models import AgeCategory
import sqlmodel
import logging


class AgeCategoryState(rx.State):
    categories: list[AgeCategory] = []
    is_open: bool = False
    current_category_id: Optional[int] = None
    form_name: str = ""
    form_min_age: int = 5
    form_max_age: int = 18
    form_description: str = ""

    @rx.event
    async def load_categories(self):
        with rx.session() as session:
            self.categories = session.exec(
                sqlmodel.select(AgeCategory).order_by(AgeCategory.min_age)
            ).all()

    @rx.event
    def set_form_min_age(self, value: str):
        if not value:
            self.form_min_age = 0
            return
        try:
            self.form_min_age = int(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def set_form_max_age(self, value: str):
        if not value:
            self.form_max_age = 0
            return
        try:
            self.form_max_age = int(value)
        except ValueError as e:
            logging.exception(f"Error: {e}")

    @rx.event
    def open_add_modal(self):
        self.current_category_id = None
        self.form_name = ""
        self.form_min_age = 5
        self.form_max_age = 18
        self.form_description = ""
        self.is_open = True

    @rx.event
    def open_edit_modal(self, category: AgeCategory):
        self.current_category_id = category.id
        self.form_name = category.name
        self.form_min_age = category.min_age
        self.form_max_age = category.max_age
        self.form_description = category.description or ""
        self.is_open = True

    @rx.event
    def close_modal(self):
        self.is_open = False

    @rx.event
    async def save_category(self):
        with rx.session() as session:
            if self.current_category_id:
                category = session.get(AgeCategory, self.current_category_id)
                if category:
                    category.name = self.form_name
                    category.min_age = self.form_min_age
                    category.max_age = self.form_max_age
                    category.description = self.form_description
                    session.add(category)
            else:
                new_category = AgeCategory(
                    name=self.form_name,
                    min_age=self.form_min_age,
                    max_age=self.form_max_age,
                    description=self.form_description,
                )
                session.add(new_category)
            session.commit()
        self.is_open = False
        return AgeCategoryState.load_categories

    @rx.event
    async def delete_category(self, id: int):
        with rx.session() as session:
            category = session.get(AgeCategory, id)
            if category:
                session.delete(category)
                session.commit()
        return AgeCategoryState.load_categories