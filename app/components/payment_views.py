import reflex as rx
from app.states.payment_state import PaymentState, PaymentData
import datetime


def status_badge(status: str) -> rx.Component:
    color_map = {
        "Paid": "green",
        "Unpaid": "red",
        "Overdue": "orange",
        "Partial": "yellow",
    }
    color = color_map.get(status, "gray")
    return rx.el.span(
        status,
        class_name=f"px-2.5 py-0.5 rounded-full text-xs font-medium bg-{color}-100 text-{color}-800 dark:bg-{color}-900/30 dark:text-{color}-300",
    )


def payment_card(payment: PaymentData) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        payment.payment_date,
                        class_name="text-xs text-gray-500 dark:text-gray-400 mb-1",
                    ),
                    rx.el.h3(
                        payment.athlete_name,
                        class_name="text-lg font-bold text-gray-900 dark:text-white truncate",
                    ),
                    rx.el.p(
                        payment.payment_type,
                        class_name="text-sm text-violet-600 dark:text-violet-400 font-medium",
                    ),
                    class_name="flex-1",
                ),
                status_badge(payment.status),
                class_name="flex justify-between items-start mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Amount:", class_name="text-sm text-gray-500 dark:text-gray-400"
                    ),
                    rx.el.span(
                        f"{payment.amount:,.2f} DA",
                        class_name="text-sm font-bold text-gray-900 dark:text-white",
                    ),
                    class_name="flex justify-between items-center mb-1",
                ),
                rx.el.div(
                    rx.el.span(
                        "Period:", class_name="text-sm text-gray-500 dark:text-gray-400"
                    ),
                    rx.el.span(
                        payment.month_year,
                        class_name="text-sm text-gray-700 dark:text-gray-300",
                    ),
                    class_name="flex justify-between items-center",
                ),
                class_name="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-3 mb-4",
            ),
            class_name="p-5",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="w-4 h-4"),
                on_click=lambda: PaymentState.open_edit_modal(payment),
                class_name="p-2 text-gray-500 hover:text-violet-600 hover:bg-violet-50 rounded-lg transition-colors",
                title="Edit",
            ),
            rx.el.button(
                rx.icon("file-text", class_name="w-4 h-4"),
                on_click=lambda: PaymentState.download_receipt(payment.id),
                class_name="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors",
                title="Download Receipt",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                on_click=lambda: PaymentState.delete_payment(payment.id),
                class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                title="Delete",
            ),
            class_name="flex justify-end gap-1 px-5 py-3 border-t border-gray-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50",
        ),
        class_name="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-md transition-all duration-200",
    )


def stats_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 text-{color}-600 dark:text-{color}-400"),
            class_name=f"w-12 h-12 rounded-xl bg-{color}-50 dark:bg-{color}-900/20 flex items-center justify-center mb-4",
        ),
        rx.el.h3(
            title,
            class_name="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1",
        ),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900 dark:text-white"),
        class_name="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800",
    )


