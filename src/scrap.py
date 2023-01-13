from utils import get_client

async def get_groups(client):
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)
    
async def main():

    async for message in client.iter_messages(1001869654432):
        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        await message.download_media(file="../data/test")

client = get_client()

with client:
    client.loop.run_until_complete(main())

