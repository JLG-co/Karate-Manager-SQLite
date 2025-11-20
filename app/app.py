import reflex as rx
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState
from app.states.athlete_state import AthleteState
from app.states.coach_state import CoachState
from app.states.age_category_state import AgeCategoryState
from app.states.payment_state import PaymentState
from app.states.attendance_state import AttendanceState
from app.states.competition_state import CompetitionState
from app.states.reporting_state import ReportingState
from app.components.login_component import login_component
from app.components.dashboard_layout import dashboard_layout
from app.components.athlete_views import athletes_page, athlete_form
from app.components.coach_views import coaches_page
from app.components.age_category_views import age_categories_page
from app.components.payment_views import payments_page
from app.components.attendance_views import attendance_page
from app.components.competition_views import competitions_page
from app.components.reporting_views import reporting_page
from app.components.settings_views import settings_page
from app.states.settings_state import SettingsState


def dashboard_stat_card(
    title: str, value: rx.Var, color: str = "violet"
) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            title,
            class_name="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2",
        ),
        rx.el.p(
            value,
            class_name=f"text-3xl font-bold text-{color}-600 dark:text-{color}-400",
        ),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800",
    )


def recent_activity_item(athlete: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.icon("user-plus", class_name="w-5 h-5 text-green-500 mt-1"),
        rx.el.div(
            rx.el.p(
                rx.el.span("New athlete joined: ", class_name="text-gray-500"),
                rx.el.span(
                    athlete.full_name,
                    class_name="font-semibold text-gray-900 dark:text-white",
                ),
            ),
            rx.el.p(
                athlete.joined_date.to_string(), class_name="text-xs text-gray-400"
            ),
            class_name="flex-1",
        ),
        class_name="flex gap-4 p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-xl transition-colors",
    )


def quick_action_btn(
    icon: str, label: str, event: rx.event.EventType, color: str
) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="w-6 h-6 mb-2"),
        rx.el.span(label, class_name="text-sm font-medium"),
        on_click=event,
        class_name=f"flex flex-col items-center justify-center p-4 rounded-xl bg-{color}-50 text-{color}-700 hover:bg-{color}-100 dark:bg-{color}-900/20 dark:text-{color}-300 dark:hover:bg-{color}-900/30 transition-colors",
    )


def index() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        dashboard_layout(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        LanguageState.translations[LanguageState.current_lang][
                            "dashboard"
                        ],
                        class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora']",
                    ),
                    rx.el.p(
                        LanguageState.translations[LanguageState.current_lang][
                            "welcome_back"
                        ],
                        class_name="text-gray-500 dark:text-gray-400 mt-1",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    dashboard_stat_card(
                        LanguageState.translations[LanguageState.current_lang][
                            "total_athletes"
                        ],
                        DashboardState.total_athletes,
                        "violet",
                    ),
                    dashboard_stat_card(
                        LanguageState.translations[LanguageState.current_lang][
                            "active_coaches"
                        ],
                        DashboardState.active_coaches,
                        "blue",
                    ),
                    dashboard_stat_card(
                        LanguageState.translations[LanguageState.current_lang][
                            "monthly_revenue"
                        ],
                        f"{DashboardState.monthly_revenue} DA",
                        "green",
                    ),
                    dashboard_stat_card(
                        LanguageState.translations[LanguageState.current_lang][
                            "unpaid_fees"
                        ],
                        DashboardState.unpaid_count,
                        "red",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            LanguageState.translations[LanguageState.current_lang][
                                "quick_actions"
                            ],
                            class_name="text-xl font-bold text-gray-800 dark:text-white mb-4",
                        ),
                        rx.el.div(
                            quick_action_btn(
                                "user-plus",
                                LanguageState.translations[LanguageState.current_lang][
                                    "add_athlete"
                                ],
                                AthleteState.open_add_modal,
                                "violet",
                            ),
                            quick_action_btn(
                                "credit-card",
                                LanguageState.translations[LanguageState.current_lang][
                                    "record_payment"
                                ],
                                rx.redirect("/payments"),
                                "green",
                            ),
                            quick_action_btn(
                                "calendar-check",
                                LanguageState.translations[LanguageState.current_lang][
                                    "attendance"
                                ],
                                rx.redirect("/attendance"),
                                "blue",
                            ),
                            quick_action_btn(
                                "medal",
                                LanguageState.translations[LanguageState.current_lang][
                                    "add_result"
                                ],
                                rx.redirect("/competitions"),
                                "orange",
                            ),
                            class_name="grid grid-cols-2 sm:grid-cols-4 gap-4",
                        ),
                        class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            LanguageState.translations[LanguageState.current_lang][
                                "recent_activity"
                            ],
                            class_name="text-xl font-bold text-gray-800 dark:text-white mb-4",
                        ),
                        rx.el.div(
                            rx.cond(
                                DashboardState.recent_athletes,
                                rx.foreach(
                                    DashboardState.recent_athletes, recent_activity_item
                                ),
                                rx.el.p(
                                    LanguageState.translations[
                                        LanguageState.current_lang
                                    ]["no_activity"],
                                    class_name="text-gray-500 dark:text-gray-400 p-4 text-center",
                                ),
                            ),
                            class_name="space-y-1",
                        ),
                        class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
                ),
                athlete_form_hidden(),
            )
        ),
        login_component(),
    )


def athlete_form_hidden() -> rx.Component:
    return rx.cond(AthleteState.is_open, rx.fragment(athlete_form()), rx.fragment())


def protected_page(page_content: rx.Component) -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated, dashboard_layout(page_content), login_component()
    )


from app.states.global_state import GlobalState
from app.states.language_state import LanguageState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
        rx.script("""
            document.addEventListener('keydown', function(event) {
                if ((event.ctrlKey || event.metaKey) && (event.key === 's' || event.key === 'p' || event.key === 'n')) {
                    event.preventDefault();
                }
            });
            """),
    ],
)
app.add_page(
    index, route="/", on_load=[AuthState.initialize_database, DashboardState.load_stats]
)
app.add_page(
    index, route="/", on_load=[AuthState.initialize_database, DashboardState.load_stats]
)
app.add_page(
    lambda: protected_page(athletes_page()),
    route="/athletes",
    on_load=AthleteState.load_athletes,
)
app.add_page(
    lambda: protected_page(coaches_page()),
    route="/coaches",
    on_load=CoachState.load_coaches,
)
app.add_page(
    lambda: protected_page(age_categories_page()),
    route="/age-categories",
    on_load=AgeCategoryState.load_categories,
)
app.add_page(
    lambda: protected_page(payments_page()),
    route="/payments",
    on_load=PaymentState.load_data,
)
app.add_page(
    lambda: protected_page(attendance_page()),
    route="/attendance",
    on_load=AttendanceState.load_today_status,
)
app.add_page(
    lambda: protected_page(competitions_page()),
    route="/competitions",
    on_load=CompetitionState.load_competitions,
)
app.add_page(
    lambda: protected_page(reporting_page()),
    route="/reports",
    on_load=ReportingState.load_stats,
)
app.add_page(
    lambda: protected_page(settings_page()),
    route="/settings",
    on_load=SettingsState.load_settings,
)