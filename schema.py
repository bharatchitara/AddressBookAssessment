from pydantic import BaseModel

class locationData(BaseModel):
    location: str
    latitude: float
    longitude: float
    
    
