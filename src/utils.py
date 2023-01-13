# import pyyaml module
import yaml
from yaml.loader import SafeLoader
from telethon import TelegramClient, sync

CONFIG_FILE = "../artifacts/config.yml"

def __config():
    """ Returns the configuration file

    Returns:
        data (dict): configuration data
    """
    with open(CONFIG_FILE) as fp:
        data = yaml.load(fp, Loader=SafeLoader)
        return data

def get_client(name_session="base"):
    """_summary_

    Args:
        name_session (str, optional): Name of the session. Defaults to "base".

    Returns:
        obj: client instance
    """
    config = __config()

    api_id = config["api_id"]
    api_hash = config["api_hash"]
    client = TelegramClient(name_session, api_id, api_hash).start()

    # You will be asked to enter your mobile number- Enter mobile number with country code
    # Enter OTP (For OTP check Telegram inbox)
    return client
        