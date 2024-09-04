from pydantic import BaseModel, validator


class CropRecommendation(BaseModel):
    """Crop recommendation model"""

    nitrogen: float = 0.0  # Nitrogen level in soil (kg/ha)
    phosporus: float = 0.0  # Phosporus level in soil (kg/ha)
    potassium: float = 0.0  # Potassium level in soil (kg/ha)
    temperature: float = 0.0  # Average temperature (°C)
    humidity: float = 0.0  # Average humidity (%)
    ph: float = 0.0  # Soil pH
    rainfall: float = 0.0  # Average rainfall (mm)

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
