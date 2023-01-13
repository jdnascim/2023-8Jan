from utils import get_client
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import is_audio, is_image, is_video


async def list_dialogs(client):
    """list all dialogs you are part of (name and id)

    Args:
        client (object): telethon client object
    """
    async for dialog in client.iter_dialogs():
        print(dialog.name, "has ID", dialog.id)


async def scrap_profile_picture(client, entity):
    """get the profile picture of a given entity (i.e., user or group)

    Args:
        client (object): telethon client object
        entity (object): telethon entity
    """

    await client.download_profile_photo(entity, file=f"../data/profile/{entity}.png")


async def scrap_profile_info(user):
    """get user profile

    Args:ß
        user (object): username or user_id
    """
    profile = await client(GetFullUserRequest(user))
    print(profile.to_json())


async def scrap_dialog(client, dialog_id, media=True):
    """get message from a given

    Args:
        client (object): telethon client object
        dialog_id (int): id of the dialog to be scraped
        media (bool, optional): If it will download the media attached to
                                the messages. Defaults to True.
    """

    async for message in client.iter_messages(dialog_id):
        # print(message.to_json())

        # if media is True:
        #     await message.download_media(file="../data/test")

        # if message.photo:
        #     path = await message.download_media(file=f"../data/images/{message.id}.png")
        #     print("File saved to", path)  # printed after download is done
        if message.media:
            if is_audio(message.media):
                await message.download_media(file=f"../data/{dialog_id}/voices/{message.id}.mp3")
            elif is_image(message.media):
                await message.download_media(file=f"../data/{dialog_id}/images/{message.id}.png")
            elif is_video(message.media):
                await message.download_media(file=f"../data/{dialog_id}/videos/{message.id}.mp4")

        


async def main():
    """Main loop"""
    # await list_dialogs(client)
    await scrap_dialog(client, 382371748, media=False)
    # await scrap_profile_info(90037115)
    # await scrap_profile_picture(client, 382371748)


if __name__ == "__main__":
    client = get_client()

    with client:
        client.loop.run_until_complete(main())
