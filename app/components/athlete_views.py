import reflex as rx
from app.states.athlete_state import AthleteState
from app.states.belt_progression_state import BeltProgressionState
from app.states.settings_state import SettingsState
from app.components.belt_progression_views import belt_progression_modal
from app.models import Athlete


def athlete_card(athlete: Athlete) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("user", class_name="w-8 h-8 text-gray-400"),
                class_name="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mx-auto mb-4",
            ),
            rx.el.h3(
                athlete.full_name,
                class_name="text-lg font-bold text-center text-gray-900 dark:text-white mb-1",
            ),
            rx.el.p(
                athlete.gender,
                class_name="text-sm text-center text-gray-500 dark:text-gray-400 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("cake", class_name="w-4 h-4 text-gray-400"),
                    rx.el.span(
                        athlete.date_of_birth,
                        class_name="text-sm text-gray-600 dark:text-gray-300",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.div(
                    rx.icon("phone", class_name="w-4 h-4 text-gray-400"),
                    rx.el.span(
                        athlete.phone,
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
                rx.icon("medal", class_name="w-4 h-4"),
                "Belt",
                on_click=lambda: BeltProgressionState.open_modal(athlete),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-orange-600 hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors",
            ),
            rx.el.button(
                rx.icon("id-card", class_name="w-4 h-4"),
                "ID Card",
                on_click=lambda: SettingsState.generate_id_card(athlete.id),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors border-l border-gray-100 dark:border-gray-800",
            ),
            rx.el.button(
                rx.icon("pencil", class_name="w-4 h-4"),
                "Edit",
                on_click=lambda: AthleteState.open_edit_modal(athlete),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors border-l border-gray-100 dark:border-gray-800",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                "Delete",
                on_click=lambda: AthleteState.delete_athlete(athlete.id),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors border-l border-gray-100 dark:border-gray-800",
            ),
            class_name="flex border-t border-gray-100 dark:border-gray-800",
        ),
        class_name="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-md transition-shadow",
    )


def athlete_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AthleteState.current_athlete_id, "Edit Athlete", "Add New Athlete"
                ),
                class_name="text-xl font-bold mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Full Name", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        on_change=AthleteState.set_form_full_name,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=AthleteState.form_full_name,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Date of Birth", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        type="date",
                        on_change=AthleteState.set_form_dob,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=AthleteState.form_dob,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Gender", class_name="block text-sm font-medium mb-1"),
                    rx.el.select(
                        rx.el.option("Male", value="Male"),
                        rx.el.option("Female", value="Female"),
                        value=AthleteState.form_gender,
                        on_change=AthleteState.set_form_gender,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Phone", class_name="block text-sm font-medium mb-1"),
                    rx.el.input(
                        on_change=AthleteState.set_form_phone,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=AthleteState.form_phone,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Guardian Name", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        on_change=AthleteState.set_form_guardian,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=AthleteState.form_guardian,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Age Category", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.select(
                        rx.el.option("Select Category", value=""),
                        rx.foreach(
                            AthleteState.available_age_categories,
                            lambda cat: rx.el.option(
                                cat.name, value=cat.id.to_string()
                            ),
                        ),
                        value=AthleteState.form_age_category_id,
                        on_change=AthleteState.set_form_age_category_id,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Belt Rank", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.select(
                        rx.el.option("Select Belt", value=""),
                        rx.foreach(
                            AthleteState.available_belts,
                            lambda belt: rx.el.option(
                                belt.name, value=belt.id.to_string()
                            ),
                        ),
                        value=AthleteState.form_belt_rank_id,
                        on_change=AthleteState.set_form_belt_rank_id,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                    ),
                    class_name="mb-4",
                ),
                class_name="space-y-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=AthleteState.close_modal,
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.button(
                    "Save Athlete",
                    on_click=AthleteState.save_athlete,
                    class_name="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700",
                ),
                class_name="flex justify-end gap-2 mt-6",
            ),
        ),
        open=AthleteState.is_open,
        on_open_change=AthleteState.set_is_open,
    )


def athletes_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Athletes",
                class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora']",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5"),
                "Add Athlete",
                on_click=AthleteState.open_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors shadow-sm font-medium",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search athletes...",
                    on_change=AthleteState.set_search,
                    class_name="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 focus:ring-2 focus:ring-violet-200 outline-none",
                    default_value=AthleteState.search_query,
                ),
                class_name="relative flex-1",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("All Categories", value="all"),
                    rx.foreach(
                        AthleteState.available_age_categories,
                        lambda cat: rx.el.option(cat.name, value=cat.id.to_string()),
                    ),
                    on_change=AthleteState.set_filter_age,
                    class_name="px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 outline-none",
                ),
                rx.el.select(
                    rx.el.option("All Belts", value="all"),
                    rx.foreach(
                        AthleteState.available_belts,
                        lambda belt: rx.el.option(belt.name, value=belt.id.to_string()),
                    ),
                    on_change=AthleteState.set_filter_belt,
                    class_name="px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 outline-none",
                ),
                rx.el.button(
                    rx.icon("upload", class_name="w-5 h-5"),
                    "Import CSV",
                    on_click=AthleteState.open_upload_modal,
                    class_name="flex items-center gap-2 px-4 py-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-xl transition-colors font-medium",
                ),
                class_name="flex gap-4",
            ),
            class_name="flex flex-col md:flex-row gap-4 mb-8",
        ),
        rx.el.div(
            rx.foreach(AthleteState.athletes, athlete_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        athlete_form(),
        belt_progression_modal(),
        upload_modal(),
    )


def upload_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                "Import Athletes from CSV", class_name="text-xl font-bold mb-4"
            ),
            rx.el.div(
                rx.el.p(
                    "Upload a CSV file with the following columns: full_name, date_of_birth, gender, phone, guardian_name, guardian_phone",
                    class_name="text-sm text-gray-500 mb-4",
                ),
                rx.upload.root(
                    rx.el.div(
                        rx.icon(
                            "upload", class_name="w-8 h-8 text-gray-400 mb-2 mx-auto"
                        ),
                        rx.el.p(
                            "Drag and drop or click to select file",
                            class_name="text-center text-sm text-gray-500",
                        ),
                        class_name="border-2 border-dashed border-gray-300 rounded-xl p-8 hover:bg-gray-50 transition-colors cursor-pointer",
                    ),
                    id="upload_csv",
                    accept={"text/csv": [".csv"]},
                    multiple=False,
                ),
                rx.cond(
                    AthleteState.upload_error,
                    rx.el.div(
                        rx.icon("badge_alert", class_name="w-4 h-4 mr-2"),
                        AthleteState.upload_error,
                        class_name="mt-4 p-3 bg-red-50 text-red-600 rounded-lg text-sm flex items-center",
                    ),
                ),
                rx.cond(
                    AthleteState.upload_success,
                    rx.el.div(
                        rx.icon("check_check", class_name="w-4 h-4 mr-2"),
                        AthleteState.upload_success,
                        class_name="mt-4 p-3 bg-green-50 text-green-600 rounded-lg text-sm flex items-center",
                    ),
                ),
                class_name="space-y-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=AthleteState.close_upload_modal,
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.button(
                    "Import",
                    on_click=lambda: AthleteState.handle_upload(
                        rx.upload_files("upload_csv")
                    ),
                    class_name="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700",
                ),
                class_name="flex justify-end gap-2 mt-6",
            ),
        ),
        open=AthleteState.is_upload_open,
        on_open_change=AthleteState.set_is_upload_open,
    )