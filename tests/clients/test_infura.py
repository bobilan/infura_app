import requests
import pytest
from pytest_httpserver import HTTPServer, RequestMatcher

from clients.infura import InfuraClient, InfuraApiPayload


class TestInfuraClient:

    def test_get_balance_returns_expected_result(self, httpserver: HTTPServer) -> None:
        # given
        infura_client = InfuraClient(base_url=httpserver.url_for("get-wallet"))
        payload = InfuraApiPayload(
            jsonrpc="test", method="get_walletBalance", params=["wallet_id", "1"], id=1
        )
        expected_response = {
            "jsonrpc": "0.1",
            "id": 1,
            "result": "0xDE0B6B3A7640000",
        }
        httpserver.expect_request("/get-wallet", method="POST").respond_with_json(
            expected_response
        )

        # when
        client_response = infura_client.get_balance(payload=payload)

        # then
        assert client_response == 1

        httpserver.assert_request_made(
            matcher=RequestMatcher(
                uri="/get-wallet", method="POST", json=payload.model_dump()
            )
        )

    def test_get_balance_value_error_not_hexadecimal(self, httpserver: HTTPServer):
        # given
        infura_client = InfuraClient(base_url=httpserver.url_for("/get-balance"))
        payload = InfuraApiPayload(
            jsonrpc="test", method="get_walletBalance", params=["wallet_id", "1"], id=1
        )
        expected_response = {
            "jsonrpc": "0.1",
            "id": 1,
            "result": "000sdf",
        }

        httpserver.expect_request("/get-balance", method="POST").respond_with_json(
            expected_response
        )
        # when
        response = infura_client.get_balance(payload=payload)
        # then
        assert response is None

    def test_hexadecimal_wei_to_gwei_correct_hexadecimal(self):
        # given
        infura_client = InfuraClient(base_url="/")
        hex_balance = "0x2540BE400"
        # when
        result = infura_client.convert_to_gwei(hex_balance)
        # then
        assert result == 10.0

    def test_hexadecimal_wei_to_gwei_zero_value(self):
        # given
        infura_client = InfuraClient(base_url="/")
        hex_balance = "0x0"
        # when
        result = infura_client.convert_to_gwei(hex_balance)
        # then
        assert result == 0.0

    def test_get_gas_price_success(self, httpserver: HTTPServer):
        # given
        infura_app = InfuraClient(base_url=httpserver.url_for("/eth-gas-price"))
        payload = InfuraApiPayload(
            jsonrpc="2.0",
            method="eth_gasPrice",
            params=[],
            id=1,
        )
        response_data = {
            "jsonrpc": "0.1",
            "id": 1,
            "result": "0x12A05F200",
        }
        httpserver.expect_request("/eth-gas-price", method="POST").respond_with_json(
            response_data
        )
        # when
        result = infura_app.get_gas_price(payload=payload)

        # then
        assert result == 5.0

        httpserver.assert_request_made(
            matcher=RequestMatcher(
                uri="/eth-gas-price", method="POST", json=payload.model_dump()
            )
        )

    def test_get_gas_price_404(self, httpserver: HTTPServer):
        # given
        infura_app = InfuraClient(base_url=httpserver.url_for("/eth-gas-price"))
        payload = InfuraApiPayload(
            jsonrpc="2.0",
            method="eth_gasPrice",
            params=[],
            id=1,
        )
        response_data = {
            "jsonrpc": "0.1",
            "id": 1,
            "result": "unsuccessful",
        }
        httpserver.expect_request("/eth-gas-price", method="POST").respond_with_json(
            response_data, status=404
        )
        # when
        with pytest.raises(requests.exceptions.HTTPError):
            infura_app.get_gas_price(payload=payload)

            httpserver.assert_request_made(
                matcher=RequestMatcher(
                    uri="/eth-gas-price", method="POST", json=payload.model_dump()
                )
            )
            # TODO: how to handle unsuccessful codes
