from typing import List
from dataclasses import dataclass, field

from .base import BaseImopayObj


@dataclass
class BaseTransaction(BaseImopayObj):
    payer: str
    receiver: str
    reference_id: str
    amount: int
    description: str


@dataclass
class Configuration(BaseImopayObj):
    value: str
    type: str
    charge_type: str
    days: str


@dataclass
class InvoiceConfigurations(BaseImopayObj):
    fine: Configuration
    interest: Configuration
    discounts: List[Configuration] = field(default=list)

    def __post_init__(self):
        if isinstance(self.fine, dict):
            self.fine = Configuration.from_dict(self.fine)
        if isinstance(self.interest, dict):
            self.interest = Configuration.from_dict(self.interest)
        if self.discounts:
            for i, discount in enumerate(self.discounts):
                if isinstance(discount, dict):
                    self.discounts[i] = Configuration.from_dict(discount)

    def to_dict(self):
        """
        Por causa do typehint 'List' o to_dict original não funciona!

        Ao invés de solucionar isso, mais fácil sobreescrever o método
        no momento.
        """
        data = {}
        if self.fine:
            data["fine"] = self.fine.to_dict()

        if self.interest:
            data["interest"] = self.interest.to_dict()

        if self.discounts:
            data["discounts"] = [discount.to_dict() for discount in self.discounts]
        return data


@dataclass
class Invoice(BaseImopayObj):
    expiration_date: str
    limit_date: str
    configurations: InvoiceConfigurations = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.configurations, dict):
            self.configurations = InvoiceConfigurations.from_dict(self.configurations)


@dataclass
class InvoiceTransaction(BaseTransaction):
    payment_method: Invoice

    def __post_init__(self):
        if isinstance(self.payment_method, dict):
            self.payment_method = Invoice(**self.payment_method)
