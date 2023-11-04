from web3 import Web3
import time
from loguru import logger
from config import MAX_GWEI, Base_GWEI


def base_gas():
    try:
        w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
        gas_price = w3.eth.gas_price
        gwei_gas_price = w3.from_wei(gas_price, 'gwei')
        return gwei_gas_price
    except Exception as error:
        logger.error(error)
        return base_gas()


def eth_gas():
    try:
        w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
        gas_price = w3.eth.gas_price
        gwei_gas_price = w3.from_wei(gas_price, 'gwei')
        return gwei_gas_price
    except Exception as error:
        logger.error(error)
        return eth_gas()



def wait_eth_gas():
    while True:
        current_gas = eth_gas()
        if current_gas > MAX_GWEI:
            logger.info(f'current_gas : {round(current_gas, 1)} > {MAX_GWEI} Жду понижения...')
            time.sleep(60)
        else:
            logger.info(f'ETH gas: {round(current_gas, 1)} Gwei')
            break


def wait_base_gas():
    while True:
        current_gas = base_gas()
        if current_gas > Base_GWEI:
            logger.info(f'Chain gas price: {round(current_gas, 1)} Gwei > {Base_GWEI} Жду понижения...')
            time.sleep(60)
        else:
            logger.info(f'Chain gas price: {round(current_gas, 1)} Gwei. Отправляю транзакцию')
            break
