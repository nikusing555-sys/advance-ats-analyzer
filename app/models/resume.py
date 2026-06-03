from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from app.database.db import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    original_resume = Column(Text)

    rewritten_resume = Column(Text)

    ats_score = Column(Float)

    job_description = Column(Text)