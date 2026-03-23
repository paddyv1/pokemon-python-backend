from sqlalchemy.orm import Session

from app.services.team.teammodels import TeamCreateResponse
from app.models import Team as TeamModel


async def create_team_for_user(
    userId: int,
    teamName: str,
    db: Session,
) -> TeamCreateResponse:
    db.add(TeamModel(user_id=userId, team_name=teamName))
    db.commit()
    return TeamCreateResponse(ok=True, team_name=teamName, message="")
