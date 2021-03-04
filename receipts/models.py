from pydantic import BaseModel, HttpUrl
from typing import List


class Step(BaseModel):
    number: int
    title: str
    steps: List[str]
    image: HttpUrl


class Recipe(BaseModel):
    name: str
    external_id: str  # (max_length=1024, blank=True, unique=True)
    ingredients: List[str]
    tools: List[str]
    steps: List[Step]
