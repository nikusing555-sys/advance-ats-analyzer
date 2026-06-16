from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.subscription import Subscription

router = APIRouter()


@router.get("/usage")
def get_usage(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()

    resumes_used = db.query(Resume).filter(
        Resume.user_id == user_id
    ).count()

    plan = "Free"
    resume_limit = 1

    if subscription:

        plan = subscription.plan_name

        if plan == "Pro":
            resume_limit = 5

        elif plan == "Premium":
            resume_limit = 10

    return {
        "user_id": user.id,
        "plan": plan,
        "resume_limit": resume_limit,
        "used": resumes_used,
        "remaining": max(
            0,
            resume_limit - resumes_used
        )
    }