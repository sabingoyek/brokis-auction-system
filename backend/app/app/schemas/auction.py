from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import null

#if TYPE_CHECKING:
from .item import Item

# Shared properties
class AuctionBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on Auction creation
class AuctionCreate(AuctionBase):
    title: str



# Properties to receive on Auction update
class AuctionUpdate(AuctionBase):
    is_published: bool = True


# Properties shared by models stored in DB
class AuctionInDBBase(AuctionBase):
    id: int
    title: str
    owner_id: int
    creation_date: datetime
    cycle_duration: int = 5        # 5 minutes
    max_cycle_number: int = 3
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    is_published: bool = False
    is_active: bool = False

    class Config:
        orm_mode = True


# Properties to return to client
class Auction(AuctionInDBBase):
    items: List[Item] = []
    


# Properties properties stored in DB
class AuctionInDB(AuctionInDBBase):
    pass
