#!/usr/bin/env python3

import requests
import json

from ..config import bitcoin
from ...utils.exceptions import AddressError, APIError
from .utils import is_address


# Request headers
headers = dict()
headers.setdefault("Content-Type", "application/json")

# Bitcoin configuration
bitcoin = bitcoin()


# Get balance by address
def get_balance(address, network="testnet", timeout=bitcoin["timeout"]):
    """
    Get Bitcoin balance.

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: int -- Bitcoin balance.

    >>> from swap.providers.bitcoin.rpc import get_balance
    >>> get_balance(bitcoin_address, "mainnet")
    25800000
    """

    if not is_address(address=address, network=network):
        raise AddressError("invalid %s %s address" % (network, address))
    url = str(bitcoin[network]["blockcypher"]["url"]) + ("/addrs/%s/balance" % address)
    return requests.get(url=url, headers=headers, timeout=timeout).json()["balance"]


# Get unspent transaction by address
def get_unspent_transactions(address, network="testnet",
                             include_script=True, limit=15, timeout=bitcoin["timeout"]):
    """
    Get Bitcoin unspent transaction output (UTXO).

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param include_script: Bitcoin include script, defaults to True.
    :type include_script: bool
    :param limit: Bitcoin utxo's limit, defaults to 15.
    :type limit: int
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: list -- Bitcoin utxo's.

    >>> from swap.providers.bitcoin.rpc import get_unspent_transactions
    >>> get_unspent_transactions(bitcoin_address, "testnet")
    [...]
    """

    if not is_address(address=address, network=network):
        raise AddressError("invalid %s %s address" % (network, address))
    _include_script = "true" if include_script else "false"
    parameter = dict(limit=limit, unspentOnly="true",
                     includeScript=_include_script, token=bitcoin[network]["blockcypher"]["token"])
    url = bitcoin[network]["blockcypher"]["url"] + ("/addrs/%s" % address)
    response = requests.get(url=url, params=parameter, headers=headers, timeout=timeout).json()
    return response["txrefs"] if "txrefs" in response else []


# Get transaction detail by hash
def get_transaction_detail(transaction_id, network="testnet", timeout=bitcoin["timeout"]):
    """
    Get transaction detail.

    :param transaction_id: Bitcoin transaction hash or transaction id.
    :type transaction_id: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bitcoin transaction detail.

    >>> from swap.providers.bitcoin.rpc import get_transaction_detail
    >>> get_transaction_detail(transaction_id, "testnet")
    {...}
    """

    parameter = dict(token=bitcoin[network]["blockcypher"]["token"])
    url = bitcoin[network]["blockcypher"]["url"] + ("/txs/%s" % transaction_id)
    return requests.get(url=url, params=parameter,
                        headers=headers, timeout=timeout).json()


# Getting decode transaction by transaction raw
def decoded_transaction_raw(transaction_raw, network="testnet", timeout=bitcoin["timeout"]):
    """
    Get decoded transaction raw.

    :param transaction_raw: Bitcoin transaction raw.
    :type transaction_raw: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bitcoin decoded transaction raw.

    >>> from swap.providers.bitcoin.rpc import decoded_transaction_raw
    >>> decoded_transaction_raw(transaction_raw, "testnet")
    {...}
    """

    if isinstance(transaction_raw, str):
        parameter = dict(token=bitcoin[network]["blockcypher"]["token"])
        tx = json.dumps(dict(tx=transaction_raw))
        return requests.post(url=bitcoin[network]["blockcypher"]["url"] + "/txs/decode",
                             data=tx, params=parameter, headers=headers, timeout=timeout).json()
    raise TypeError("transaction raw must be string format!")


# Submit payment from blockcypher
def submit_payment(tx_raw, network="testnet", timeout=bitcoin["timeout"]):
    """
    Submit transaction raw to Bitcoin blockchain.

    :param tx_raw: Bitcoin transaction raw.
    :type tx_raw: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bitcoin decoded transaction raw.

    >>> from swap.providers.bitcoin.rpc import submit_payment
    >>> submit_payment(transaction_raw, "testnet")
    {...}
    """

    if isinstance(tx_raw, str):
        tx = json.dumps(dict(tx_hex=tx_raw))
        if "mainnet" == network:
            sochain_network = "BTC"
        elif "testnet" == network:
            sochain_network = "BTCTEST"
        else:
            raise ValueError("invalid network, only mainnet or testnet")
        url = bitcoin[network]["sochain"] + f"/send_tx/{sochain_network}"
        response = requests.post(url=url, data=tx, headers=headers, timeout=timeout)
        if "status" in response.json() and response.json()["status"] == "fail":
            raise APIError(response.json()["data"]["tx_hex"])
        elif "status" in response.json() and response.json()["status"] == "success":
            return response.json()["data"]
        else:
            raise Exception("Unknown Bitcoin submit payment error")
    raise TypeError("transaction raw must be string format!")
