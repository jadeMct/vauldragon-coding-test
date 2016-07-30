from pymongo import MongoClient
import requests
import datetime
import time
import json
from bson.json_util import dumps


def get_value_timest(url):

    while 1:
        
        gvts = input("Get a value at timestamp? (y/n) \n")
        if ((gvts.strip() == 'n') or (gvts.strip() == 'N')):
            break
        if ((gvts.strip() == 'y') or (gvts.strip() == 'Y')):
            get_key = input("Add a key: \n")
            timestamp = input("Add a timestamp\n")

    new_url = "{}/{}?{}".format(url, get_key, timestamp)
    return requests.get(new_url)
    
def get_value(url):

    while 1:
        
        gv = input("Get a value? (y/n) \n")
        if ((gv.strip() == 'n') or (gv.strip() == 'N')):
            return 0
        if ((gv.strip() == 'y') or (gv.strip() == 'Y')):
            get_key = input("Add a key: \n")
    
            new_url = "{}/{}".format(url, get_key)
            print(new_url)
            return requests.get(new_url)
    

def add_key(url, payload, db):

    while 1:
        
        kv = input("Add a key-value pair? (y/n) \n")
        if kv.strip() == 'n' or kv.strip() == 'N':
            return 0
        if ((kv.strip() == 'y') or (kv.strip() == 'Y')):
            mykey = input("Add a key: \n")
            nb_val = input("How many values do you want to add ?\n")
            if int(nb_val) == 0:
                 if mykey in payload:
                    payload[mykey] = 'None'
                 else:
                    payload.update({mykey : 'None'})
            if int(nb_val) == 1:
                value = input("Type your value: \n")
                if mykey in payload:
                    payload[mykey] = value
                else:
                    payload.update({mykey : value})
            if int(nb_val) > 1:
                i = 1
                if mykey in payload:
                    payload[mykey] = []
                    while i <= int(nb_val):
                        val = input("Add a value:\n")
                        value = val
                        payload[mykey].append(value)
                        i += 1
                else:
                    while i <= int(nb_val):
                        val = input("Add a value: \n")
                        value = val
                        payload.setdefault(mykey, [])
                        payload[mykey].append(value)
                        i += 1

            payload.update({'timestamp' : str(time.time())})
            print(payload)
    
            posts = db.posts
            post_id = posts.insert_one(payload)
            print("Storage:", post_id)

            return requests.post(url, data = dumps([payload]))

def add_url():

    while 1:
        new_url = input("Which URL? (HTTP) \n")
        if(new_url != ""):
            break
    return new_url

def main():

    payload = dict()

    url = add_url()

    client = MongoClient('mongodb://192.168.1.249', 27017)
    db = client.key_store

    while 1:

        post = add_key(url, payload, db)
        if post != 0:
            if post.status_code != 201:
                print("API Error - Post not done")
            print("Post: ", post.text)

        get = get_value(url)
        if get.status_code != 200:
            print("API Error - no response !")
        print("Get: ", get.text)

        get_timest = get_value_timest(url)
        if post != 0:
            if get_timest.status_code != 200:
                print("API Error - no response !")
            print(get_timest.text)
            

        n = input("Do you want to continue? (y/n) \n")
        if n.strip() == 'n':
            break
        
if __name__ == '__main__':
    main()













