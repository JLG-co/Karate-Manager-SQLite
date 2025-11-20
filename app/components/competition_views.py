import reflex as rx
from app.states.competition_state import CompetitionState
from app.states.competition_result_state import CompetitionResultState
from app.models import Competition


def competition_card(competition: Competition) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    competition.name,
                    class_name="text-lg font-bold text-gray-900 dark:text-white mb-1",
                ),
                rx.el.p(
                    competition.date.to_string().split(" ")[0],
                    class_name="text-sm text-violet-600 dark:text-violet-400 font-medium mb-2",
                ),
                rx.el.div(
                    rx.icon("map-pin", class_name="w-4 h-4 text-gray-400"),
                    rx.el.span(
                        competition.location,
                        class_name="text-sm text-gray-600 dark:text-gray-300",
                    ),
                    class_name="flex items-center gap-2 mb-4",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("trophy", class_name="w-5 h-5"),
                    "Manage Results",
                    on_click=lambda: CompetitionState.open_manage_modal(competition),
                    class_name="w-full flex items-center justify-center gap-2 py-2 bg-violet-50 text-violet-700 hover:bg-violet-100 dark:bg-violet-900/20 dark:text-violet-300 rounded-lg font-medium transition-colors mb-2",
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="p-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="w-4 h-4"),
                "Edit",
                on_click=lambda: CompetitionState.open_edit_modal(competition),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                "Delete",
                on_click=lambda: CompetitionState.delete_competition(competition.id),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors border-l border-gray-100 dark:border-gray-800",
            ),
            class_name="flex border-t border-gray-100 dark:border-gray-800",
        ),
        class_name="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-md transition-shadow",
    )


def competition_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    CompetitionState.current_competition_id,
                    "Edit Competition",
                    "New Competition",
                ),
                class_name="text-xl font-bold mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Competition Name", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        on_change=CompetitionState.set_form_name,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=CompetitionState.form_name,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Date", class_name="block text-sm font-medium mb-1"),
                    rx.el.input(
                        type="date",
                        on_change=CompetitionState.set_form_date,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=CompetitionState.form_date,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Location", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        on_change=CompetitionState.set_form_location,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=CompetitionState.form_location,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Description", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.textarea(
                        on_change=CompetitionState.set_form_description,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700 h-24",
                        default_value=CompetitionState.form_description,
                    ),
                    class_name="mb-4",
                ),
                class_name="space-y-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=CompetitionState.close_modal,
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.button(
                    "Save Competition",
                    on_click=CompetitionState.save_competition,
                    class_name="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700",
                ),
                class_name="flex justify-end gap-2 mt-6",
            ),
        ),
        open=CompetitionState.is_open,
        on_open_change=CompetitionState.set_is_open,
    )


def result_row(result) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            result.athlete_name,
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white",
        ),
        rx.el.td(
            result.category,
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400",
        ),
        rx.el.td(
            rx.el.select(
                rx.el.option("Registered", value="Registered"),
                rx.el.option("Gold", value="Gold"),
                rx.el.option("Silver", value="Silver"),
                rx.el.option("Bronze", value="Bronze"),
                rx.el.option("Participant", value="Participant"),
                value=result.result,
                on_change=lambda val: CompetitionResultState.update_result_status(
                    result.id, val
                ),
                class_name=rx.cond(
                    result.result == "Gold",
                    "text-yellow-600 font-bold bg-yellow-50 border-yellow-200",
                    rx.cond(
                        result.result == "Silver",
                        "text-gray-600 font-bold bg-gray-100 border-gray-200",
                        rx.cond(
                            result.result == "Bronze",
                            "text-orange-600 font-bold bg-orange-50 border-orange-200",
                            "text-gray-700 bg-white border-gray-200",
                        ),
                    ),
                )
                + " rounded-lg px-2 py-1 border text-sm outline-none",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                on_click=lambda: CompetitionResultState.delete_result(result.id),
                class_name="text-red-600 hover:text-red-800 p-2 hover:bg-red-50 rounded-lg transition-colors",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
    )


def manage_results_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.el.div(
                    rx.icon("trophy", class_name="w-6 h-6 text-violet-600"),
                    rx.el.span(f"Results: {CompetitionState.current_competition_name}"),
                    class_name="flex items-center gap-2",
                ),
                class_name="text-xl font-bold mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        "Add Athlete",
                        class_name="text-sm font-bold text-gray-900 dark:text-white mb-3",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("Select Athlete", value=""),
                            rx.foreach(
                                CompetitionResultState.available_athletes,
                                lambda a: rx.el.option(
                                    a.full_name, value=a.id.to_string()
                                ),
                            ),
                            value=CompetitionResultState.form_athlete_id,
                            on_change=CompetitionResultState.set_form_athlete_id,
                            class_name="flex-1 p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        ),
                        rx.el.select(
                            rx.el.option("Kumite", value="Kumite"),
                            rx.el.option("Kata", value="Kata"),
                            rx.el.option("Team Kata", value="Team Kata"),
                            rx.el.option("Team Kumite", value="Team Kumite"),
                            value=CompetitionResultState.form_category,
                            on_change=CompetitionResultState.set_form_category,
                            class_name="w-40 p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        ),
                        rx.el.button(
                            "Add",
                            on_click=CompetitionResultState.add_result,
                            class_name="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 font-medium",
                        ),
                        class_name="flex gap-2 mb-6 bg-gray-50 dark:bg-gray-900/50 p-4 rounded-xl",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h4(
                            "Participants & Results",
                            class_name="text-sm font-bold text-gray-900 dark:text-white",
                        ),
                        rx.el.button(
                            rx.icon("file-down", class_name="w-4 h-4"),
                            "Export PDF",
                            on_click=CompetitionResultState.generate_pdf,
                            class_name="flex items-center gap-2 px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors",
                        ),
                        class_name="flex items-center justify-between mb-3",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Athlete",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Category",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Result",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th("", class_name="px-6 py-3 text-right"),
                                ),
                                class_name="bg-gray-50 dark:bg-gray-800",
                            ),
                            rx.el.tbody(
                                rx.foreach(CompetitionResultState.results, result_row),
                                class_name="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800",
                            ),
                            class_name="min-w-full divide-y divide-gray-200 dark:divide-gray-800",
                        ),
                        class_name="border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden",
                    ),
                ),
                class_name="space-y-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=CompetitionState.close_manage_modal,
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                class_name="flex justify-end mt-6 pt-4 border-t border-gray-100 dark:border-gray-800",
            ),
            class_name="max-w-4xl w-full",
        ),
        open=CompetitionState.is_manage_open,
        on_open_change=CompetitionState.set_is_manage_open,
    )


def competitions_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Competitions",
                class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora']",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5"),
                "Add Competition",
                on_click=CompetitionState.open_add_modal,
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
                    placeholder="Search competitions...",
                    on_change=CompetitionState.set_search,
                    class_name="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 focus:ring-2 focus:ring-violet-200 outline-none",
                ),
                class_name="relative flex-1 max-w-md mb-8",
            )
        ),
        rx.cond(
            CompetitionState.competitions,
            rx.el.div(
                rx.foreach(CompetitionState.competitions, competition_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.el.p(
                    "No competitions found.",
                    class_name="text-gray-500 text-center py-12",
                )
            ),
        ),
        competition_form(),
        manage_results_modal(),
    )