from pydantic import BaseModel

from api.schemas.companies import UtilityCompanyBase


class AccountBase(BaseModel):
    number: str


class AccountResponse(AccountBase):
    id: int
    utility_company: UtilityCompanyBase

    class Config:
        from_attributes = True
