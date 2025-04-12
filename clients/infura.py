import json
import ssl

import requests
from pydantic import BaseModel
from requests import Response
from web3 import Web3
from websocket import create_connection


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

        return self.convert_to_eth(validated_response.result)

    def _post(self, payload: InfuraApiPayload) -> Response:
        response = requests.post(
            self.base_url, json=payload.model_dump(), headers=self.headers
        )
        response.raise_for_status()
        return response

    @staticmethod
    def convert_to_eth(hex_balance: str) -> float:
        try:
            return round(int(hex_balance, 16) / 10**18, 5)
        except ValueError as e:
            print("Not a valid hexadecimal balance:", e)

    @staticmethod
    def convert_to_gwei(hex_balance: str) -> float:
        try:
            return round(int(hex_balance, 16) / 10**9, 3)
        except ValueError as e:
            print("Not a valid hexadecimal balance:", e)

    def get_gas_price(self, payload: InfuraApiPayload):
        response = self._post(payload=payload)
        validate_response = InfuraApiResponse.model_validate(response.json())
        return self.convert_to_gwei(validate_response.result)


class StreamingInfuraClient:
    def __init__(self, web3_client: Web3, infura_ws_url: str):
        self.web3_client = web3_client
        self.infura_ws_url = infura_ws_url

    def get_event(self, subscription_payload: InfuraApiPayload):
        if self.web3_client.is_connected():
            print("Successfully connected to the Ethereum network via Infura!")
        else:
            print("Failed to connect to Infura.")
            exit(1)

        ssl_opts = {"cert_reqs": ssl.CERT_NONE, "check_hostname": False}

        ws = create_connection(self.infura_ws_url, sslopt=ssl_opts)
        ws.send(subscription_payload.model_dump_json())
        subscription_response = ws.recv()
        print(subscription_response)

        while True:
            try:
                message = ws.recv()
                response = json.loads(message)
                tx_hash = response["params"]["result"]
                print(tx_hash)

            except Exception as e:
                print(f"An error occurred: {e}")
