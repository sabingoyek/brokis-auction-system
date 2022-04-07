from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class BidBase(BaseModel):
    price: Optional[int] = None
    item_id: Optional[int] = None

# Properties to receive on Bid creation
class BidCreate(BidBase):
    price: int
    item_id: int

# Properties to receive on Bid update
# Not allowed
#class BidUpdate(BidBase):
#    pass


# Properties shared by models stored in DB
class BidInDBBase(BidBase):
    id: int
    price: int
    item_id: int
    bidder_id: int
    bid_date: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Bid(BidInDBBase):
    pass


# Properties properties stored in DB
class BidInDB(BidInDBBase):
    pass
