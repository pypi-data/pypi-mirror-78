from dataclasses import dataclass

from .base import BaseImopayObj


@dataclass
class Company(BaseImopayObj):
    email: str
    phone: str
    cnpj: str
    opening_date: str
    social_name: str
    commercial_name: str = ""
    website: str = ""
