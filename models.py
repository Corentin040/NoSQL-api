from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class ViewerInfo(BaseModel):
    fresh: Optional[int] = None

class CriticInfo(BaseModel):
    rotten: Optional[int] = None


class Movie(BaseModel):
    id: str = Field(alias="_id")
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    cast: Optional[List[str]] = None
    title: str
    languages: Optional[List[str]] = None
    directors: Optional[List[str]] = None
    year: Optional[int] = None
    

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "573a1390f29313caabcd42e8",
                "plot": "A group of bandits stage a brazen train hold-up...",
                "genres": ["Short", "Western"],
                "cast": ["A.C. Abadie", "Gilbert M. 'Broncho Billy' Anderson", "George Barnes", "Justus D. Barnes"],
                "title": "The Great Train Robbery",
                "languages": ["English"],
                "directors": ["Edwin S. Porter"],
                "year": 1903,
            }
        }

class MovieUpdate(BaseModel):
    plot: Optional[str]
    genres: Optional[List[str]]
    cast: Optional[List[str]]
    languages: Optional[List[str]]
    directors: Optional[List[str]]
    year: Optional[int]
    class Config:
        schema_extra = {
            "example": {
                "plot": "A new plot description...",
                "genres": ["Drama"],
                "runtime": 120
            }
        }
