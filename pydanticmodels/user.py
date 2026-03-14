from pydantic import BaseModel, ConfigDict, Field

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)