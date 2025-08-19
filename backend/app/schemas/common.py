from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 50
    offset: int = 0



