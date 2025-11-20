import reflex as rx
from app.states.auth_state import AuthState
from app.states.language_state import LanguageState
from app.states.global_state import GlobalState


def sidebar_item(icon: str, text: str, href: str = "#") -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5"),
            rx.el.span(text, class_name="font-medium"),
            class_name="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-violet-50 hover:text-violet-700 dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-white rounded-xl transition-all duration-200",
        ),
        href=href,
    )


def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.icon("swords", class_name="w-8 h-8 text-red-600 rtl:rotate-180"),
                    rx.el.span(
                        "Galia Manager",
                        class_name="text-xl font-bold text-gray-900 dark:text-white font-['Lora']",
                    ),
                    class_name="flex items-center gap-3 px-4 py-6 mb-4",
                ),
                rx.el.nav(
                    sidebar_item(
                        "layout-dashboard",
                        LanguageState.translations[LanguageState.current_lang][
                            "dashboard"
                        ],
                        "/",
                    ),
                    sidebar_item(
                        "users",
                        LanguageState.translations[LanguageState.current_lang][
                            "athletes"
                        ],
                        "/athletes",
                    ),
                    sidebar_item(
                        "user-cog",
                        LanguageState.translations[LanguageState.current_lang][
                            "coaches"
                        ],
                        "/coaches",
                    ),
                    sidebar_item(
                        "users-round",
                        LanguageState.translations[LanguageState.current_lang][
                            "age_categories"
                        ],
                        "/age-categories",
                    ),
                    sidebar_item(
                        "credit-card",
                        LanguageState.translations[LanguageState.current_lang][
                            "payments"
                        ],
                        "/payments",
                    ),
                    sidebar_item(
                        "calendar-check",
                        LanguageState.translations[LanguageState.current_lang][
                            "attendance"
                        ],
                        "/attendance",
                    ),
                    sidebar_item(
                        "trophy",
                        LanguageState.translations[LanguageState.current_lang][
                            "competitions"
                        ],
                        "/competitions",
                    ),
                    sidebar_item(
                        "bar-chart-3",
                        LanguageState.translations[LanguageState.current_lang][
                            "reports"
                        ],
                        "/reports",
                    ),
                    sidebar_item(
                        "settings",
                        LanguageState.translations[LanguageState.current_lang][
                            "settings"
                        ],
                        "/settings",
                    ),
                    class_name="flex flex-col gap-1 px-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "user",
                                class_name="w-5 h-5 text-gray-600 dark:text-gray-300",
                            ),
                            class_name="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center",
                        ),
                        rx.el.div(
                            rx.el.p(
                                AuthState.user.username,
                                class_name="text-sm font-semibold text-gray-900 dark:text-white",
                            ),
                            rx.el.p(
                                AuthState.user.role,
                                class_name="text-xs text-gray-500 dark:text-gray-400 capitalize",
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("English", value="en"),
                            rx.el.option("Français", value="fr"),
                            rx.el.option("العربية", value="ar"),
                            value=LanguageState.current_lang,
                            on_change=LanguageState.set_language,
                            class_name="p-1 text-xs border rounded dark:bg-gray-800 dark:border-gray-700",
                        ),
                        rx.color_mode.button(
                            class_name="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
                        ),
                        rx.el.button(
                            rx.icon(
                                "log-out",
                                class_name="w-5 h-5 text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 rtl:rotate-180",
                            ),
                            on_click=AuthState.logout,
                            class_name="p-2 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    class_name="mt-auto border-t border-gray-100 dark:border-gray-800 p-4 flex items-center justify-between",
                ),
                class_name="flex flex-col h-full",
            ),
            class_name="w-72 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 hidden md:block h-screen sticky top-0 shrink-0",
        ),
        rx.el.main(
            rx.el.div(content, class_name="max-w-7xl mx-auto"),
            class_name="flex-1 bg-gray-50 dark:bg-gray-950 min-h-screen p-4 md:p-8 overflow-y-auto",
        ),
        rx.window_event_listener(
            on_key_down=lambda key, ctrl_key: GlobalState.handle_global_shortcuts(
                key, ctrl_key
            )
        ),
        dir=rx.cond(LanguageState.is_rtl, "rtl", "ltr"),
        class_name="flex min-h-screen font-['Inter'] text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-900",
    )