
from typing import List, Optional


from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from ..schemas import travely_schema
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..oauth2 import get_current_user
from .user import add_recent_search
import mpu


router = APIRouter(tags=["Travelies"], prefix="/travelies",)


# HELPER FUNCTIONS
# Get travelies bases on recent searches
def get_results_per_recent_searches(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    recent_searches = db.query(models.RecentSearchModel).filter(
        models.RecentSearchModel.user_id == current_user.user_id).limit(10).all()

    # return only the names in a list
    return [search.name.lower() for search in recent_searches]


# GET TRAVELIES
@router.get("/", response_model=List[travely_schema.TravelyOut], status_code=status.HTTP_200_OK)
async def get_travelies(background_tasks: BackgroundTasks, current_user=Depends(get_current_user), db: Session = Depends(get_db), limit: int = 50, skip: int = 0, ):

    recent_searches = get_results_per_recent_searches(db, current_user)

    # Check if there are recent searches
    if len(recent_searches) > 10:

        return db.query(models.TravelyModel).filter(
            models.TravelyModel.name.lower().in_(recent_searches)).offset(skip).limit(limit).all()
    else:
        return db.query(models.TravelyModel).offset(skip).limit(limit).all()

# Get Searches


@router.get("/search", response_model=List[travely_schema.TravelyOut], status_code=status.HTTP_200_OK)
async def get_travelies(search: str, background_tasks: BackgroundTasks, current_user=Depends(get_current_user), db: Session = Depends(get_db), limit: int = 50, skip: int = 0,
                        # filters: Optional[str] = Query(...)
                        ):
    if search:
        background_tasks.add_task(add_recent_search)

    # if filters:
    #     newFilter = json.loads(filters)
    #     ll_filters = parse_obj_as(List[travely_schema.QueryFilter], newFilter)

    #     # Execute the filters
    #     for filter in ll_filters:
    #         db = db.query(models.TravelyModel).filter(
    #             filter.get_sqlalchemy_filter(models.TravelyModel))

    #     return db.query(models.TravelyModel).filter().offset(skip).limit(limit).all()

    return db.query(models.TravelyModel).filter(models.TravelyModel.name.lower().contains(search.lower())).offset(skip).limit(limit).all()

# GET NEARBY TRAVELIES


@router.get("/nearby", response_model=List[travely_schema.TravelyOut], status_code=status.HTTP_200_OK)
def get_results_per_location(lat: float, long: float, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    # Get all travelies ON 100KM RADIUS
    travelies = db.query(models.TravelyModel).filter(
        mpu.haversine_distance((lat, long), (models.TravelyModel.latitude, models.TravelyModel.longitude)) < 100).all()
    if len(travelies) > 10:
        return travelies
    alternatives = db.query(models.TravelyModel).filter(
        mpu.haversine_distance((lat, long), (models.TravelyModel.latitude, models.TravelyModel.longitude)) < 1000).all()
    return alternatives if len(alternatives) > 10 else db.query(models.TravelyModel).all()


# GET A SPECIFIC TRAVELY

@router.get("/{travely_id}", response_model=travely_schema.TravelyDetails, status_code=status.HTTP_200_OK)
async def get_travely(travely_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely = db.query(models.TravelyModel).filter(
        models.TravelyModel.id == travely_id).first()
    if travely is None:
        raise HTTPException(status_code=404, detail="Travely not found")
    return travely


# CREATE A TRAVELY

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=travely_schema.TravelyOut)
async def create_travely(travely: travely_schema.TravelyCreate, status_code=status.HTTP_201_CREATED, current_user=Depends(get_current_user), db: Session = Depends(get_db)):

    new_travely = models.TravelyModel(
        owner_id=current_user.user_id, **travely.dict())
    db.add(new_travely)
    db.commit()
    db.refresh(new_travely)
    return new_travely


# CREATE A RULE FOR A TRAVELY
@router.post("/{travely_id}/rules", status_code=status.HTTP_201_CREATED, response_model=travely_schema.TravelyOut)
async def create_rule(travely_id: str, rule: travely_schema.RulesBase, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely = db.query(models.RulesModel).filter(
        models.RulesModel.travely_id == travely_id)
    if travely.first() is None:
        raise HTTPException(status_code=404, detail="Travely not found")
    new_rule = models.RulesModel(**rule.dict())
    db.add(new_rule)
    db.commit()

    return travely.first()

# DELETE A RULE FOR A TRAVELY


@router.delete("/{travely_id}/rules", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(travely_id: str, rule_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely = db.query(models.RulesModel).filter(
        models.RulesModel.travely_id == travely_id)
    if travely.first() is None:
        raise HTTPException(status_code=404, detail="Travely not found")
    rule = db.query(models.RulesModel).filter(
        models.RulesModel.id == rule_id).delete(synchronize_session=False)
    db.commit()
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")


# DELETE A TRAVELY
@router.delete("/{travely_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_travely(travely_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely = db.query(models.TravelyModel).filter(
        models.TravelyModel.id == travely_id).delete(synchronize_session=False)
    db.commit()
    if travely is None:
        raise HTTPException(status_code=404, detail="Travely not found")


# UPDATE A RULE FOR A TRAVELY


@router.put("/{travely_id}/rules", status_code=status.HTTP_200_OK, response_model=travely_schema.TravelyOut)
async def update_rule(travely_id: str, rule: travely_schema.RulesBase, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely = db.query(models.RulesModel).filter(
        models.RulesModel.travely_id == travely_id)
    if travely.first() is None:
        raise HTTPException(status_code=404, detail="Travely not found")
    rule_to_update = db.query(models.RulesModel).filter(
        models.RulesModel.id == rule.id)
    if rule_to_update.first() is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    rule_to_update.update(rule.dict())
    db.commit()
    db.refresh(rule_to_update.first())
    return rule_to_update.first()

# UPDATE A TRAVELY


@router.put("/{travely_id}", status_code=status.HTTP_200_OK, response_model=travely_schema.TravelyOut)
async def update_travely(travely_id: str, travely: travely_schema.TravelyCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    travely_to_update = db.query(models.TravelyModel).filter(
        models.TravelyModel.id == travely_id)
    if travely_to_update.first() is None:
        raise HTTPException(status_code=404, detail="Travely not found")
    travely_to_update.update(travely.dict())
    db.commit()
    db.refresh(travely_to_update.first())
    return travely_to_update.first()
