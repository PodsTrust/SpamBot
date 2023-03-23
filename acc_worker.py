from db import User
import datetime

import pytz

import sys

from telethon import TelegramClient, events, sync, types
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio
import random
import time
import threading
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest,HideChatJoinRequestRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.errors import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import UserStatusLastWeek,UserStatusOffline,UserStatusLastMonth,UserStatusRecently,UserStatusEmpty
from db import Username


api_id = 28433121
api_hash = "e25a851b3b347d74b7b8f88d6ba5f856"
name = "acc.session"
# count = 15
SESSION = "1ApWapzMBuwVNI2FfgJNhhuCkbqkTTkG-dTHfM5zep-Kg7AOkRcvPklpNJKrfY8FBWUKy7QA170kOZjwkCNSwtNXs-UuYtf2S3Yr4I-VqaiK6juVxDGgNtNDVPZoE7cRSk3qmXlABdfy_wC6CWIzktujdOQdfvAavp_8eDJmRO516GimbbYu8SBCipFfB2j0BQQexc3vr-UAs5xIdiAxQLTK2gX4FGc69QBwOTOzP4T0VdvszstQBSdhsRqWHrFnwH7r0nCjI0W_gsMnIbMwoOvQuemXQvHJmue4dYHOsRbvlFqi4iltSfBXEVv-qaes89W7OqdGq_e6UMvinZIYWUMZOUqLEBSY="
# with TelegramClient(name, api_id, api_hash) as client:
#     print(StringSession.save(client.session))
client = TelegramClient(StringSession(SESSION),api_id,api_hash)
l = 0


async def join_and_parse(group):
    # result = await client(JoinChannelRequest(
    #     channel="https://t.me/+1MTVZMg8ltQ2OTUy"
    # ))
    if group.startswith("https://t.me/"):
        entity = group.replace("https://t.me/","")
        if entity.startswith("+"):
            entity = entity[1:]
            chat_invite = await client(ImportChatInviteRequest(entity))
        else:
            chat_invite = await client(JoinChannelRequest(
                channel=entity
            ))
    else:
        if group.startswith("@"):
            entity = group[1:]
        else:
            entity = group
        chat_invite = await client(JoinChannelRequest(
            channel=entity
        ))
    print(chat_invite)
    print("JOINED TO GROUP")
    ll = []
    ADDED = 0
    DUBL = 0
    if chat_invite.users:
        users = chat_invite.users
    else:
        users = await client.get_participants(entity)
    for i in users:
        if i.username and i.bot == False and i.is_self == False:
            if isinstance(i.status, UserStatusLastMonth):
                continue
            if isinstance(i.status, UserStatusLastWeek):
                continue
            if isinstance(i.status, UserStatusOffline):
                if datetime.datetime.now(pytz.utc) - datetime.timedelta(
                        days=7) < i.status.was_online:
                    continue
            ll.append((i.username,i.first_name))
    print(f"PARSED {len(ll)} USERS")
    for u in ll:
        us = Username.get_or_none(Username.username == u[0])
        if not us:
            Username(username=u[0],first_name=u[1]).save()
            ADDED += 1
        else:
            DUBL += 1
    print(f"ADDED: {ADDED}\nDUPLICATES: {DUBL}")


with client:
    link = "https://t.me/prooptchat"
    client.loop.run_until_complete(join_and_parse(link))



