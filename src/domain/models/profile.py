from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Profile(BaseModel):
    id: UUID
    email: str
    phone_number: Optional[str]
    first_name: str
    last_name: str


    class Config:
        orm_mode = True