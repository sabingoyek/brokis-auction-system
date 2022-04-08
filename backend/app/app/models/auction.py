from email.policy import default
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Auction(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    status = Column(String, default="draft")
    cycle_duration = Column(Integer, default=5)     # duration in minutes
    max_cycle_number = Column(Integer, default=3)
    creation_date = Column(String, default=datetime.now())
    start_date = Column(String)
    end_date = Column(String)

    owner = relationship("User", back_populates="auctions")
    items = relationship("Item", back_populates="auction", cascade="all, delete", passive_deletes=True)
