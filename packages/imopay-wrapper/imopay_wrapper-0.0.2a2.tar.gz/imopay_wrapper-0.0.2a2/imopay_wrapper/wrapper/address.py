from .base import BaseImopayWrapper, CreateMixin, UpdateMixin, RetrieveMixin
from ..models.address import Address


class AddressWrapper(BaseImopayWrapper, CreateMixin, UpdateMixin, RetrieveMixin):
    """
    Wrapper para os métodos de address
    """

    @property
    def model(self):
        return Address

    @property
    def action(self):
        return "addresses"

    def create(self, data: dict):
        instance = self.model(**data)
        url = self._construct_url(action=self.action, subaction="create_by_name_and_uf")
        return self._post(url, instance.to_dict())
