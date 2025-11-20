import reflex as rx
from app.states.auth_state import AuthState


def login_field(
    label: str, type_: str, value_var: rx.Var, on_change_handler: rx.event.EventType
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-700 mb-1 font-['Lora']",
        ),
        rx.el.input(
            type=type_,
            default_value=value_var,
            on_change=on_change_handler,
            class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-red-500 focus:ring-2 focus:ring-red-200 transition-all duration-200 outline-none bg-gray-50 focus:bg-white",
            placeholder=f"Enter your {label.lower()}",
        ),
        class_name="mb-4",
    )


def login_component() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("swords", class_name="w-16 h-16 text-red-600 mb-6"),
                    rx.el.h1(
                        "Galia Club",
                        class_name="text-5xl font-bold text-white mb-2 font-['Lora'] tracking-tight",
                    ),
                    rx.el.h2(
                        "Karate Manager",
                        class_name="text-2xl font-light text-red-500 mb-8 tracking-widest uppercase",
                    ),
                    rx.el.p(
                        "Excellence through discipline and dedication.",
                        class_name="text-gray-400 text-lg max-w-md leading-relaxed",
                    ),
                    class_name="relative z-10 flex flex-col justify-center h-full px-12",
                ),
                rx.el.div(
                    class_name="absolute inset-0 bg-gradient-to-br from-neutral-900 via-neutral-900 to-neutral-800 z-0"
                ),
                rx.el.div(
                    class_name="absolute top-0 left-0 w-full h-full opacity-10 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-red-600 via-transparent to-transparent"
                ),
                class_name="hidden lg:block lg:w-1/2 relative overflow-hidden",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("swords", class_name="w-12 h-12 text-red-600 mb-6"),
                        rx.el.h2(
                            "Welcome Back",
                            class_name="text-3xl font-bold text-gray-900 mb-2 font-['Lora']",
                        ),
                        rx.el.p(
                            "Please sign in to your account",
                            class_name="text-gray-500 mb-8",
                        ),
                        rx.cond(
                            AuthState.login_error != "",
                            rx.el.div(
                                rx.icon("badge_alert", class_name="w-5 h-5 mr-2"),
                                rx.text(AuthState.login_error),
                                class_name="bg-red-50 text-red-600 p-4 rounded-xl mb-6 flex items-center text-sm font-medium animate-pulse",
                            ),
                        ),
                        rx.el.form(
                            login_field(
                                "Username",
                                "text",
                                AuthState.username,
                                AuthState.set_username,
                            ),
                            login_field(
                                "Password",
                                "password",
                                AuthState.password,
                                AuthState.set_password,
                            ),
                            rx.el.button(
                                "Sign In",
                                type="submit",
                                class_name="w-full bg-red-600 text-white font-semibold py-3.5 rounded-xl hover:bg-red-700 transition-all duration-200 shadow-lg shadow-red-200 mt-2 flex items-center justify-center gap-2",
                            ),
                            on_submit=AuthState.login,
                        ),
                        class_name="w-full max-w-md",
                    ),
                    class_name="flex items-center justify-center h-full p-8",
                ),
                class_name="w-full lg:w-1/2 bg-white",
            ),
            class_name="flex min-h-screen w-full shadow-2xl overflow-hidden rounded-none sm:rounded-3xl max-w-[1920px] mx-auto",
        ),
        class_name="min-h-screen bg-neutral-100 p-0 sm:p-4 md:p-8 flex items-center justify-center font-['Inter']",
    )