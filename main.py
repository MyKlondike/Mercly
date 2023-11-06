import math
import time
import random
from web3 import Web3
from eth_abi import encode
from loguru import logger
from decimal import Decimal
import traceback
from helper import wait_eth_gas, wait_base_gas
from config import amount_from, amount_to, delay_from, delay_to, source
from contract import refuel
from abi import abi
from data import DATA

amount = int(Decimal(random.uniform(amount_from, amount_to)) * Decimal("1e18"))
chain_from = source
w3 = Web3(Web3.HTTPProvider(DATA[chain_from]['rpc']))
contract = w3.eth.contract(address = Web3.to_checksum_address(refuel[chain_from]), abi = abi)


with open("wallets.txt", "r") as file:
    key = [row.strip() for row in file]


def get_adapter_params(privatekey):
    account = w3.eth.account.from_key(privatekey)
    wallet = Web3.to_checksum_address(account.address)
    params = Web3.to_hex(encode(["uint16", "uint64", "uint256"], [2, 250000, amount])[30:])
    adapter_params = params + wallet[2:].lower()
    return adapter_params


def sign_tx(w3, contract_txn, privatekey):
    signed_tx = w3.eth.account.sign_transaction(contract_txn, privatekey)
    raw_tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = w3.to_hex(raw_tx_hash)
    return tx_hash


def check_status_tx(tx_hash):
    start_time_stamp = int(time.time())
    while True:
        try:

            rpc_chain = DATA[chain_from]['rpc']
            web3 = Web3(Web3.HTTPProvider(rpc_chain))
            status_ = web3.eth.get_transaction_receipt(tx_hash)
            status = status_["status"]

            if status in [0, 1]:
                return status

        except Exception as error:
            time_stamp = int(time.time())
            if time_stamp - start_time_stamp > 100:
                logger.info(f'{error} не получили tx_status за {100} sec, вероятно tx is success')
                return 1
            time.sleep(1)


def merkly_refuel(privatekey, retry=1):
    try:
        module_str = f'merkly_refuel : {chain_from} => scroll'
        logger.info(module_str)
        adapter_params = get_adapter_params(privatekey)
        account = w3.eth.account.from_key(privatekey)
        wallet = Web3.to_checksum_address(account.address)
        logger.info(f'From address | {wallet}')
        nonce = w3.eth.get_transaction_count(wallet)
        payload = b''
        gas_price = w3.eth.gas_price
        native_fee = contract.functions.estimateSendFee(214, payload, adapter_params).call()
        value = int(math.ceil(native_fee[0] * 1.01))

        gas = contract.functions.bridgeGas(214, wallet, adapter_params).estimate_gas({'from': wallet, 'nonce': nonce, 'value': value})

        contract_txn = contract.functions.bridgeGas(214, wallet, adapter_params).build_transaction({
            'from': wallet,
            'value': value,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas,
        })

        tx_hash = sign_tx(w3, contract_txn, privatekey)
        tx_link = f'{DATA[chain_from]["scan"]}/{tx_hash}'

        status = check_status_tx(tx_hash)

        if status == 1:
            logger.success(f'{tx_link}')
            return "success"
        else:
            if retry < 1:
                logger.info(f'tx is failed, try again in 10 sec | {tx_link}')
                time.sleep(10)
                merkly_refuel(privatekey, retry + 1)
            else:
                logger.error(f'tx is failed | {tx_link}')

    except Exception as error:
        logger.error(f'{module_str} | {error}')
        traceback.print_exc()

        if retry < 1:
            logger.info(f'try again | {wallet}')
            time.sleep(10)
            merkly_refuel(privatekey, retry + 1)
        else:
            logger.error(f'Maximum retry limit reached')
            return "max_retries_exceeded"


def main():
    random.shuffle(key)
    total_wallets = len(key)
    number = 0
    for privatekey in key:
        number += 1
        print(f"\nОбработка кошелька {number} из {total_wallets}")
        wait_eth_gas()
        if chain_from == "base":
            wait_base_gas()
        merkly_refuel(privatekey)
        sleep = random.randint(delay_from, delay_to)
        if number != total_wallets:
            print(f"Следующий кошелек будет обработан через {sleep} сек.")
            time.sleep(sleep)
        else:
            print(f"\nВсе кошельки успешно обработаны!")


if __name__ == "__main__":
    main()
