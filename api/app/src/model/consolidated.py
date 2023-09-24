from datetime import date, datetime
from typing import Optional

from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import SQLModel, Field


class Consolidated(SQLModel, table=True):
    __tablename__ = "consolidated"
    __table_args__ = (
        PrimaryKeyConstraint('project_name', 'client_name', 'date'),
    )

    project_id: str
    project_name: str
    client_name: str
    date: date
    hours_billable: Optional[float]
    hours_unbillable: Optional[float]
    budgeted_time: Optional[float]
    current_spent_time: Optional[float]
    amount: Optional[float]
    cost: str
    profit: str
    amount_rate: str
    cost_rate: str
