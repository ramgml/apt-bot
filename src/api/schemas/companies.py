from pydantic import BaseModel


class UtilityCompanyBase(BaseModel):
    id: int
    name: str
    email: str
