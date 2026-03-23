from pydantic import BaseModel


class TeamCreateRequest(BaseModel):
    team_name: str
    user_id: int


class TeamCreateResponse(BaseModel):
    ok: bool
    message: str | None
    team_name: str
