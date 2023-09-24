from datetime import datetime
from typing import Optional

from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import SQLModel


class ConsolidatedHistory(SQLModel, table=True):
    __tablename__ = "consolidated_history"
    __table_args__ = (
        PrimaryKeyConstraint('project_name', 'client_name', 'date'),
    )

    project_id: str
    project_name: str
    client_name: str
    date: datetime
    hours_billable: Optional[float]
    hours_unbillable: Optional[float]
    budgeted_time: Optional[float]
    current_spent_time: Optional[float]
    amount: Optional[float]
    cost: str
    profit: str
    amount_rate: str
    cost_rate: str
