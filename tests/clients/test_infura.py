from pytest_httpserver import HTTPServer, RequestMatcher

from clients.infura import InfuraClient, InfuraApiPayload


class TestInfuraClient:
    def test_get_balance_returns_expected_result(self, httpserver: HTTPServer) -> None:
        # given
        infura_client = InfuraClient(base_url=httpserver.url_for("get-wallet"))
        payload = InfuraApiPayload(
            jsonrpc="test",
            method="get_walletBalance",
            params=["wallet_id", "1"],
            id=1
        )
        expected_response = {
                "jsonrpc": "0.1",
                "id": 1,
                "result": "test",
        }
        httpserver.expect_request("/get-wallet", method="POST").respond_with_json(
            expected_response
        )

        # when
        client_response = infura_client.get_balance(payload=payload)

        # then
        assert client_response.id == expected_response["id"]
        assert client_response.result == expected_response["result"]
        assert client_response.jsonrpc == expected_response["jsonrpc"]

        httpserver.assert_request_made(matcher=RequestMatcher(uri="/get-wallet", method="POST", json=payload.model_dump()))
