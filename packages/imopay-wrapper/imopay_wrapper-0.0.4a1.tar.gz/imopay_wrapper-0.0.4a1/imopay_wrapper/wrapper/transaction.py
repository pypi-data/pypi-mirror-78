from .base import BaseImopayWrapper, RetrieveMixin
from ..models.transaction import InvoiceTransaction


class TransactionWrapper(BaseImopayWrapper, RetrieveMixin):
    """
    Wrapper para os métodos de transaction
    """

    @property
    def action(self):
        return "transactions"

    def create_invoice(self, data: dict):
        instance = InvoiceTransaction(**data)
        url = self._construct_url(
            action=self.action, subaction="create_invoice_transaction"
        )
        return self._post(url, instance.to_dict())
