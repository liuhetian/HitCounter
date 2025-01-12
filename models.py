from datetime import date, datetime
from sqlmodel import SQLModel, Field

class Visit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    path: str
    visit_time: datetime = Field(default_factory=datetime.now)
    visit_date: date = Field(default_factory=date.today, index=True)
