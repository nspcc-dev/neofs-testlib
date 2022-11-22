import json
import logging

logger = logging.getLogger("neofs.testlib.utils")

def get_first_address_from_wallet(wallet_path: str):
    """
    Extracting the last address from the given wallet.
    Args:
        wallet_path:  The path to the wallet to extract address from.
        wallet_password: The password for the given wallet.
    Returns:
        The address for the wallet.
    """
    with open(wallet_path) as wallet_file:
        wallet = json.loads(wallet_file.read())
    address = wallet.get('accounts')[0]['address']
    logger.info(f"got address: {address}")
    return address

def get_last_address_from_wallet(wallet_path: str):
    """
    Extracting the last address from the given wallet.
    Args:
        wallet_path:  The path to the wallet to extract address from.
        wallet_password: The password for the given wallet.
    Returns:
        The address for the wallet.
    """
    with open(wallet_path) as wallet_file:
        wallet = json.loads(wallet_file.read())
    address = wallet.get('accounts')[-1]['address']
    logger.info(f"got address: {address}")
    return address
