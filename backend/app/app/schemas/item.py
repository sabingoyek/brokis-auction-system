from typing import Optional, TYPE_CHECKING, List

from pydantic import BaseModel

#if TYPE_CHECKING:
from .bid import Bid

# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str
    start_price: int
    picture_url: Optional[str]


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    start_price: int 
    picture_url: str
    owner_id: int
    auction_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    bids: List[Bid] = []


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
