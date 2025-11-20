import reflex as rx
from app.states.attendance_state import AttendanceState, AttendanceItem


def status_button(
    item: AttendanceItem, status: str, label: str, color: str, icon: str
) -> rx.Component:
    is_active = item.status == status
    return rx.el.button(
        rx.icon(icon, class_name="w-4 h-4"),
        rx.el.span(label, class_name="hidden sm:inline"),
        on_click=lambda: AttendanceState.mark_status(item.athlete_id, status),
        class_name=rx.cond(
            is_active,
            f"flex items-center gap-2 px-3 py-2 rounded-lg bg-{color}-100 text-{color}-700 border border-{color}-200 font-medium transition-colors",
            f"flex items-center gap-2 px-3 py-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800 transition-colors",
        ),
    )


def attendance_row(item: AttendanceItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("user", class_name="w-5 h-5 text-gray-400"),
                class_name="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.h4(
                    item.full_name,
                    class_name="font-medium text-gray-900 dark:text-white",
                ),
                rx.el.p(item.belt_name, class_name="text-xs text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-3 flex-1",
        ),
        rx.el.div(
            status_button(item, "Present", "Present", "green", "check"),
            status_button(item, "Late", "Late", "yellow", "clock"),
            status_button(item, "Absent", "Absent", "red", "x"),
            class_name="flex gap-2",
        ),
        class_name="flex items-center justify-between p-4 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 hover:shadow-sm transition-shadow",
    )


def stat_pill(label: str, value: int, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            label,
            class_name="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider",
        ),
        rx.el.span(
            value,
            class_name=f"text-xl font-bold text-{color}-600 dark:text-{color}-400",
        ),
        class_name="flex flex-col items-center justify-center bg-white dark:bg-gray-900 p-4 rounded-xl border border-gray-100 dark:border-gray-800 flex-1 shadow-sm",
    )


def attendance_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Daily Attendance",
                class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora']",
            ),
            rx.el.div(
                rx.el.input(
                    type="date",
                    on_change=AttendanceState.set_checkin_date,
                    class_name="px-4 py-2 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 font-medium outline-none focus:ring-2 focus:ring-blue-200",
                    default_value=AttendanceState.checkin_date,
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            stat_pill("Total Athletes", AttendanceState.total_count, "gray"),
            stat_pill("Present", AttendanceState.present_count, "green"),
            stat_pill("Late", AttendanceState.late_count, "yellow"),
            stat_pill("Absent", AttendanceState.absent_count, "red"),
            stat_pill("Rate", f"{AttendanceState.attendance_rate}%", "blue"),
            class_name="flex gap-4 mb-8 overflow-x-auto pb-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Quick search athlete...",
                    on_change=AttendanceState.set_search_query,
                    class_name="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 focus:ring-2 focus:ring-blue-200 outline-none",
                ),
                class_name="relative flex-1",
            ),
            rx.el.button(
                rx.icon("scan-barcode", class_name="w-5 h-5"),
                "Scan QR",
                class_name="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors shadow-sm font-medium",
            ),
            class_name="flex gap-4 mb-6",
        ),
        rx.el.div(
            rx.foreach(AttendanceState.filtered_attendance, attendance_row),
            class_name="space-y-3",
        ),
    )