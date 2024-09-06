from pydantic import BaseModel, validator


class CropRecommendation(BaseModel):
    """Crop recommendation model"""

    nitrogen: float = 0.0  
    phosporus: float = 0.0  
    potassium: float = 0.0  
    temperature: float = 0.0  
    humidity: float = 0.0  
    ph: float = 0.0  
    rainfall: float = 0.0  

    @validator(
        "nitrogen",
        "phosporus",
        "potassium",
        "temperature",
        "humidity",
        "ph",
        "rainfall",
    )
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v
