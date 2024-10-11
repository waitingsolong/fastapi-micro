from pydantic import BaseModel

class Reaction(BaseModel):
    emoji: str 
    count: int
    