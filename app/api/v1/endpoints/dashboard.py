from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.subscription import Subscription

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {
            "error": "User not found"
        }

    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()

    resume_count = db.query(Resume).filter(
        Resume.user_id == user_id
    ).count()

    plan_name = "Free"
    resume_limit = 1

    if subscription:

        plan_name = subscription.plan_name

        if subscription.plan_name == "Pro":
            resume_limit = 5

        elif subscription.plan_name == "Premium":
            resume_limit = 10

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "plan": plan_name,
        "active_subscription":
            subscription is not None,
        "resumes_uploaded":
            resume_count,
        "resume_limit":
            resume_limit,
        "remaining":
            max(0, resume_limit - resume_count)
    }