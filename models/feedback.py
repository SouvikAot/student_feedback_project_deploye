from dataclasses import dataclass
from datetime import datetime

@dataclass
class Feedback:
    feedback_id: int = None
    student_id: int = None
    course_id: int = None
    rating: int = 0
    comments: str = ""
    created_at: datetime = None
