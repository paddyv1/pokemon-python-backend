from sqlalchemy.orm import Session

from teammodels import TeamCreateResponse
from models import Team as TeamModel


async def create_team(
    userId: int,
    teamName: str,
    db: Session,
) -> TeamCreateResponse:
    db.add(TeamModel(user_id=userId, team_name=teamName))
    db.commit()
