import os

from web3 import Web3

from clients.infura import InfuraClient, InfuraApiPayload, StreamingInfuraClient


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
    gas_payload = InfuraApiPayload(
        jsonrpc="2.0",
        method="eth_gasPrice",
        params=[],
        id=1,
    )

    print(infura_client.get_balance(payload=wallet_payload))
    print(infura_client.get_gas_price(payload=gas_payload))

    web3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{infura_api_key}"))

    subscription_payload = InfuraApiPayload(
        jsonrpc="2.0",
        method="eth_subscribe",
        params=["newPendingTransactions"],
        id=1,
    )

    streaming_client = StreamingInfuraClient(
        infura_ws_url=f"wss://mainnet.infura.io/ws/v3/{infura_api_key}",
        web3_client=web3,
    )
    streaming_client.get_event(subscription_payload)


# TODO: with web3 read data from stream.
# https://docs.metamask.io/services/tutorials/ethereum/subscribe-to-pending-transactions/
# TODO: Add tests (not for streaming client)
# TODO: save to db: Postgres,
# TODO: how to use alembic, sqlalchemy
