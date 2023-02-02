from pymongo import MongoClient
from utils import get_database_name, get_field
import re


def main():
    """Main loop"""
    
    with MongoClient('localhost', 27017) as mongo_client:
        db = mongo_client[get_database_name()]

        messages = db.messages

        msgs_w_group_link = messages.find({"message": {"$regex": "t\.me"}})
        
        new_groups = dict()
        for msg in msgs_w_group_link:
            urls = set(re.findall('t\.me\/[a-zA-Z0-9\+\-\_]+', msg["message"]))
            for u in urls:
                if u in new_groups:
                    new_groups[u].add(msg["_id"]["dialog_id"])
                else:
                    new_groups[u] = set()
                    new_groups[u].add(msg["_id"]["dialog_id"])
        
        new_groups_count = dict()
        for ngp in new_groups.keys():
            new_groups_count[ngp] = len(new_groups[ngp])
        
        with open(get_field("scrapping", "new_dialogs_file"), "w") as fp:
            for ngp, count in sorted(new_groups_count.items(), key=lambda item: item[1], reverse=True):
                fp.write(ngp + " : " + str(count) + '\n')
                
if __name__ == "__main__":
    main()