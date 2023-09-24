from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlmodel import SQLModel, Field


class TimeEntry(SQLModel, table=True):
    __tablename__ = "time_entry"

    id: Optional[int] = Field(None, primary_key=True, nullable=False)
    description: str
    user_id: str
    project_id: str
    project_name: str
    client_id: str
    client_name: str
    user_name: str
    activity: str
    quickbooks_invoice: str
    client_call: str
    non_billing_reason: str
    subject_matter: str
    time_interval_start: datetime
    time_interval_end: datetime
    start_date: str
    start_time: str
    end_dat: str
    end_time: str
    time_interval_duration: Optional[int]
    billable: bool
    amount: Optional[float]
    cost: str
    profit: str
    amount_rate: str
    cost_rate: str

