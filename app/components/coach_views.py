import reflex as rx
from app.states.coach_state import CoachState
from app.models import Coach


def coach_card(coach: Coach) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("user-cog", class_name="w-8 h-8 text-violet-600"),
                class_name="w-16 h-16 rounded-full bg-violet-50 dark:bg-violet-900/20 flex items-center justify-center mx-auto mb-4",
            ),
            rx.el.h3(
                coach.full_name,
                class_name="text-lg font-bold text-center text-gray-900 dark:text-white mb-1",
            ),
            rx.el.p(
                coach.specialization,
                class_name="text-sm text-center text-violet-600 dark:text-violet-400 font-medium mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("phone", class_name="w-4 h-4 text-gray-400"),
                    rx.el.span(
                        coach.phone,
                        class_name="text-sm text-gray-600 dark:text-gray-300",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.div(
                    rx.icon("mail", class_name="w-4 h-4 text-gray-400"),
                    rx.el.span(
                        coach.email,
                        class_name="text-sm text-gray-600 dark:text-gray-300",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                class_name="bg-gray-50 dark:bg-gray-800/50 p-3 rounded-lg",
            ),
            class_name="p-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="w-4 h-4"),
                "Edit",
                on_click=lambda: CoachState.open_edit_modal(coach),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                "Delete",
                on_click=lambda: CoachState.delete_coach(coach.id),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors border-l border-gray-100 dark:border-gray-800",
            ),
            class_name="flex border-t border-gray-100 dark:border-gray-800",
        ),
        class_name="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-md transition-shadow",
    )


def coach_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(CoachState.current_coach_id, "Edit Coach", "Add New Coach"),
                class_name="text-xl font-bold mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Full Name", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        on_change=CoachState.set_form_name,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=CoachState.form_name,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Specialization", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        on_change=CoachState.set_form_spec,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=CoachState.form_spec,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Phone", class_name="block text-sm font-medium mb-1"),
                    rx.el.input(
                        on_change=CoachState.set_form_phone,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=CoachState.form_phone,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Email", class_name="block text-sm font-medium mb-1"),
                    rx.el.input(
                        on_change=CoachState.set_form_email,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=CoachState.form_email,
                    ),
                    class_name="mb-4",
                ),
                class_name="space-y-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=CoachState.close_modal,
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.button(
                    "Save Coach",
                    on_click=CoachState.save_coach,
                    class_name="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700",
                ),
                class_name="flex justify-end gap-2 mt-6",
            ),
        ),
        open=CoachState.is_open,
        on_open_change=CoachState.set_is_open,
    )


def coaches_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Coaches",
                class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora']",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5"),
                "Add Coach",
                on_click=CoachState.open_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors shadow-sm font-medium",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.foreach(CoachState.coaches, coach_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        coach_form(),
    )