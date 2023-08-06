from dataclasses import dataclass


@dataclass
class BaseImopayObj:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_fields(cls):
        return cls.__dataclass_fields__

    def to_dict(self):
        data = {}
        for field_name, field in self.get_fields().items():
            value = getattr(self, field_name)

            if self.is_empty_value(value):
                continue

            if isinstance(value, BaseImopayObj):
                data[field_name] = value.to_dict()
            else:
                data[field_name] = field.type(value)
        return data

    @classmethod
    def from_dict(cls, data: dict):

        missing_fields = {
            field_name
            for field_name in cls.get_fields().keys()
            if field_name not in data.keys()
        }

        for missing_field in missing_fields:
            data[missing_field] = None

        return cls(**data)

    @staticmethod
    def is_empty_value(value):
        return value == "" or value is None
