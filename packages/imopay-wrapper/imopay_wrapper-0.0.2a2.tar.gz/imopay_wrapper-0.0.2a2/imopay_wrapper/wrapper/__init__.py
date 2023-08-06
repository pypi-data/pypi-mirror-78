from .address import AddressWrapper
from .company import CompanyWrapper
from .person import PersonWrapper
from .transaction import TransactionWrapper


class ImopayWrapper:
    def __init__(self, *args, **kwargs):
        self.address = AddressWrapper(*args, **kwargs)
        self.company = CompanyWrapper(*args, **kwargs)
        self.person = PersonWrapper(*args, **kwargs)
        self.transaction = TransactionWrapper(*args, **kwargs)