def payment_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(PaymentState.current_payment_id, "Edit Payment", "New Payment"),
                class_name="text-xl font-bold mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Athlete", class_name="block text-sm font-medium mb-1"),
                    rx.el.select(
                        rx.el.option("Select Athlete", value=""),
                        rx.foreach(
                            PaymentState.athletes,
                            lambda a: rx.el.option(a.full_name, value=a.id.to_string()),
                        ),
                        value=PaymentState.form_athlete_id,
                        on_change=PaymentState.set_form_athlete_id,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Amount (DA)", class_name="block text-sm font-medium mb-1"
                        ),
                        rx.el.input(
                            type="number",
                            on_change=PaymentState.set_form_amount,
                            class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                            default_value=PaymentState.form_amount.to_string(),
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Date", class_name="block text-sm font-medium mb-1"
                        ),
                        rx.el.input(
                            type="date",
                            on_change=PaymentState.set_form_date,
                            class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                            default_value=PaymentState.form_date,
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Type", class_name="block text-sm font-medium mb-1"
                        ),
                        rx.el.select(
                            rx.el.option("Monthly Fee", value="Monthly Fee"),
                            rx.el.option("Yearly License", value="Yearly License"),
                            rx.el.option("Equipment", value="Equipment"),
                            rx.el.option("Other", value="Other"),
                            value=PaymentState.form_type,
                            on_change=PaymentState.set_form_type,
                            class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Status", class_name="block text-sm font-medium mb-1"
                        ),
                        rx.el.select(
                            rx.el.option("Paid", value="Paid"),
                            rx.el.option("Unpaid", value="Unpaid"),
                            rx.el.option("Partial", value="Partial"),
                            rx.el.option("Overdue", value="Overdue"),
                            value=PaymentState.form_status,
                            on_change=PaymentState.set_form_status,
                            class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Period Covered", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                rx.Var.range(1, 13),
                                lambda m: rx.el.option(
                                    m.to_string(), value=m.to_string()
                                ),
                            ),
                            value=PaymentState.form_month.to_string(),
                            on_change=PaymentState.set_form_month,
                            class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        ),
                        rx.el.select(
                            rx.foreach(
                                rx.Var.range(2023, 2030),
                                lambda y: rx.el.option(
                                    y.to_string(), value=y.to_string()
                                ),
                            ),
                            value=PaymentState.form_year.to_string(),
                            on_change=PaymentState.set_form_year,
                            class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Notes", class_name="block text-sm font-medium mb-1"),
                    rx.el.textarea(
                        on_change=PaymentState.set_form_notes,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700 h-20",
                        default_value=PaymentState.form_notes,
                    ),
                    class_name="mb-4",
                ),
                class_name="space-y-1",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=PaymentState.close_modal,
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.button(
                    "Save Payment",
                    on_click=PaymentState.save_payment,
                    class_name="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700",
                ),
                class_name="flex justify-end gap-2 mt-6",
            ),
        ),
        open=PaymentState.is_open,
        on_open_change=PaymentState.set_is_open,
    )


def payments_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Financial Management",
                class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora']",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5"),
                "New Payment",
                on_click=PaymentState.open_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-xl hover:bg-violet-700 transition-colors shadow-sm font-medium",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            stats_card(
                "Total Revenue",
                f"{PaymentState.total_income:,.0f} DA",
                "wallet",
                "green",
            ),
            stats_card(
                "Monthly Revenue",
                f"{PaymentState.monthly_revenue:,.0f} DA",
                "bar-chart-3",
                "violet",
            ),
            stats_card(
                "Unpaid Fees",
                PaymentState.unpaid_count.to_string(),
                "badge_alert",
                "red",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search by athlete name...",
                    on_change=PaymentState.set_search,
                    class_name="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 focus:ring-2 focus:ring-violet-200 outline-none",
                    default_value=PaymentState.search_query,
                ),
                class_name="relative flex-1",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("All Statuses", value="all"),
                    rx.el.option("Paid", value="Paid"),
                    rx.el.option("Unpaid", value="Unpaid"),
                    rx.el.option("Overdue", value="Overdue"),
                    rx.el.option("Partial", value="Partial"),
                    value=PaymentState.status_filter,
                    on_change=PaymentState.set_status_filter,
                    class_name="px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 outline-none",
                ),
                rx.el.select(
                    rx.el.option("All Types", value="all"),
                    rx.el.option("Monthly Fee", value="Monthly Fee"),
                    rx.el.option("Yearly License", value="Yearly License"),
                    value=PaymentState.type_filter,
                    on_change=PaymentState.set_type_filter,
                    class_name="px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 dark:bg-gray-900 outline-none",
                ),
                class_name="flex gap-4",
            ),
            class_name="flex flex-col md:flex-row gap-4 mb-8",
        ),
        rx.cond(
            PaymentState.filtered_payments,
            rx.el.div(
                rx.foreach(PaymentState.filtered_payments, payment_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "receipt", class_name="w-12 h-12 text-gray-300 mb-4 mx-auto"
                    ),
                    rx.el.h3(
                        "No payments found",
                        class_name="text-lg font-medium text-gray-900 dark:text-white mb-1",
                    ),
                    rx.el.p(
                        "Try adjusting your search or filters",
                        class_name="text-gray-500",
                    ),
                    class_name="text-center py-12",
                ),
                class_name="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-8",
            ),
        ),
        payment_form(),
    )