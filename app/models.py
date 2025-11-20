import reflex as rx
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    role: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True


class BeltRank(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    color: str
    rank_order: int


class AgeCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    min_age: int
    max_age: int
    description: Optional[str] = None


class Athlete(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    date_of_birth: str
    gender: str
    address: Optional[str] = None
    phone: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    joined_date: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    current_belt_rank_id: Optional[int] = None
    age_category_id: Optional[int] = None


class Coach(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    specialization: Optional[str] = None
    phone: str
    email: Optional[str] = None
    joined_date: datetime = Field(default_factory=datetime.now)
    is_active: bool = True


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    athlete_id: int
    amount: float
    payment_type: str
    payment_date: datetime = Field(default_factory=datetime.now)
    month_covered: Optional[int] = None
    year_covered: Optional[int] = None
    status: str
    notes: Optional[str] = None


class Attendance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    athlete_id: int
    date: datetime = Field(default_factory=datetime.now)
    status: str
    class_time: Optional[str] = None


class Competition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: datetime
    location: str
    description: Optional[str] = None


class CompetitionResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    competition_id: int
    athlete_id: int
    result: str
    category: str


class BeltPromotion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    athlete_id: int
    from_belt_id: Optional[int] = None
    to_belt_id: int
    promotion_date: datetime = Field(default_factory=datetime.now)
    examiner_name: Optional[str] = None
    notes: Optional[str] = None
    media_files: Optional[str] = None


class Setting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    value: str
    description: Optional[str] = None