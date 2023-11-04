import time
import random
from web3 import Web3
from eth_abi import encode
from loguru import logger
from decimal import Decimal
import traceback
from helper import wait_eth_gas, wait_base_gas
from config import amount_from, amount_to, delay_from, delay_to
base = {'rpc': 'https://mainnet.base.org', 'scan': 'https://basescan.org/tx', 'token': 'ETH', 'chain_id': 8453}
scroll = {"rpc": "https://scroll.blockpi.network/v1/rpc/public", "scan": "https://scrollscan.com/tx", "token": "ETH", "chain_id": 534352}


amount = int(Decimal(random.uniform(amount_from, amount_to)) * Decimal("1e18"))


w3 = Web3(Web3.HTTPProvider(base['rpc']))
contract = w3.eth.contract(address = Web3.to_checksum_address('0x6bf98654205b1ac38645880ae20fc00b0bb9ffca'),
                           abi = '[{"inputs":[{"internalType":"address","name":"_lzEndpoint","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":false,"internalType":"uint64","name":"_nonce","type":"uint64"},{"indexed":false,"internalType":"bytes","name":"_payload","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"_reason","type":"bytes"}],"name":"MessageFailed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"indexed":false,"internalType":"uint64","name":"_nonce","type":"uint64"},{"indexed":false,"internalType":"bytes32","name":"_payloadHash","type":"bytes32"}],"name":"RetryMessageSuccess","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"indexed":false,"internalType":"uint16","name":"_type","type":"uint16"},{"indexed":false,"internalType":"uint256","name":"_minDstGas","type":"uint256"}],"name":"SetMinDstGas","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"precrime","type":"address"}],"name":"SetPrecrime","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_path","type":"bytes"}],"name":"SetTrustedRemote","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"_remoteAddress","type":"bytes"}],"name":"SetTrustedRemoteAddress","type":"event"},{"inputs":[],"name":"DEFAULT_PAYLOAD_SIZE_LIMIT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NO_EXTRA_GAS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PT_SEND","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_toAddress","type":"bytes"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"bridgeGas","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"payload","type":"bytes"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"estimateSendFee","outputs":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"zroFee","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint64","name":"","type":"uint64"}],"name":"failedMessages","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"forceResumeReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"_configType","type":"uint256"}],"name":"getConfig","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"}],"name":"getTrustedRemoteAddress","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"isTrustedRemote","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lzEndpoint","outputs":[{"internalType":"contract ILayerZeroEndpoint","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"lzReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"uint16","name":"","type":"uint16"}],"name":"minDstGasLookup","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"nonblockingLzReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"payloadSizeLimitLookup","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"precrime","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"retryMessage","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"uint256","name":"_configType","type":"uint256"},{"internalType":"bytes","name":"_config","type":"bytes"}],"name":"setConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint16","name":"_packetType","type":"uint16"},{"internalType":"uint256","name":"_minGas","type":"uint256"}],"name":"setMinDstGas","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint256","name":"_size","type":"uint256"}],"name":"setPayloadSizeLimit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_precrime","type":"address"}],"name":"setPrecrime","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setReceiveVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"}],"name":"setSendVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"internalType":"bytes","name":"_path","type":"bytes"}],"name":"setTrustedRemote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_remoteChainId","type":"uint16"},{"internalType":"bytes","name":"_remoteAddress","type":"bytes"}],"name":"setTrustedRemoteAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"trustedRemoteLookup","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"useCustomAdapterParams","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"payable","type":"function"}]')

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

            rpc_chain = base['rpc']
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
        module_str = f'merkly_refuel : base => scroll'
        logger.info(module_str)
        adapter_params = get_adapter_params(privatekey)
        account = w3.eth.account.from_key(privatekey)
        wallet = Web3.to_checksum_address(account.address)
        nonce = w3.eth.get_transaction_count(wallet)
        payload = b''
        gasPrice = w3.eth.gas_price
        nativeFee = contract.functions.estimateSendFee(214, payload, adapter_params).call()
        value = amount + nativeFee[0]

        contract_txn = contract.functions.bridgeGas(214, wallet, adapter_params).build_transaction({
            'from': wallet,
            'value': value,
            'nonce': nonce,
            'gasPrice': gasPrice,
            'gas': 250000,
        })

        tx_hash = sign_tx(w3, contract_txn, privatekey)
        tx_link = f'{base["scan"]}/{tx_hash}'

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
        print(f"Обработка кошелька {number} из {total_wallets}")
        wait_eth_gas()
        wait_base_gas()
        merkly_refuel(privatekey)
        sleep = random.randint(delay_from, delay_to)
        if number != total_wallets:
            print(f"Следующий кошелек будет обработан через {sleep} сек.")
            time.sleep(sleep)
        else:
            print(f"Все кошельки успешно обработаны!")


if __name__ == "__main__":
    main()
