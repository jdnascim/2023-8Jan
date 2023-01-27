from telethon import TelegramClient
from datetime import datetime
import pytz
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
        
def get_database_name():
    """ wrapper for getting the database name in MongoDB

    Returns:
        str: database name
    """
    config = __config()

    return config.get("mongodb", "database_name")
    
    
def get_start_date():
    config = __config()

    datestr = config.get("scrapping", "start_date")
    date = datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%SZ")

    utc=pytz.UTC
    utc_date = utc.localize(date)

    return utc_date

    
    