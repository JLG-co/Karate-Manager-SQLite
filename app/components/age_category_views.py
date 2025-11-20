import reflex as rx
from app.states.age_category_state import AgeCategoryState
from app.models import AgeCategory


def age_category_card(category: AgeCategory) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("users", class_name="w-8 h-8 text-violet-600"),
                class_name="w-16 h-16 rounded-full bg-violet-50 dark:bg-violet-900/20 flex items-center justify-center mx-auto mb-4",
            ),
            rx.el.h3(
                category.name,
                class_name="text-lg font-bold text-center text-gray-900 dark:text-white mb-1",
            ),
            rx.el.p(
                f"{category.min_age} - {category.max_age} years",
                class_name="text-sm text-center text-violet-600 dark:text-violet-400 font-medium mb-4",
            ),
            rx.el.p(
                category.description,
                class_name="text-sm text-center text-gray-500 dark:text-gray-400 mb-4 line-clamp-2",
            ),
            class_name="p-6",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="w-4 h-4"),
                "Edit",
                on_click=lambda: AgeCategoryState.open_edit_modal(category),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="w-4 h-4"),
                "Delete",
                on_click=lambda: AgeCategoryState.delete_category(category.id),
                class_name="flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors border-l border-gray-100 dark:border-gray-800",
            ),
            class_name="flex border-t border-gray-100 dark:border-gray-800",
        ),
        class_name="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden hover:shadow-md transition-shadow",
    )


def age_category_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(
                    AgeCategoryState.current_category_id,
                    "Edit Category",
                    "Add New Category",
                ),
                class_name="text-xl font-bold mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Category Name", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.input(
                        on_change=AgeCategoryState.set_form_name,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                        default_value=AgeCategoryState.form_name,
                        placeholder="e.g. Junior A",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Min Age", class_name="block text-sm font-medium mb-1"
                            ),
                            rx.el.input(
                                type="number",
                                on_change=AgeCategoryState.set_form_min_age,
                                class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                                default_value=AgeCategoryState.form_min_age.to_string(),
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Max Age", class_name="block text-sm font-medium mb-1"
                            ),
                            rx.el.input(
                                type="number",
                                on_change=AgeCategoryState.set_form_max_age,
                                class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700",
                                default_value=AgeCategoryState.form_max_age.to_string(),
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Description", class_name="block text-sm font-medium mb-1"
                    ),
                    rx.el.textarea(
                        on_change=AgeCategoryState.set_form_description,
                        class_name="w-full p-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700 h-24",
                        default_value=AgeCategoryState.form_description,
                    ),
                    class_name="mb-4",
                ),
                class_name="space-y-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=AgeCategoryState.close_modal,
                    class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg",
                ),
                rx.el.button(
                    "Save Category",
                    on_click=AgeCategoryState.save_category,
                    class_name="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700",
                ),
                class_name="flex justify-end gap-2 mt-6",
            ),
        ),
        open=AgeCategoryState.is_open,
        on_open_change=AgeCategoryState.set_is_open,
    )


def age_categories_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Age Categories",
                class_name="text-3xl font-bold text-gray-900 dark:text-white font-['Lora']",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5"),
                "Add Category",
                on_click=AgeCategoryState.open_add_modal,
                class_name="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors shadow-sm font-medium",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.foreach(AgeCategoryState.categories, age_category_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        age_category_form(),
    )