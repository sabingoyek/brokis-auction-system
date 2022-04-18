from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
"""
if TYPE_CHECKING:
    from app.models import *
    from .user import User  # noqa: F401
    from .auction import Auction
    from .bid import Bid
"""

class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    start_price= Column(Integer)
    picture_url = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    auction_id = Column(Integer, ForeignKey("auction.id"))

    auction = relationship("Auction", back_populates="items")
    bids = relationship("Bid", back_populates="item")
