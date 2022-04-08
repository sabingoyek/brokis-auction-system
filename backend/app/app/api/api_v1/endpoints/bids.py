from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Bid])
def read_bids(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve bids.
    """
    if crud.user.is_superuser(current_user):
        bids = crud.bid.get_multi(db, skip=skip, limit=limit)
    else:
        bids = crud.bid.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return bids


@router.post("/", response_model=schemas.Bid)
def create_bid(
    *,
    db: Session = Depends(deps.get_db),
    bid_in: schemas.BidCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bid.
    """
    bid = crud.bid.create_with_owner(db=db, obj_in=bid_in, owner_id=current_user.id)
    return bid

"""
@router.put("/{id}", response_model=schemas.Bid)
def update_bid(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    bid_in: schemas.BidUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    
    #Update an bid.
    
    bid = crud.bid.get(db=db, id=id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if not crud.user.is_superuser(current_user) and (bid.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bid = crud.bid.update(db=db, db_obj=bid, obj_in=bid_in)
    return bid
"""

@router.get("/{id}", response_model=schemas.Bid)
def read_bid(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get bid by ID.
    """
    bid = crud.bid.get(db=db, id=id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if not crud.user.is_superuser(current_user) and (bid.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return bid


@router.delete("/{id}", response_model=schemas.Bid)
def delete_bid(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an bid.
    """
    bid = crud.bid.get(db=db, id=id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if not crud.user.is_superuser(current_user) and (bid.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    bid = crud.bid.remove(db=db, id=id)
    return bid
