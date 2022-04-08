from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.item import Item
from app.models.bid import Bid
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_with_auction(
        self, db: Session, *, obj_in: ItemCreate, owner_id: int, auction_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id, auction_id=auction_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_auction(
        db: Session, auction_id: int, skip: int = 0, limit: int = 100
        ) -> List[Item]:
        return(
            db.query(Item)
            .filter(Item.auction_id == auction_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_item_highest_bid(
        db: Session, item_id: int
    ) -> List[Item]:
        return(
            db.query(Bid)
            .filter(Bid.item_id == item_id)
            .order_by(Bid.price.desc(), Bid.bid_date.asc())
            .first()
        )
    
    def get_item_start_price(
        self, db: Session, *, item_id: int
    ) -> str:
        return (
            db.query(Item)
            .filter(Item.id == item_id)
            .with_entities(Item.start_price)
            .first()
        )






item = CRUDItem(Item)
