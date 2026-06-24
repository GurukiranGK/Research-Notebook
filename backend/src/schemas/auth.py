from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int | None = None
    refresh_expires_in: int | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    id_token: str | None = None
    not_before_policy: int | None = Field(default=None, alias="not-before-policy")
    session_state: str | None = None
    scope: str | None = None


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=8, max_length=128)
    displayName: str | None = Field(default=None, max_length=100)


class RegisterResponse(BaseModel):
    id: str
    username: str
    email: str
    displayName: str | None = None