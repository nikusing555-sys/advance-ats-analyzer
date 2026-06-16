from sqlalchemy import Column, Integer, String, Boolean

from app.database.db import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)

    plan_name = Column(String, nullable=False)

    amount = Column(Integer, nullable=False)

    payment_id = Column(String, nullable=True)

    order_id = Column(String, nullable=True)

    payment_status = Column(
        String,
        default="Pending"
    )

    is_active = Column(
        Boolean,
        default=False
    )