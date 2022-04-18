from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
"""
if TYPE_CHECKING:
    from .user import User  # noqa: F401
    from .item import Item
"""

class Bid(Base):
    id = Column(Integer, primary_key=True, index=True)
    bid_date = Column(String, default=datetime.now())
    price = Column(Integer)
    bidder_id = Column(Integer, ForeignKey("user.id"))
    item_id = Column(Integer, ForeignKey("item.id"))

    owner = relationship("User", back_populates="bids")
    item = relationship("Item", back_populates="bids")
