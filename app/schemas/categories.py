from pydantic import BaseModel, field_validator, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        name = name.strip()
        name = name.capitalize()

        if not name:
            raise ValueError("Category name cannot be empty")

        return name


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError("Category name cannot be empty")

        return name


