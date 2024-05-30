import datetime
from typing import Any
from pydantic import BaseModel, model_validator, ConfigDict


class CustomModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    # @model_serializer(mode="wrap")
    # def serialize_model(self, serializer: SerializerFunctionWrapHandler, info: SerializationInfo):
    #     print("Serialized", info)
    #     data = serializer(self)
    #     if context := info.context:
    #         offset = context.get("_timezone", datetime.timedelta)
    #     else:
    #         offset = datetime.timedelta(seconds=0)
    #     for field_name, field_info in self.model_fields.items():
    #         if field_info.annotation == datetime.datetime:
    #             data[field_name] = convert_datetime_to_local(getattr(self, field_name), offset)
    #         elif field_info.annotation == datetime.timedelta:
    #             data[field_name] = convert_td_to_utcoffset(getattr(self, field_name))
    #     return data

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
