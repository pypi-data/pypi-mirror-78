import requests

from ..constants import IMOPAY_ENV, IMOPAY_API_KEY
from ..utils import get_logger


logger = get_logger("requests")


class RequestsWrapper:
    """
    wrapper da lib requests

    Attributes:
        __base_url: Url base para construir os requests
    """

    def __init__(self, base_url):
        self.__base_url = base_url

    @staticmethod
    def __process_response(response) -> requests.Response:
        """
        Processa a resposta.

        Adiciona o :attr:`.data` carregado do :meth:`requests.Response.json`.

        Adiciona o :attr:`.instance` ou :attr:`.instances` baseado no resource.

        .. note::
            Apenas adiciona :attr:`.instance` ou :attr:`.instances` se não tiver o dado 'deleted' no :attr:`.data`  # noqa
            que é retornado em todas as respostas de deleção (200 ok) e se tiver o dado `resource` no :attr:`.data`  # noqa

        Adiciona :attr:`.error` na resposta se tiver ocorrido erros

        Args:
            response (:class:`requests.Response`): resposta a ser processada

        Raises:
            HttpError: quando a resposta não foi ok (200 <= status <= 299)!

        Returns:
            'objeto' (:class:`.requests.Response`) de resposta http
        """
        response.data = response.json()
        response.raise_for_status()
        return response

    def _construct_url(
        self,
        action=None,
        identifier=None,
        subaction=None,
        search=None,
        sub_action_before_identifier=False,
    ):
        # noinspection PyProtectedMember
        """
        Constrói a url para o request.

        Args:
            action: nome do resource
            identifier: identificador de detalhe (ID)
            search: query com url args para serem buscados
            sub_action_before_identifier: flag para inverter a posição do identifier e subaction
            subaction: subação do resource

        Examples:
            >>> rw = RequestsWrapper()
            >>> rw._construct_url(action='acao', identifier='1', subaction='subacao', search='algum_atributo=1')  # noqa:
            'rw.__base_url/acao/1/subacao/?algum_atributo=1'

        Returns:
            url completa para o request
        """
        url = f"{self._base_url}/"
        if action:
            url += f"{action}/"

        if sub_action_before_identifier:
            if subaction:
                url += f"{subaction}/"
            if identifier:
                url += f"{identifier}/"
        else:
            if identifier:
                url += f"{identifier}/"
            if subaction:
                url += f"{subaction}/"

        if search:
            if isinstance(search, dict):
                url += "?"
                for key, value in search.items():
                    url += f"{key}={value}"
            else:
                url += f"?{search}"
        return url

    @property
    def _auth(self):
        """
        Propriedade de autenticação

        Raises:
            NotImplementedError: É um método abstrato!
        """
        raise NotImplementedError("Must implement auth function!")

    @property
    def _base_url(self):
        return self.__base_url

    @property
    def _headers(self):
        return {"Authorization": self._auth}

    def _delete(self, url) -> requests.Response:
        """
        http delete

        Args:
            url: url de requisição

        Returns:
            (:class:`.requests.Response`)
        """
        response = requests.delete(url, headers=self._headers)
        response = self.__process_response(response)
        return response

    def _get(self, url) -> requests.Response:
        """
        http get

        Args:
            url: url de requisição

        Returns:
            (:class:`.requests.Response`)
        """
        response = requests.get(url, headers=self._headers)
        response = self.__process_response(response)
        return response

    def _post(self, url, data) -> requests.Response:
        """
        http post

        Args:
            url: url de requisição
            data (dict): dados da requisição

        Returns:
            (:class:`.requests.Response`)
        """
        response = requests.post(url, json=data, headers=self._headers)
        response = self.__process_response(response)
        return response

    def _put(self, url, data) -> requests.Response:
        """
        http put

        Args:
            url: url de requisição
            data (dict): dados da requisição

        Returns:
            (:class:`.requests.Response`)
        """
        response = requests.put(url, json=data, headers=self._headers)
        response = self.__process_response(response)
        return response

    def _patch(self, url, data) -> requests.Response:
        response = requests.patch(url, json=data, headers=self._headers)
        response = self.__process_response(response)
        return response


class BaseImopayWrapper(RequestsWrapper):
    """
    wrapper do ImopayAPI

    Attributes:
        __imopay_env: ambiente do Imopay
        __imopay_api_key: chave de autenticação do Imopay
    """

    BASE_SCHEMA = "http://"
    BASE_URL = "imopay.com.br"

    def __init__(self, imopay_env=None, imopay_api_key=None):
        if imopay_env is None:
            imopay_env = IMOPAY_ENV

        if imopay_api_key is None:
            imopay_api_key = IMOPAY_API_KEY

        self.__imopay_env = imopay_env
        self.__imopay_api_key = imopay_api_key

        if self.__imopay_api_key == "" or self.__imopay_env == "":
            raise ValueError("configure as variáveis corretamente!")

        super().__init__(
            base_url=f"{self.BASE_SCHEMA}{self.__imopay_env}.{self.BASE_URL}"
        )

    @property
    def _auth(self):
        """
        Propriedade de autenticação.

        Returns:
            string de autenticação para o header
            Authorization com :attr:`.IMOAY_API_KEY`
        """
        return f"Api-Key {self.__imopay_api_key}"

    @property
    def action(self):
        raise NotImplementedError()

    @property
    def model(self):
        raise NotImplementedError()


class CreateMixin:
    def create(self, data: dict):
        instance = self.model(**data)
        url = self._construct_url(action=self.action)
        return self._post(url, instance.to_dict())


class UpdateMixin:
    def update(self, identifier: str, data: dict):
        instance = self.model.from_dict(data)
        url = self._construct_url(action=self.action, identifier=identifier)
        return self._patch(url, instance.to_dict())


class RetrieveMixin:
    def retrieve(self, identifier: str):
        url = self._construct_url(action=self.action, identifier=identifier)
        return self._get(url)
