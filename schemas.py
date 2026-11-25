from pydantic import BaseModel, ConfigDict, Field


class ServiceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    description: str = Field(min_length=3, max_length=255)


class ServiceResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str

    model_config = ConfigDict(from_attributes=True)