from typing import List, Optional
from pydantic import BaseModel, Field

class District(BaseModel):
    """Model representing a district or district-like city in Belarus."""
    name: str = Field(..., description="Name of the district/city")
    name_ru: str = Field(..., description="Name in Russian")
    name_be: str = Field(..., description="Name in Belarusian")
    region: str = Field(..., description="Region (область) the district belongs to")
    square: float = Field(..., description="Area in square kilometers")
    population: int = Field(..., description="Population count")
    bordering_districts: List[str] = Field(default_factory=list, description="List of bordering districts/cities")
    is_city: bool = Field(default=False, description="Whether this is a city of regional subordination")
    administrative_center: Optional[str] = Field(None, description="Administrative center for districts") 