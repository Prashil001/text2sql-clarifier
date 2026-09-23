from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.database.base import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    order_date: Mapped[datetime] = mapped_column(DateTime)

    total_amount: Mapped[float] = mapped_column(Numeric(10,2))

    customer = relationship("Customer", back_populates="orders")

    items = relationship("OrderItem", back_populates="order")


