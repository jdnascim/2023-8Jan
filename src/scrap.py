from utils import get_telethon_client
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import is_audio, is_image, is_video
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import pandas as pd

DATABASE_NAME = "T8Jan"

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
    profile = await tlt_client(GetFullUserRequest(user))
    print(profile.to_json())


async def scrap_dialog(tlt_client, mongo_client, dialog_id, media=True):
    """get message from a given

    Args:
        tlt_client (object): telethon client
        mongo_client (object): mongodb client
        dialog_id (int): id of the dialog to be scraped
        media (bool, optional): If it will download the media attached to
                                the messages. Defaults to True.
    """

    db = mongo_client.T8Jan
    messages = db.messages
    
    async for msg in tlt_client.iter_messages(dialog_id):
        #db = mongo_client.messages(message.to_json())
        msg_dt = msg.to_dict()
        msg_dt["_id"] = {"dialog_id": dialog_id, "message_id": msg_dt["id"]} 

        if "message" in msg_dt.keys():
            print(msg_dt["message"])

        try:
            messages.insert_one(msg_dt)
        except DuplicateKeyError:
            print("Existing Key for Message")
            pass

        if msg.media and media is True:
            if is_audio(msg.media):
                await msg.download_media(file=f"../data/{dialog_id}/voices/{msg.id}.mp3")
            elif is_image(msg.media):
                await msg.download_media(file=f"../data/{dialog_id}/images/{msg.id}.png")
            elif is_video(msg.media):
                await msg.download_media(file=f"../data/{dialog_id}/videos/{msg.id}.mp4")

def dialog_document(dialog):
    """ returns document representing the given dialog
        to be stored in MongoDB

    Args:
        dialog (obj): dialog object

    Returns:
        dict: dialog document
    """
    dialogdt = dialog.to_dict()

    dialogdoc = dialogdt["entity"].to_dict()
    dialogdoc["_id"] = dialog.id

    return dialogdoc


async def main():
    """Main loop"""
    
    with MongoClient('localhost', 27017) as mongo_client:
        db = mongo_client[DATABASE_NAME]
        async for dlg in tlt_client.iter_dialogs():
            dialogs = db.dialogs
            dialogdoc = dialog_document(dlg)

            try:
                dialogs.insert_one(dialogdoc)
            except DuplicateKeyError:
                print("Existing Key for Dialog")
                pass

            await scrap_dialog(tlt_client, mongo_client, dialogdoc["_id"], media=True)


if __name__ == "__main__":
    tlt_client = get_telethon_client()

    with tlt_client:
        tlt_client.loop.run_until_complete(main())
