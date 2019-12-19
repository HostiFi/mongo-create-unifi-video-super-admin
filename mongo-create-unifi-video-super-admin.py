import json
import random
import string
import time
from random import SystemRandom
from datetime import datetime
import argparse
import pymongo
from bson.objectid import ObjectId
import bcrypt

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='UniFi Video username to create')
parser.add_argument('-e','--email', help='UniFi Video username to create')
parser.add_argument('-p','--password', help='UniFi Video password to create')
args = parser.parse_args()

randchoice = SystemRandom().choice
client = pymongo.MongoClient("mongodb://127.0.0.1:7441/av")
mdb = client.av

class Server():
    def __init__(self, server_name):
        self.server_name = server_name

    def _create_user(self, account_id, super_admin_id):
        print "Deleting user for"
        print account_id
        response = ''
        print self.server_name
        response = mdb.user.insert({'accountId': ObjectId(account_id), 'userGroupId': ObjectId(account_id), "disabled" : False, "enableApiAccess" : False, "enableLocalAccess" : True, "motionAlertSchedules" : {  }, "adoptionKey" : "gvmWzctP", "enableEmail" : True, "enablePush" : True, "sysDisconnectEmailAlert" : True, "sysDisconnectPushAlert" : True })
        print "Response:"
        print response
        return response

    def _create_account(self, username, email, hashed):
        print "Creating account for"
        print username
        response = ''
        print self.server_name
        response = mdb.account.insert({'username': username, 'password': hashed, 'name': username, 'language': 'English'})
        print "Response:"
        print response
        return response

    def _get_account_id(self, username):
        print "Getting account id for"
        print username
        response = ''
        print self.server_name
        response = mdb.account.find({'username': username})
        print "Account id:"
        print response[0]["_id"]
        return response[0]["_id"]

    def _get_super_admin_user_group_id(self):
        print "Getting Super Admin id"
        response = ''
        print self.server_name
        response = mdb.usergroup.find({'groupType': "SUPER_ADMIN"}, {"_id"})
        print "Super Admin id:"
        print response[0]["_id"]
        return response[0]["_id"]

    def create_super_admin(self, username, email, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        super_admin_id = self._get_super_admin_user_group_id()
        self._create_account(username, email, hashed)
        account_id = self._get_account_id(username)
        self._create_user(account_id, super_admin_id)

    def _logout_of_ssh(self):
        print "Logging out of SSH"

if args.email is not None and args.password is not None and args.username is not None:
    unifi_video_server = Server('localhost')
    unifi_video_server.create_super_admin(args.username, args.email, args.password)
else:
    print "Error: Missing arguments. --username, --password, and --email are required."