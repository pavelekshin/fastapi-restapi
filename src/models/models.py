import datetime
from typing import Any
from pydantic import BaseModel, model_validator, ConfigDict


class CustomModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Remove microseconds from datetime object"""
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(v, datetime.datetime)
        }

        return {**data, **datetime_fields}
