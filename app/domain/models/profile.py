from typing import Optional

from pydantic import BaseModel


class Profile(BaseModel):
    email: str
    phone_number: Optional[str] = None
    first_name: str
    last_name: str
