import binascii
import hashlib
import hmac

import base58
import ecdsa
from bip32utils import BIP32Key
from mnemonic import Mnemonic
from pbkdf2 import PBKDF2
import string, re
from solders.keypair import Keypair
from solders.pubkey import Pubkey

import logging

logging.basicConfig(filename='kalyna_wallet.log', level=logging.INFO)
logger = logging.getLogger(__name__)

from typing import Union
from httpx import Timeout

CURRENT_BLOCKCHAIN = 'solana'

# Константа для определения URL-адреса узла Solana в тестовой сети Devnet
# SOLANA_NODE_URL = "https://api.testnet.solana.com"
SOLANA_NODE_URL = "https://api.devnet.solana.com"

# Например, установить таймаут на чтение ответа 120 секунд, таймаут на соединение 20 секунд
timeout_settings = Timeout(read=120.0, connect=20.0, write=None, pool=None)
from solana.rpc.api import Client

client = Client(SOLANA_NODE_URL)
# Константа для определения соотношения между лампортами и SOL. 1 SOL = 10^9 лампортов.
LAMPORT_TO_SOL_RATIO = 10 ** 9


def generate_cusom_mnemo(text):
    # Remove punctuation
    text = re.sub(r'[^a-zA-Zа-яА-ЯїЇіІ\s]', '',
                  text)  # text  = ''.join([char for char in text if char not in string.punctuation])
    text = text.lower()
    words = text.split()
    words = [word for word in words if len(word) >= 5]
    seen = set()
    unique_words = []
    for item in words:
        if item not in seen:
            unique_words.append(item)
            seen.add(item)

    words = unique_words[:12]
    return " ".join(words) if len(words) == 12 else None


def get_solana_keypair_from_mnemo_words(mnemo_words):
    mnemo = Mnemonic()
    seed = mnemo.to_seed(mnemo_words)
    keypair = Keypair.from_seed(seed[:32])
    return keypair


def get_solana_derived_wallet(mnemo_words):
    """
        Takes a Solana wallet.
        Returns:
            Tuple[str, str]: A tuple containing the public address and private key of the wallet.
        Raises:
            Exception: If there's an error during the wallet creation process.
    """
    mnemo = Mnemonic()
    seed = mnemo.to_seed(mnemo_words)
    try:
        solana_derivation_path = "m/44'/501'/0'/0'"
        keypair = Keypair.from_seed_and_derivation_path(seed, solana_derivation_path)
        wallet_address = str(keypair.pubkey())
        private_key = keypair.secret().hex()
        return wallet_address, private_key

    except Exception as e:
        logger.error(f"Failed to get a Solana wallet: {e}\n")
        # Поднятие нового исключения с подробной информацией
        raise Exception(f"Failed to create Solana wallet: {e}")


def get_sol_balance(wallet_address):
    """
        retrieves the SOL balance for the specified wallet addresses.

        Args:
            wallet_addresses (Union[str, List[str]]): The wallet address or a list of wallet addresses.
        Returns:
            Union[float, List[float]]: The SOL balance corresponding to the wallet address.
    """
    try:
        balance = (client.get_balance(Pubkey.from_string(wallet_address))).value
        # Преобразование лампортов в SOL
        sol_balance = balance / LAMPORT_TO_SOL_RATIO
        logger.debug(f"wallet_address: {wallet_address}, balance: {balance}, sol_balance: {sol_balance}")
        return sol_balance
    except Exception as error:
        logger.error(f"Failed to get Solana balance: {error}\n")
        raise Exception(f"Failed to get Solana balance: {error}\n")


def transfer_coins(sender_address: str, sender_private_key: str, recipient_address: str, amount: float):
    """
    Asynchronous function to transfer coins between wallets.

    Args:
    sender_address (str): Sender's address.
    sender_private_key (str): Sender's private key.
    recipient_address (str): Recipient's address.
    amount (float): Amount of tokens to transfer.

    Raises:
    ValueError: If any of the provided addresses is invalid or the private key is invalid.

    Returns:
    bool: True if the transfer is successful, False otherwise.
    """

def mnemonic_to_seed(mnemonic_phrase, passphrase=''):
    mnemo = Mnemonic()  # Create a new instance of the Mnemonic class
    seed = mnemo.to_seed(mnemonic_phrase, passphrase)
    return seed.hex()

def seed_to_keys(seed):
    # Convert the seed to bytes if it's in hex format
    seed_bytes = binascii.unhexlify(seed)
    # Use the seed to create the master key
    bip32_root_key = BIP32Key.fromEntropy(seed_bytes)
    # Extract the master private key
    master_private_key = bip32_root_key.PrivateKey().hex()
    # Extract the master public key
    master_public_key = bip32_root_key.PublicKey().hex()

    return master_private_key, master_public_key