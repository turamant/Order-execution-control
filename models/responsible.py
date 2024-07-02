from pydantic import BaseModel


class Responsible(BaseModel):
    id: int
    name: str
    email: str
    phone: str