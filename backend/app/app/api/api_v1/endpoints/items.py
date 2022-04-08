from typing import Any, List
from urllib import response

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items

""""
@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    ""
    Create new item.
    ""
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item
"""

@router.put("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item_status = crud.auction.get_auction_status(db=db,auction_id=item.auction_id).status
    if item_status != "draft":
        raise HTTPException(status_code=403, detail="Action forbidden: item already published.")
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item_status = crud.auction.get_auction_status(db=db, auction_id=item.auction_id).status
    if item_status != "draft":
        raise HTTPException(
            status_code=403, detail="Action forbidden: item already published.")
    item = crud.item.remove(db=db, id=id)
    return item


@router.get("/items/{id}/winner/", response_model=int)
def read_item_winner(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    ) -> Any:
    """
    Read the winner of an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_status = crud.auction.get_auction_status(db=db, auction_id=item.auction_id).status
    if item_status != "end":
        raise HTTPException(
            status_code=403, detail="Auction that this article belong to is not over yet.")
    item_highest_bid = crud.item.get_item_highest_bid(db=db, item_id=id)
    return item_highest_bid


@router.get("/items/{id}/start_price/", response_model=object)
def read_item_price(id: int, db: Session = Depends(deps.get_db)):
    """
    Read the price of an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_status = crud.auction.get_auction_status(db=db, auction_id=item.auction_id).status
    if item_status == "draft":
        raise HTTPException(
            status_code=403, detail="Auction that this article belong to is not published yet.")
    item_price = crud.item.get_item_start_price(db=db, item_id=id)
    return item_price


############ Item's Bid ##############

@router.get("/{item_id}/bids", response_model=List[schemas.Bid])
def read_bids(
    item_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve an item bids.
    """

    item = crud.item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_status = crud.auction.get_auction_status(db=db, auction_id=item.auction_id).status
    if item_status == "draft":
        raise HTTPException(
            status_code=403, detail="Action forbidden: Auction that this item belong to is not already published.")
    # How to do pagination
    return item.bids
    #return crud.item.get_by_auction(db=db,auction_id=auction_id, skip=skip, limit=limit)


@router.post("/{item_id}/bids", response_model=schemas.Bid)
def create_bid_for_item(
    item_id: int,
    bid_in: schemas.BidCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bid for an item. The item must exist.
    """
    item = crud.item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_status = crud.auction.get_auction_status(db=db, auction_id=item.auction_id).status
    if item_status == "draft":
        raise HTTPException(
            status_code=403, detail="Action forbidden: Auction that this item belong to is not already published.")
    elif item_status == "end":
        raise HTTPException(
            status_code=403, detail="Action forbidden: Auction closed.")

    bid = crud.bid.create_with_item(
        db=db, obj_in=bid_in, owner_id=current_user.id, item_id=item_id)
    return bid
