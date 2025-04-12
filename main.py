import os
from clients.infura import InfuraClient, InfuraApiPayload


if __name__ == "__main__":
    infura_api_key = os.getenv("INFURA_API_KEY")
    eth_wallet = os.getenv("ETH_WALLET")

    infura_client = InfuraClient(f"https://mainnet.infura.io/v3/{infura_api_key}")
    wallet_payload = InfuraApiPayload(
        jsonrpc="2.0",
        method="eth_getBalance",
        params=[eth_wallet, "latest"],
        id=1,
    )
    qq

    print(infura_client.get_balance(payload=wallet_payload))

    print(infura_client.get_gas_price(payload=gas_payload))

# TODO: Add few methods with models
# TODO: Write tests for those methods (more test cases)
