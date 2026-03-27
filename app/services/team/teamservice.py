from sqlalchemy.orm import Session

from app.services.team.teammodels import (
    TeamCreateResponse,
    TeamDeleteResponse,
    TeamUpdateResponse,
)
from app.models import Team as TeamModel


async def create_team_for_user(
    userId: int,
    teamName: str,
    db: Session,
) -> TeamCreateResponse:
    db.add(TeamModel(user_id=userId, team_name=teamName))
    db.commit()
    return TeamCreateResponse(ok=True, team_name=teamName, message="")


async def delete_team_for_user(teamId: int, db: Session) -> TeamDeleteResponse:
    team = db.get(TeamModel, teamId)
    if team is None:
        return TeamDeleteResponse(ok=True, message="Team has already been deleetd")
    db.delete(team)
    db.commit()
    return TeamDeleteResponse(
        ok=True, message=f"Team {team.team_name} has been deleted"
    )


async def update_team_for_user(teamId: int, teamName: str, db: Session) -> TeamUpdateResponse:
    team = db.get(TeamModel, teamId)
    if team is None:
        return TeamUpdateResponse(ok=False, message="This team does not exist in the database")
    team.team_name = teamName
    db.commit()
    return TeamUpdateResponse(ok=True, message="Team has been updated")
