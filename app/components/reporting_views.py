import reflex as rx
from app.states.reporting_state import ReportingState


def stat_card_large(title: str, value: rx.Var, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-8 h-8 text-{color}-600"),
            class_name=f"w-16 h-16 rounded-2xl bg-{color}-50 flex items-center justify-center mb-4",
        ),
        rx.el.h3(title, class_name="text-lg font-medium text-gray-500 mb-2"),
        rx.el.p(value, class_name="text-4xl font-bold text-gray-900 dark:text-white"),
        class_name="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm",
    )


def reporting_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Reports & Analytics",
            class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora'] mb-8",
        ),
        rx.el.div(
            stat_card_large(
                "Total Athletes",
                ReportingState.total_athletes.to_string(),
                "users",
                "violet",
            ),
            stat_card_large(
                "Total Revenue",
                f"{ReportingState.total_income:,.0f} DA",
                "wallet",
                "green",
            ),
            stat_card_large(
                "Attendance Rate",
                f"{ReportingState.attendance_rate}%",
                "calendar-check",
                "blue",
            ),
            stat_card_large(
                "Recent Promotions",
                ReportingState.promotions_count.to_string(),
                "medal",
                "orange",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Export Data",
                    class_name="text-xl font-bold text-gray-900 dark:text-white mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Report Type", class_name="block text-sm font-medium mb-1"
                        ),
                        rx.el.select(
                            rx.el.option("Athletes List", value="Athletes"),
                            rx.el.option("Financial Report", value="Payments"),
                            rx.el.option("Attendance Log", value="Attendance"),
                            rx.el.option("Competition Results", value="Competitions"),
                            value=ReportingState.report_type,
                            on_change=ReportingState.set_report_type,
                            class_name="w-full p-3 border rounded-xl dark:bg-gray-800 dark:border-gray-700",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Start Date", class_name="block text-sm font-medium mb-1"
                        ),
                        rx.el.input(
                            type="date",
                            on_change=ReportingState.set_start_date,
                            class_name="w-full p-3 border rounded-xl dark:bg-gray-800 dark:border-gray-700",
                            default_value=ReportingState.start_date,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "End Date", class_name="block text-sm font-medium mb-1"
                        ),
                        rx.el.input(
                            type="date",
                            on_change=ReportingState.set_end_date,
                            class_name="w-full p-3 border rounded-xl dark:bg-gray-800 dark:border-gray-700",
                            default_value=ReportingState.end_date,
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("file-spreadsheet", class_name="w-5 h-5"),
                        "Export CSV",
                        on_click=ReportingState.generate_csv,
                        class_name="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-colors font-medium shadow-lg shadow-green-200",
                    ),
                    class_name="flex gap-4 justify-end",
                ),
                class_name="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800",
            ),
            class_name="max-w-4xl mx-auto",
        ),
    )