from __future__ import annotations

from pydantic import BaseModel, field_validator, ValidationError

from errors import HttpError


class BaseAdvertisement(BaseModel):
    title: str
    description: str
    owner: str

    @field_validator("description")
    @classmethod
    def validate_description_length(cls, value):
        if len(value) < 15:
            raise ValueError("Description must be at least 15 characters")
        return value

class CreateAdvertisement(BaseAdvertisement):
    pass

class UpdateAdvertisement(BaseAdvertisement):
    title: str | None = None
    description: str | None = None
    owner: str | None = None


def validate_json(
        json_data: dict,
        schema_class: type[CreateAdvertisement] | type[UpdateAdvertisement]
):
    try:
        schema_obj = schema_class(**json_data)
        return schema_obj.model_dump(exclude_unset=True)
    except ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)