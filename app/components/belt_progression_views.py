import reflex as rx
from app.states.belt_progression_state import BeltProgressionState
from app.models import BeltPromotion


def timeline_item(promotion: BeltPromotion) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name=f"w-4 h-4 rounded-full bg-{BeltProgressionState.belt_color_map[promotion.to_belt_id]}-500 border-2 border-white dark:border-gray-900 absolute -left-[9px] top-1"
            ),
            class_name="absolute left-0 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-800",
        ),
        rx.el.div(
            rx.el.p(
                promotion.promotion_date.to_string().split(" ")[0],
                class_name="text-xs text-gray-500 dark:text-gray-400 mb-1",
            ),
            rx.el.h4(
                rx.el.span("Promoted to ", class_name="text-gray-500 font-normal"),
                rx.el.span(
                    BeltProgressionState.belt_map[promotion.to_belt_id],
                    class_name="font-bold text-gray-900 dark:text-white",
                ),
                class_name="text-sm font-medium",
            ),
            rx.cond(
                promotion.examiner_name,
                rx.el.p(
                    f"Examiner: {promotion.examiner_name}",
                    class_name="text-xs text-gray-500 mt-1",
                ),
            ),
            rx.cond(
                promotion.notes,
                rx.el.p(
                    promotion.notes,
                    class_name="text-xs text-gray-600 dark:text-gray-300 mt-2 bg-gray-50 dark:bg-gray-800 p-2 rounded",
                ),
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-3 h-3"),
                "Delete",
                on_click=lambda: BeltProgressionState.delete_promotion(promotion.id),
                class_name="text-xs text-red-500 hover:text-red-700 flex items-center gap-1 mt-2",
            ),
            class_name="ml-6 pb-8",
        ),
        class_name="relative",
    )


def belt_progression_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.el.div(
                    rx.icon("medal", class_name="w-6 h-6 text-orange-500"),
                    rx.el.span(
                        f"Belt Progression: {BeltProgressionState.current_athlete_name}"
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="text-xl font-bold mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Promotion History",
                        class_name="text-sm font-semibold text-gray-900 dark:text-white mb-4",
                    ),
                    rx.el.div(
                        rx.cond(
                            BeltProgressionState.promotion_history,
                            rx.foreach(
                                BeltProgressionState.promotion_history, timeline_item
                            ),
                            rx.el.p(
                                "No promotions recorded yet.",
                                class_name="text-sm text-gray-500 italic",
                            ),
                        ),
                        class_name="max-h-[400px] overflow-y-auto pr-4",
                    ),
                    class_name="flex-1 border-r border-gray-100 dark:border-gray-800 pr-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Record New Promotion",
                        class_name="text-sm font-semibold text-gray-900 dark:text-white mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Promote To",
                            class_name="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Select Belt Rank", value=""),
                            rx.foreach(
                                BeltProgressionState.available_belts,
                                lambda b: rx.el.option(b.name, value=b.id.to_string()),
                            ),
                            value=BeltProgressionState.form_to_belt_id,
                            on_change=BeltProgressionState.set_form_to_belt_id,
                            class_name="w-full p-2 text-sm border rounded-lg dark:bg-gray-800 dark:border-gray-700 mb-3",
                        ),
                        rx.el.label(
                            "Date",
                            class_name="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1",
                        ),
                        rx.el.input(
                            type="date",
                            on_change=BeltProgressionState.set_form_date,
                            class_name="w-full p-2 text-sm border rounded-lg dark:bg-gray-800 dark:border-gray-700 mb-3",
                            default_value=BeltProgressionState.form_date,
                        ),
                        rx.el.label(
                            "Examiner",
                            class_name="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1",
                        ),
                        rx.el.input(
                            placeholder="Sensei Name",
                            on_change=BeltProgressionState.set_form_examiner,
                            class_name="w-full p-2 text-sm border rounded-lg dark:bg-gray-800 dark:border-gray-700 mb-3",
                            default_value=BeltProgressionState.form_examiner,
                        ),
                        rx.el.label(
                            "Notes",
                            class_name="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1",
                        ),
                        rx.el.textarea(
                            placeholder="Performance notes...",
                            on_change=BeltProgressionState.set_form_notes,
                            class_name="w-full p-2 text-sm border rounded-lg dark:bg-gray-800 dark:border-gray-700 mb-4 h-20",
                            default_value=BeltProgressionState.form_notes,
                        ),
                        rx.el.button(
                            "Record Promotion",
                            on_click=BeltProgressionState.add_promotion,
                            class_name="w-full py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm font-medium rounded-lg transition-colors shadow-sm",
                        ),
                        class_name="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-xl",
                    ),
                    class_name="w-72 pl-6",
                ),
                class_name="flex flex-col md:flex-row",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=BeltProgressionState.close_modal,
                    class_name="px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                class_name="flex justify-end mt-6 pt-4 border-t border-gray-100 dark:border-gray-800",
            ),
            class_name="max-w-3xl w-full",
        ),
        open=BeltProgressionState.is_open,
        on_open_change=BeltProgressionState.set_is_open,
    )