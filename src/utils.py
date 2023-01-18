from telethon import TelegramClient
import configparser

CONFIG_FILE = "../artifacts/config.ini"

def __config():
    """ Returns the configuration file

    Returns:
        data (dict): configuration data
    """
    # with open(CONFIG_FILE) as fp:
        # data = yaml.load(fp, Loader=SafeLoader)
        # return data
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def get_telethon_client(name_session="base"):
    """_summary_

    Args:
        name_session (str, optional): Name of the session. Defaults to "base".

    Returns:
        obj: client instance
    """
    config = __config()

    api_id = config.get("telethon", "api_id")
    api_hash = config.get("telethon", "api_hash")
    client = TelegramClient(name_session, api_id, api_hash).start()

    # You will be asked to enter your mobile number- Enter mobile number with country code
    # Enter OTP (For OTP check Telegram inbox)
    return client
        