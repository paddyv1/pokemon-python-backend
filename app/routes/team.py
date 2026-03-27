from datetime import timedelta
from app.pydanticmodels.auth import TokenResponse
from fastapi import APIRouter
from app.database.session import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.pydanticmodels.user import UserRead
from app.services.team.teamservice import (
    create_team_for_user,
    delete_team_for_user,
    get_all_teams_for_a_user_func,
    get_team_for_user,
    update_team_for_user,
)

from app.services.team.teammodels import TeamCreateRequest
from app.services.authservice import get_current_active_user

from app.services.team.teammodels import (
    TeamCreateResponse,
    TeamDeleteResponse,
    TeamUpdateResponse,
)

router = APIRouter(prefix="/team")


##create team
@router.post("")
async def create_team(
    team_data: TeamCreateRequest,
    user: UserRead = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    await create_team_for_user(userId=user.user_id, teamName=team_data.team_name, db=db)
    return {"message": "good"}


##retrieve all teams for a user
@router.get("/all")
async def get_all_teams_for_a_user(user: UserRead = Depends(get_current_active_user), db: Session = Depends(get_db)):
    result = await get_all_teams_for_a_user_func(user.user_id, db)
    return result


##retrieve a specific team by id
@router.get("/{team_id}")
async def get_team_for_user_route(team_id: int, user: UserRead = Depends(get_current_active_user), db: Session = Depends(get_db)):
    team = await get_team_for_user(team_id, db)
    return {"message": f"returned {team.team_name} and {team.slots}"}


##update team by id
@router.put("/{team_id}")
async def update_team(
    team_id: int,
    team_name: str,
    user: UserRead = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> TeamUpdateResponse:
    resp = await update_team_for_user(teamId=team_id, teamName=team_name, db=db)
    return resp


##delete a team by id
@router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    user: UserRead = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> TeamDeleteResponse:
    resp = await delete_team_for_user(team_id, db)
    return TeamDeleteResponse(ok=resp.ok, message=resp.message)
