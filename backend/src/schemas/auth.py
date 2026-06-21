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
