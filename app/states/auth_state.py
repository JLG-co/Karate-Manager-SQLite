import reflex as rx
from typing import Optional
import logging
from app.models import (
    User,
    BeltRank,
    AgeCategory,
    Athlete,
    Coach,
    Payment,
    Attendance,
    Competition,
    CompetitionResult,
    Setting,
)
import bcrypt
import sqlmodel
from sqlmodel import SQLModel


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    user: Optional[User] = None
    is_authenticated: bool = False
    login_error: str = ""

    @rx.event
    async def check_login(self):
        """Check if user is already logged in (client-side session persistence would go here)"""
        pass

    @rx.event
    async def login(self):
        """Handle login submission."""
        self.login_error = ""
        if not self.username or not self.password:
            self.login_error = "Please enter both username and password."
            return
        if self.username == "admin":
            try:
                expected_password_bytes = b"admin123"
                stored_hash = bcrypt.hashpw(expected_password_bytes, bcrypt.gensalt())
                entered_password_bytes = self.password.encode("utf-8")
                if bcrypt.checkpw(entered_password_bytes, stored_hash):
                    mock_user = User(
                        username="admin",
                        password_hash=stored_hash.decode("utf-8"),
                        role="admin",
                        is_active=True,
                    )
                    if not mock_user.is_active:
                        self.login_error = "Account is deactivated."
                        return
                    self.user = mock_user
                    self.is_authenticated = True
                    self.password = ""
                    return rx.redirect("/")
                else:
                    self.login_error = "Invalid username or password."
                    self.is_authenticated = False
            except Exception as e:
                logging.exception(f"Login error during bcrypt operation: {e}")
                self.login_error = "An error occurred during login verification."
                self.is_authenticated = False
        else:
            self.login_error = "Invalid username or password."
            self.is_authenticated = False

    @rx.event
    def logout(self):
        """Handle logout."""
        self.user = None
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        return rx.redirect("/")

    @rx.event(background=True)
    async def initialize_database(self):
        """Initialize the database with default admin and settings if they don't exist."""
        async with self:
            try:
                with rx.session() as session:
                    engine = session.get_bind()
                    SQLModel.metadata.create_all(engine)
                    admin = session.exec(
                        sqlmodel.select(User).where(User.username == "admin")
                    ).first()
                    if not admin:
                        password_bytes = b"admin123"
                        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode(
                            "utf-8"
                        )
                        admin_user = User(
                            username="admin",
                            password_hash=hashed,
                            role="admin",
                            is_active=True,
                        )
                        session.add(admin_user)
                        logging.info("Admin user created.")
                    if not session.exec(sqlmodel.select(BeltRank)).first():
                        belts = [
                            BeltRank(name="White", color="white", rank_order=1),
                            BeltRank(name="Yellow", color="yellow", rank_order=2),
                            BeltRank(name="Orange", color="orange", rank_order=3),
                            BeltRank(name="Green", color="green", rank_order=4),
                            BeltRank(name="Blue", color="blue", rank_order=5),
                            BeltRank(name="Purple", color="purple", rank_order=6),
                            BeltRank(name="Brown", color="brown", rank_order=7),
                            BeltRank(name="Black", color="black", rank_order=8),
                        ]
                        for belt in belts:
                            session.add(belt)
                        logging.info("Default belt ranks created.")
                    if not session.exec(sqlmodel.select(AgeCategory)).first():
                        categories = [
                            AgeCategory(
                                name="Mini",
                                min_age=5,
                                max_age=7,
                                description="Beginners 5-7 years",
                            ),
                            AgeCategory(
                                name="Poussins",
                                min_age=8,
                                max_age=9,
                                description="Kids 8-9 years",
                            ),
                            AgeCategory(
                                name="Benjamins",
                                min_age=10,
                                max_age=11,
                                description="Kids 10-11 years",
                            ),
                            AgeCategory(
                                name="Minimes",
                                min_age=12,
                                max_age=13,
                                description="Teens 12-13 years",
                            ),
                            AgeCategory(
                                name="Cadets",
                                min_age=14,
                                max_age=15,
                                description="Teens 14-15 years",
                            ),
                            AgeCategory(
                                name="Juniors",
                                min_age=16,
                                max_age=17,
                                description="Teens 16-17 years",
                            ),
                            AgeCategory(
                                name="Seniors",
                                min_age=18,
                                max_age=99,
                                description="Adults 18+ years",
                            ),
                        ]
                        for cat in categories:
                            session.add(cat)
                        logging.info("Default age categories created.")
                    if not session.exec(
                        sqlmodel.select(Setting).where(Setting.key == "monthly_fee")
                    ).first():
                        session.add(
                            Setting(
                                key="monthly_fee",
                                value="500",
                                description="Monthly subscription fee in DA",
                            )
                        )
                    if not session.exec(
                        sqlmodel.select(Setting).where(Setting.key == "yearly_license")
                    ).first():
                        session.add(
                            Setting(
                                key="yearly_license",
                                value="300",
                                description="Annual license fee in DA",
                            )
                        )
                    session.commit()
                    logging.info("Database initialized successfully.")
            except Exception as e:
                logging.exception(f"Database initialization failed: {e}")