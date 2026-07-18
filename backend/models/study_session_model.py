from pydantic import BaseModel
from typing import Optional


class StudySessionCreate(BaseModel):
    subject: str
    date: str  # YYYY-MM-DD
    minutes: int
    focus: int  # 1–10 scale
    study_method: str

    chapter_name: Optional[str] = None
    rating: Optional[int] = None
