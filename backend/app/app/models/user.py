from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

#if TYPE_CHECKING:
#    from .item import Item  # noqa: F401
#    from .auction import Auction
#    from .bid import Bid


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    first_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    
    auctions = relationship("Auction", back_populates="owner")
    bids = relationship("Bid", back_populates="owner")