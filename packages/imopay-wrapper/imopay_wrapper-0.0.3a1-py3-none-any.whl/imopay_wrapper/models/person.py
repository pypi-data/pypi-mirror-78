from dataclasses import dataclass

from .base import BaseImopayObj


@dataclass
class Person(BaseImopayObj):
    email: str
    phone: str
    first_name: str
    last_name: str
    cpf: str
    birthdate: str
    mobile_phone: str = ""
    website: str = ""
