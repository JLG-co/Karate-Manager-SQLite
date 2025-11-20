import reflex as rx
from app.states.settings_state import SettingsState


def setting_section_header(title: str, icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-6 h-6 text-{color}-600"),
            class_name=f"w-12 h-12 rounded-xl bg-{color}-50 flex items-center justify-center mb-4",
        ),
        rx.el.h2(
            title, class_name="text-xl font-bold text-gray-900 dark:text-white mb-4"
        ),
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "System Settings",
            class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora'] mb-8",
        ),
        rx.el.div(
            rx.el.div(
                setting_section_header("Financial Configuration", "coins", "violet"),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Monthly Subscription Fee (DA)",
                            class_name="block text-sm font-medium mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            on_change=SettingsState.set_monthly_fee,
                            class_name="w-full p-3 border rounded-xl dark:bg-gray-800 dark:border-gray-700",
                            default_value=SettingsState.monthly_fee,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Annual License Fee (DA)",
                            class_name="block text-sm font-medium mb-1",
                        ),
                        rx.el.input(
                            type="number",
                            on_change=SettingsState.set_yearly_license,
                            class_name="w-full p-3 border rounded-xl dark:bg-gray-800 dark:border-gray-700",
                            default_value=SettingsState.yearly_license,
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
                ),
                rx.el.button(
                    "Save Changes",
                    on_click=SettingsState.save_settings,
                    class_name="px-6 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 font-medium",
                ),
                class_name="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm",
            ),
            rx.el.div(
                setting_section_header("ID Cards", "id-card", "blue"),
                rx.el.p(
                    "Generate ID cards for all active athletes in the system. The PDF will contain printable cards formatted for A4 paper.",
                    class_name="text-gray-500 dark:text-gray-400 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("printer", class_name="w-5 h-5"),
                        "Generate All ID Cards",
                        on_click=SettingsState.generate_all_id_cards,
                        class_name="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors font-medium shadow-lg shadow-blue-200",
                    ),
                    rx.cond(
                        SettingsState.id_card_status,
                        rx.el.p(
                            SettingsState.id_card_status,
                            class_name="text-sm text-gray-500 mt-2",
                        ),
                    ),
                    class_name="flex flex-col items-start gap-2",
                ),
                class_name="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm",
            ),
            rx.el.div(
                setting_section_header("Backup & Restore", "database-backup", "orange"),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Backup Database",
                            class_name="font-bold text-gray-900 dark:text-white mb-2",
                        ),
                        rx.el.p(
                            "Create a full backup of the database. This will download a ZIP file containing all your data.",
                            class_name="text-sm text-gray-500 dark:text-gray-400 mb-4",
                        ),
                        rx.el.button(
                            rx.icon("download", class_name="w-4 h-4"),
                            "Download Backup",
                            on_click=SettingsState.backup_database,
                            class_name="flex items-center gap-2 px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors",
                        ),
                        rx.cond(
                            SettingsState.backup_status,
                            rx.el.p(
                                SettingsState.backup_status,
                                class_name="text-xs text-gray-500 mt-2",
                            ),
                        ),
                        class_name="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Restore Database",
                            class_name="font-bold text-gray-900 dark:text-white mb-2",
                        ),
                        rx.el.p(
                            "Restore data from a previous backup. WARNING: This will overwrite all current data.",
                            class_name="text-sm text-gray-500 dark:text-gray-400 mb-4",
                        ),
                        rx.upload.root(
                            rx.el.button(
                                rx.icon("upload", class_name="w-4 h-4"),
                                "Select Backup File",
                                class_name="flex items-center gap-2 px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors w-full justify-center",
                            ),
                            id="restore_upload",
                            accept={".zip": [".zip"]},
                            multiple=False,
                            class_name="mb-2",
                        ),
                        rx.el.button(
                            "Restore Now",
                            on_click=lambda: SettingsState.handle_restore_upload(
                                rx.upload_files("restore_upload")
                            ),
                            class_name="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium",
                        ),
                        rx.cond(
                            SettingsState.restore_status,
                            rx.el.p(
                                SettingsState.restore_status,
                                class_name="text-xs text-gray-500 mt-2",
                            ),
                        ),
                        class_name="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                ),
                class_name="bg-white dark:bg-gray-900 p-8 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm",
            ),
            class_name="space-y-6",
        ),
    )