from utils import get_client

async def list_dialogs(client):
    """ list all dialogs you are part of (name and id)

    Args:
        client (object): telethon client object
    """
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)


async def scrap_dialog(client, dialog_id, media=True):
    """ get message from a given 

    Args:
        client (object): telethon client object
        dialog_id (int): id of the dialog to be scraped
        media (bool, optional): If it will download the media attached to 
                                the messages. Defaults to True.
    """

    async for message in client.iter_messages(dialog_id):
        print(message.to_json())

        if media is True:
            await message.download_media(file="../data/test")
    
async def main():
    await scrap_dialog(client, 1001869654432, media=False)


client = get_client()

with client:
    client.loop.run_until_complete(main())

