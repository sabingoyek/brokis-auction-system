import imp
from itertools import cycle
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

from pydantic import BaseModel

from .item import Item

# Shared properties
class AuctionBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on Auction creation
class AuctionCreate(AuctionBase):
    title: str
    cycle_duration: int = 5  # in minutes
    max_cycle_number: int = 3


# Properties to receive on Auction update
class AuctionUpdate(AuctionBase):
    cycle_duration: int = 5  # in minutes
    max_cycle_number: int = 3


# Properties shared by models stored in DB
class AuctionInDBBase(AuctionBase):
    id: int
    title: str
    owner_id: int
    creation_date: datetime
    start_date: datetime = None
    end_date: datetime = None
    cycle_duration: int = 5 # in minutes
    max_cycle_number: int = 3 
    status: str = "draft"

    class Config:
        orm_mode = True


# Properties to return to client
class Auction(AuctionInDBBase):
    items: List[Item] = []


# Properties properties stored in DB
class AuctionInDB(AuctionInDBBase):
    pass
