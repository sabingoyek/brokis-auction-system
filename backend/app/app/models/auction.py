from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
"""
if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .item import Item
"""

class Auction(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    cycle_duration = Column(Integer, default=5)     # duration in minutes
    max_cycle_number = Column(Integer)
    start_date = Column(String)
    end_date = Column(String)
    is_published = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    creation_date = Column(String, default=datetime.now())
    
    owner = relationship("User", back_populates="auctions")
    items = relationship("Item", back_populates="auction", cascade="all, delete", passive_deletes=True)
