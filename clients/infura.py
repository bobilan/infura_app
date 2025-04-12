import requests
from pydantic import BaseModel
from requests import Response


class InfuraApiPayload(BaseModel):
    jsonrpc: str
    method: str
    params: list[str]
    id: int


class InfuraApiResponse(BaseModel):
    jsonrpc: float
    id: int
    result: str


class InfuraClient:
    def __init__(self, base_url: str, headers=None):
        if headers is None:
            headers = {"content-type": "application/json"}

        self.base_url = base_url
        self.headers = headers

    def get_balance(self, payload: InfuraApiPayload) -> float:
        response = self._post(payload=payload)
        validated_response = InfuraApiResponse.model_validate(response.json())

        return self.hexadecimal_wei_to_eth(validated_response.result)

    def _post(self, payload: InfuraApiPayload) -> Response:
        response = requests.post(
            self.base_url, json=payload.model_dump(), headers=self.headers
        )
        response.raise_for_status()
        return response

    @staticmethod
    def hexadecimal_wei_to_eth(hex_balance: str) -> float:
        try:
            return round(int(hex_balance, 16) / 10**18, 5)
        except ValueError as e:
            print("Not a valid hexadecimal balance:", e)

    @staticmethod
    def hexadecimal_wei_to_gwei(hex_balance: str) -> float:
        try:
            return round(int(hex_balance, 16) / 10**9, 3)
        except ValueError as e:
            print("Not a valid hexadecimal balance:", e)

    def get_gas_price(self, payload: InfuraApiPayload):
        response = self._post(payload=payload)
        validate_response = InfuraApiResponse.model_validate(response.json())
        return self.hexadecimal_wei_to_gwei(validate_response.result)
