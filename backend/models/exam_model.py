from pydantic import BaseModel
from typing import Optional


class ExamCreate(BaseModel):
    subject: str
    date: str  # YYYY-MM-DD

    target_percentage: Optional[int] = 80
    current_percentage: Optional[int] = 0
    importance: Optional[int] = 3
