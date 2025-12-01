from pydantic import BaseModel


class UtilityProviderBase(BaseModel):
    id: int
    name: str
    email: str
