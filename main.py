import json
import os
import time
from time import sleep

import pluralkit
import revolt
from pluralkit.v1 import Member
from revolt.ext import  commands
import aiohttp
import asyncio
import pickle
from pluralkit import Client, Unauthorized, ProxyTag
from revolt import Masquerade, WebsiteEmbed, SendableEmbed, MessageReply
from websockets.cli import print_over_input

pk = Client(user_agent="ninty0808@gmail.com");
path = 'users.txt'
users = list()
prefix = "rk;"
class Client(commands.CommandsClient):

    async def get_prefix(self, message: revolt.Message):
        return prefix

    @commands.command()
    async def id(self, ctx: commands.Context):
        arg = ctx.message.content.removeprefix(f"{prefix}id ")
        users.append({'did': arg, 'rid': ctx.author.id, 'members': [], 'token': None})
        await ctx.channel.send(content=f"Set id to {arg}! \nPlease use {prefix}fetch so i can find your proxy, if you want me to be able to access private members also add your token, My code shouldn't contain anything that edits your system, but this is still a security risk!")

    @commands.command()
    async def fetch(self, ctx: commands.Context):
        user = next((x for x in users if x['rid'] == ctx.author.id), None)
        arg = ctx.message.content.removeprefix(f"{prefix}fetch ")
        if arg != f"{prefix}fetch":
            user['token'] = arg
        members = []
        async for member in pluralkit.Client(user['token']).get_members(user['did']):
            try:
                if not member.proxy_tags:
                    continue
                if len(member.proxy_tags.json()) == 0:
                    continue
                members.append({'id': member.id.uuid, 'proxies': member.proxy_tags.json()})
            except:
                print("error in members");
        user['members'] = members
        await ctx.channel.send(content=f"Done!")

    async def on_message(self, message: revolt.Message):
        await commands.CommandsClient.process_commands(self, message)
        if message.content.startswith("rk;"):
            return
        if message.content.startswith("\\"):
            return

        user = next((x for x in users if x['rid'] == message.author.id), None)
        if user is None:
            return
        client = pluralkit.Client(user['token'])
        proxier = None
        content = message.content
        try:
            for member in user['members']:
                if proxier is not None:
                    break
                for proxy in member['proxies']:
                    print(proxy)
                    pt = ProxyTag(prefix=proxy['prefix'], suffix=proxy['suffix'])
                    if pt(message.content):
                        print('found')
                        # proxier = next((x for x in client.get_members() if x.id == member['id']), None)
                        proxier = await client.get_member(member['id'])
                        print("b")
                        user['members'].insert(0,user['members'].pop(user['members'].index(member)))
                        content.removeprefix(proxy['prefix'])
                        content.removesuffix(proxy['suffix'])
                        break

            if proxier is None:
                async for member in client.get_fronters(user['did']):
                    print(member)
                    proxier = member
                    break

        except Unauthorized:
            await message.channel.send(content=f"Unauthorised!")

        if proxier is None:
            return

        name = proxier.display_name
        if name is None:
            name = proxier.name
        e: WebsiteEmbed
        replies: list[MessageReply]
        i = 0
        color = None
        if proxier.color is not None:
            color = "#" + proxier.color.json()
        system = await client.get_system(proxier.system.id)
        tag = system.tag
        if tag is not None:
            name += f" {tag}"
        avatar = proxier.avatar_url
        if proxier.webhook_avatar_url is not None:
            avatar = proxier.webhook_avatar_url
        print(color)

        await message.channel.send(content=message.content,
                                   masquerade=Masquerade(name=name[:32], avatar=avatar, colour=color))
        await message.delete()


async def save():
    while True:
        with open(path, 'w') as file:
            # Serialize and write the variable to the file
            file.write(json.dumps(users))
        await asyncio.sleep(10)

async def main():

    global users
    # if not os.path.isfile(path):
    #     with open(path, 'w') as file:
    #         file.write('')
    try:
        with open(path, 'r') as file:
            # Serialize and write the variable to the file
            users = json.loads(file)
    except:
        print("test")

    print(users)
    asyncio.create_task(save())

    async with aiohttp.ClientSession() as session:
        client = Client(session, "oJVKA1bGSVxkxWzVsw0uguHs6saG6S-BdgRst9nYPr5AmhjufHb9x86r2tkB9KGd")
        await client.start()


asyncio.run(main())




