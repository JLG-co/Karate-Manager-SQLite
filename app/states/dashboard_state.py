import reflex as rx
from app.models import Athlete, Coach, Payment
import datetime
import sqlmodel
from app.states.language_state import LanguageState


class DashboardState(rx.State):
    total_athletes: int = 0
    active_coaches: int = 0
    monthly_revenue: float = 0.0
    recent_athletes: list[Athlete] = []
    unpaid_count: int = 0
    notifications_checked: bool = False

    @rx.event
    async def load_stats(self):
        with rx.session() as session:
            self.total_athletes = (
                session.exec(sqlmodel.select(Athlete).where(Athlete.is_active == True))
                .all()
                .__len__()
            )
            self.active_coaches = (
                session.exec(sqlmodel.select(Coach).where(Coach.is_active == True))
                .all()
                .__len__()
            )
            now = datetime.datetime.now()
            payments = session.exec(
                sqlmodel.select(Payment).where(
                    (Payment.month_covered == now.month)
                    & (Payment.year_covered == now.year)
                )
            ).all()
            self.monthly_revenue = sum([p.amount for p in payments])
            self.recent_athletes = session.exec(
                sqlmodel.select(Athlete)
                .where(Athlete.is_active == True)
                .order_by(Athlete.joined_date.desc())
                .limit(5)
            ).all()
            paid_athlete_ids = set([p.athlete_id for p in payments])
            self.unpaid_count = max(0, self.total_athletes - len(paid_athlete_ids))
        if not self.notifications_checked and self.unpaid_count > 0:
            self.notifications_checked = True
            lang_state = await self.get_state(LanguageState)
            alert_msg = lang_state.translations[lang_state.current_lang]["unpaid_alert"]
            yield rx.toast(
                f"{self.unpaid_count} {alert_msg}",
                title=lang_state.translations[lang_state.current_lang]["notifications"],
                duration=5000,
                close_button=True,
                position="bottom-right",
                style={
                    "background_color": "#FEF2F2",
                    "color": "#DC2626",
                    "border": "1px solid #FECACA",
                },
            )