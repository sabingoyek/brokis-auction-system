from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Auction])
def read_auctions(
    status: str = "active",
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve all auctions.
    """
    if crud.user.is_superuser(current_user) or status != "draft":
        auctions = crud.auction.get_multi_by_status(db, status=status, skip=skip, limit=limit)
    else:
        auctions = crud.auction.get_multi_by_status(
            db, status=status, skip=skip, limit=limit)
    return auctions


@router.post("/", response_model=schemas.Auction)
def create_auction(
    *,
    db: Session = Depends(deps.get_db),
    auction_in: schemas.AuctionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new auction.
    """
    auction = crud.auction.create_with_owner(
        db=db, obj_in=auction_in, owner_id=current_user.id)
    return auction


@router.put("/{id}", response_model=schemas.Auction)
def update_auction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    auction_in: schemas.AuctionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an auction.
    """
    auction = crud.auction.get(db=db, id=id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not crud.user.is_superuser(current_user) and (auction.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    if auction.status != "draft":
        raise HTTPException(
            status_code=400, detail="This auction is already published.")
    auction = crud.auction.update(db=db, db_obj=auction, obj_in=auction_in)
    return auction


@router.get("/{id}", response_model=schemas.Auction)
def read_auction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get auction by ID.
    """
    auction = crud.auction.get(db=db, id=id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.status == "draft" and not crud.user.is_superuser(current_user) and (auction.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return auction


@router.delete("/{id}")
def delete_auction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an auction.
    """
    auction = crud.auction.get(db=db, id=id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not crud.user.is_superuser(current_user) and (auction.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    if auction.status != "draft":
        raise HTTPException(status_code=400, detail="This auction is already published")
    result = crud.auction.remove(db=db, id=id)
    return result


@router.post("/{id}/status", response_model=schemas.Auction)
def update_auction_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    status: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update auction status.
    """
    auction = crud.auction.get(db=db, id=id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not crud.user.is_superuser(current_user) and (auction.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    if auction.status == "draft" and status != "active":
        raise HTTPException(
            status_code=403, detail="Action forbidden: current status 'draft'")
    if auction.status == "active" and status != "end":
        raise HTTPException(
            status_code=403, detail="Action forbidden: current status 'active'")
    if auction.status == "end":
        raise HTTPException(
            status_code=403, detail="Action forbidden: current status 'end'")
    setattr(auction, "status", status)
    if status == "active":
        if not auction.items:
            raise HTTPException(
                status_code=404, detail="Your auction doesn't have any item yet. So you can't publish it. Create an item and retry.")
        setattr(auction, "start_date", datetime.now())
    if status == "end":
        setattr(auction, "end_date", datetime.now())
    db.add(auction)
    db.commit()
    db.refresh(auction)
    return auction


@router.get("/{id}/status", response_model=object)
def read_auction_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get auction status by ID.
    """
    auction = crud.auction.get(db=db, id=id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.status == "draft" and not crud.user.is_superuser(current_user) and (auction.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return {"status": auction.status}


############## Auction's item ##################################

@router.get("/{auction_id}/items", response_model=List[schemas.Item])
def read_items(
    auction_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve an auction items.
    """
    
    auction = crud.auction.get(db=db, id=auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.status == "draft" and auction.owner_id != current_user.id and not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    # How to do pagination
    return auction.items
    #return crud.item.get_by_auction(db=db,auction_id=auction_id, skip=skip, limit=limit)

@router.post("/{auction_id}/items", response_model=schemas.Item)
def create_item_for_auction(
    auction_id: int,
    item_in: schemas.ItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item for an auction. The auction must exist.
    """
    auction = crud.auction.get(db=db, id=auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.status != "draft":
        raise HTTPException(status_code=403, detail="Action forbidden: Auction already published.")
    """
    if auction.items:
        raise HTTPException(
            status_code=403, detail="Action forbidden: Auction already has an item.")
    """
    if not crud.user.is_superuser(current_user) and auction.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.create_with_auction(db=db, obj_in=item_in, owner_id=current_user.id, auction_id=auction_id)
    return item



