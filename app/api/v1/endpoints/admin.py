from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.subscription import Subscription

router = APIRouter()


# =========================
# ALL USERS
# =========================

@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]


# =========================
# ALL RESUMES
# =========================

@router.get("/resumes")
def get_all_resumes(
    db: Session = Depends(get_db)
):

    resumes = db.query(Resume).all()

    return [
        {
            "resume_id": resume.id,
            "user_id": resume.user_id,
            "name": resume.name,
            "email": resume.email,
            "ats_score": resume.ats_score
        }
        for resume in resumes
    ]


# =========================
# ALL SUBSCRIPTIONS
# =========================

@router.get("/subscriptions")
def get_all_subscriptions(
    db: Session = Depends(get_db)
):

    subscriptions = db.query(
        Subscription
    ).all()

    return [
        {
            "id": sub.id,
            "user_id": sub.user_id,
            "plan_name": sub.plan_name,
            "amount": sub.amount,
            "payment_status": sub.payment_status,
            "is_active": sub.is_active
        }
        for sub in subscriptions
    ]


# =========================
# ADMIN STATS
# =========================

@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db)
):

    total_users = db.query(User).count()

    total_resumes = db.query(
        Resume
    ).count()

    total_subscriptions = db.query(
        Subscription
    ).count()

    active_subscriptions = db.query(
        Subscription
    ).filter(
        Subscription.is_active == True
    ).count()

    return {
        "total_users": total_users,
        "total_resumes": total_resumes,
        "total_subscriptions": total_subscriptions,
        "active_subscriptions": active_subscriptions
    }


# =========================
# DELETE USER
# =========================

@router.delete("/user/{user_id}")
def delete_user(
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

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted"
    }


# =========================
# DISABLE SUBSCRIPTION
# =========================

@router.put("/subscription/{user_id}")
def disable_subscription(
    user_id: int,
    db: Session = Depends(get_db)
):

    subscription = db.query(
        Subscription
    ).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    subscription.is_active = False

    db.commit()

    return {
        "message": "Subscription disabled"
    }