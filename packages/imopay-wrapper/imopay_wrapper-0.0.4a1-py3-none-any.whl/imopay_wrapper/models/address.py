from dataclasses import dataclass

from .base import BaseImopayObj


@dataclass
class Address(BaseImopayObj):
    owner: str
    city: str
    uf: str
    zip_code: str
    street: str
    number: str
    neighborhood: str
    complement: str = ""
