import reflex as rx
from app.states.athlete_state import AthleteState
from app.states.payment_state import PaymentState


class GlobalState(rx.State):
    @rx.event
    def handle_key_down(self, key: str):
        if key == "s" and True:
            pass
        pass

    @rx.event
    def handle_global_shortcuts(self, key: str, ctrl_key: bool):
        if key == "s" and ctrl_key:
            if self.router.page.path == "/athletes":
                yield AthleteState.save_athlete
            elif self.router.page.path == "/payments":
                yield PaymentState.save_payment
        elif key == "p" and ctrl_key:
            yield rx.call_script("window.print();")
        elif key == "Escape":
            yield AthleteState.close_modal
            yield PaymentState.close_modal
        elif key == "n" and ctrl_key:
            if self.router.page.path == "/athletes":
                yield AthleteState.open_add_modal
            elif self.router.page.path == "/payments":
                yield PaymentState.open_add_modal