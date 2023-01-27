from utils import get_telethon_client, get_database_name, get_start_date
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import is_audio, is_image, is_video
from telethon import errors
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os

DATABASE_NAME = "T8Jan"
MEDIAPATH = "../data/{}/{}/{}.{}"

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


async def scrap_dialog(tlt_client, mongo_client, dlg, media=True, start_date=None):
    """get message from a given

    Args:
        tlt_client (object): telethon client
        mongo_client (object): mongodb client
        dialog_id (int): id of the dialog to be scraped
        media (bool, optional): If it will download the media attached to
                                the messages. Defaults to True.
    """

    db = mongo_client.T8Jan
    dialog_id = dlg.id
    
    # scrap users
    users = db.users
    user_list = []
    try:
        user_list = await tlt_client.get_participants(dlg.entity)
    except errors.ChatAdminRequiredError:
        pass

    for user in user_list:
        user_dt = user.to_dict()
        user_dt["_id"] = {"dialog_id": dialog_id, "user_id": user.id}
        try:
            users.insert_one(user_dt)
            print("Insert Successful", user_dt["_id"])
        except DuplicateKeyError:
            print("Existing Key for User", user_dt["_id"])
            pass
            
    # scrap messages
    messages = db.messages
    async for msg in tlt_client.iter_messages(dialog_id):
        try:
            dialog_id_trim = msg.peer_id.channel_id
        except AttributeError:
            dialog_id_trim = str(dialog_id)
            pass

        #db = mongo_client.messages(message.to_json())
        msg_dt = msg.to_dict()
        msg_dt["_id"] = {"dialog_id": dialog_id, "message_id": msg_dt["id"]} 

        if start_date is not None:
            if msg_dt["date"] < start_date:
                return

        if "message" in msg_dt.keys():
            print(msg_dt["message"])

        try:
            messages.insert_one(msg_dt)
            print("Insert Successful", msg_dt["_id"])
        except DuplicateKeyError:
            print("Existing Key for Message", msg_dt["_id"])
            pass

        if msg.media and media is True:
            if is_audio(msg.media):
                filepath = MEDIAPATH.format(dialog_id_trim, "voices", msg.id, "mp3")
                if os.path.isfile(filepath) is False:
                    print(filepath)
                    await msg.download_media(filepath)
            elif is_image(msg.media):
                filepath = MEDIAPATH.format(dialog_id_trim, "images", msg.id, "png")
                if os.path.isfile(filepath) is False:
                    print(filepath)
                    await msg.download_media(filepath)
            elif is_video(msg.media):
                filepath = MEDIAPATH.format(dialog_id_trim, "videos", msg.id, "mp4")
                if os.path.isfile(filepath) is False:
                    print(filepath)
                    await msg.download_media(filepath)

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
    
    start_date = get_start_date()
    
    with MongoClient('localhost', 27017) as mongo_client:
        db = mongo_client[get_database_name()]
        async for dlg in tlt_client.iter_dialogs():
            dialogs = db.dialogs
            dialogdoc = dialog_document(dlg)

            try:
                dialogs.insert_one(dialogdoc)
            except DuplicateKeyError:
                print("Existing Key for Dialog", dialogdoc["_id"])
                pass

            await scrap_dialog(tlt_client, mongo_client, dlg, True, start_date)


if __name__ == "__main__":
    tlt_client = get_telethon_client()

    with tlt_client:
        tlt_client.loop.run_until_complete(main())
