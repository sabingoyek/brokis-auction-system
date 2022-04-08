from typing import List
from app.models.item import Item

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.auction import Auction
from app.schemas.auction import AuctionCreate, AuctionUpdate


class CRUDAuction(CRUDBase[Auction, AuctionCreate, AuctionUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: AuctionCreate, owner_id: int
    ) -> Auction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_status(
        self, db: Session, *, status: str = "active", skip: int = 0, limit: int = 100
    ) -> List[Auction]:
        return (
            db.query(self.model)
            .filter(Auction.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Auction]:
        return (
            db.query(self.model)
            .filter(Auction.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_auction_status(
        self, db: Session, *, auction_id: int
    ) -> str:
        return (
            db.query(self.model)
            .filter(Auction.id == auction_id)
            .with_entities(Auction.status)
            .first()
        )


auction = CRUDAuction(Auction)
