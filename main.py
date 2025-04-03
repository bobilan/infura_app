from clients.infura import InfuraClient, InfuraApiPayload


if __name__ == "__main__":
    infura_client = InfuraClient(
        "https://mainnet.infura.io/v3/XXX"
    )
    wallet_payload = InfuraApiPayload(
        jsonrpc="2.0",
        method="eth_getBalance",
        params=["XXXX", "latest"],
        id=1,
    )

    print(infura_client.get_balance(payload=wallet_payload))


# TODO: Add few methods with models
# TODO: Write tests for those methods (more test cases)
