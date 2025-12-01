from pydantic import BaseModel
from typing import Optional

from api.schemas.companies import UtilityProviderBase


class AccountBase(BaseModel):
    number: str


class AccountResponse(AccountBase):
    id: int
    utility_provider: Optional[UtilityProviderBase]

    class Config:
        from_attributes = True
