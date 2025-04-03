import requests
from pydantic import BaseModel
from requests import Response


class InfuraApiPayload(BaseModel):
    jsonrpc: str
    method: str
    params: list[str]
    id: int


class InfuraApiWalletBalanceResponse(BaseModel):
    jsonrpc: float
    id: int
    result: str


class InfuraClient:
    def __init__(self, base_url: str, headers=None):
        if headers is None:
            headers = {"content-type": "application/json"}

        self.base_url = base_url
        self.headers = headers

    def get_balance(self, payload: InfuraApiPayload) -> InfuraApiWalletBalanceResponse:
        response = self._post(payload=payload)
        return InfuraApiWalletBalanceResponse.model_validate(response.json())

    def _post(self, payload: InfuraApiPayload) -> Response:
        response = requests.post(
            self.base_url, json=payload.model_dump(), headers=self.headers
        )
        response.raise_for_status()
        return response
