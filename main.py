import asyncio
import json
import os
import shutil

import pluralkit
import pyvolt
from pyvolt import ReadyEvent, MessageCreateEvent, Message, Client, RelationshipStatus


# Whether the example should be ran as a user account or not

path = 'users.txt'
users = list()
prefix = "rk;"

self_bot = False

with open('token.txt', 'r') as file:
    # Serialize and write the variable to the file
    token = file.read()
    print(users)

bot = Client(token=token, bot=True)


@bot.on(ReadyEvent)
async def on_ready(_) -> None:
    global users
    if not os.path.isfile(path):
        with open(path, 'w') as file:
            file.write('')
    try:
        with open(path, 'r') as file:
            # Serialize and write the variable to the file
            users = json.loads(file.read())
            print(users)
    except:
        print("failure loading data, making backup of file")
        shutil.copy(path, path.removesuffix(".txt") + "backup.txt")
    asyncio.create_task(save())
    print('Logged on as', bot.me)


@bot.on(MessageCreateEvent)
async def on_message(event: MessageCreateEvent):
    message = event.message

    # don't respond to ourselves/others
    if (message.author.relationship is RelationshipStatus.user) ^ self_bot:
        return

    if message.content.startswith(prefix+"id"):
        await id(message)
        return
    if message.content.startswith(prefix+"fetch"):
        await fetch(message)
        return
    if message.content.startswith(prefix+"help"):
        await help(message)
        return
    if message.content.startswith(prefix+"proxy"):
        await proxy(message)
        return
    if message.content.startswith(prefix+"auth"):
        await auth(message)
        return
    if message.content.startswith(prefix+"warn"):
        await warn(message)
        return
    if message.content.startswith(prefix+"setup"):
        await setup(message)
        return
    if message.content.startswith(prefix+"remove"):
        await remove(message)
        return
    if message.content.startswith(prefix+"switch delete"):
        # todo: await switch(message)
        return
    if message.content.startswith(prefix+"switch move"):
        # todo: await switch(message)
        return
    if message.content.startswith(prefix+"switch edit"):
        # todo: await switch(message)
        return
    if message.content.startswith(prefix+"switch"):
        # todo: await switch(message)
        return
    # todo: nameformat command

    # todo: case sensitivity
    # add a command to toggle it and if its true just convert the message to lowercase (only when checking proxy) and then als
    if message.content.startswith("\\"):
        return

    await send(message)

async def proxy(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    arg = message.content.removeprefix(f"{prefix}proxy ")
    match arg:
        case "on":
            user['proxy'] = True
            await message.channel.send(content="Messages will now be proxied!")
        case "off":
            user['proxy'] = False
            await message.channel.send(content="Messages will no longer be proxied. ):")
        case _ if arg == f"{prefix}proxy":
            await message.channel.send(content=f"Missing argument, use `{prefix}proxy [on/off]`")

async def remove(message: Message):
    arg = message.content.removeprefix(f"{prefix}warn ")
    if arg == "confirm":
        user = next((x for x in users if x['rid'] == message.author.id), None)
        users.remove(user)
        await message.channel.send(content="I don't even know who you are...")
    else:
        await message.channel.send(content=f"Are you sure? type `{prefix}remove` confirm to confirm")


async def warn(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    arg = message.content.removeprefix(f"{prefix}warn ")
    match arg:
        case "on":
            user['warn'] = True
            await message.channel.send(content="Warnings will now be displayed.")
        case "off":
            user['warn'] = False
            await message.channel.send(content="Warnings will no longer be displayed.")
        case _ if arg == f"{prefix}proxy":
            await message.channel.send(content=f"Missing argument, use {prefix}warn [on/off]")

async def send(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        return
    if not user['proxy']:
        return
    client = pluralkit.Client(token=user['token'], user_agent="ninty0808@gmail.com")
    proxier = None
    content = message.content

    def removeprefix_case_insensitive(s: str, prefix: str) -> str:
        if s.lower().startswith(prefix.lower()):
            return s[len(prefix):]
        return s

    def removesuffix_case_insensitive(s: str, suffix: str) -> str:
        if s.lower().startswith(suffix.lower()):
            return s[:-len(prefix)]
        return s
    try:
        for member in user['members']:
            if proxier is not None:
                break
            for proxy in member['proxies']:
                pt = pluralkit.ProxyTag(prefix=proxy['prefix'], suffix=proxy['suffix'])
                if pt(message.content):
                    proxier = await client.get_member(member['id'])
                    user['members'].insert(0, user['members'].pop(user['members'].index(member)))
                    if pt.prefix is not None:
                        content = content.removeprefix(pt.prefix)
                    if pt.suffix is not None:
                        content = content.removesuffix(pt.suffix)
                    break

        if proxier is None:
            async for member in client.get_fronters(user['did']):
                proxier = member
                break
    except pluralkit.Unauthorized:
        if user['warn']:
            await message.channel.send(content=f"""I'm not authorised to access this member or your fronters!
Use `{prefix}auth [token]` to set your token, or `{prefix}warn off` to turn messages like this off.""")

    if proxier is None:
        return

    name = proxier.display_name
    if name is None:
        name = proxier.name

    message.channel.permissions_for(bot.me).manage_roles
    color = None
    if proxier.color is not None:
        color = "#" + proxier.color.json()

    system = await client.get_system(proxier.system.id)
    tag = system.tag
    cutoffpostfix = "..."
    reqlen = 32 - (len(tag)+len(cutoffpostfix)+1)
    if len(name) > reqlen:
        name = name[:reqlen]+cutoffpostfix
    if tag is not None:
        name += f" {tag}"

    avatar = proxier.avatar_url
    if proxier.webhook_avatar_url is not None:
        avatar = proxier.webhook_avatar_url
    files = [
        (asset.filename,await asset.read())
        for asset in message.attachments
    ]
    await message.channel.send(
        content=content,
        masquerade=pyvolt.MessageMasquerade(name=name[:32], avatar=avatar, color=color),
        replies=message.replies,
        attachments=files,
        silent=message.is_silent()
    )
    await message.delete()

async def help(message: Message):
    #todo
    await message.channel.send(content="""rk;setup - quick guide on how to use the bot
rk;id [sysid | discord id]
rk;fetch - grabs members and proxies, not required if not proxying
rk;help - you're looking at it now!
rk;proxy [ on | off ]
rk;auth (token) - if no argument, forgets your token
rk;warn [ on|off ] - warns you about errors, on by default
rk;switch - switches on pluralkit""")

async def setup(message: Message):
    #todo
    await message.channel.send(content="""Use `rk;id [SystemID or Discord ID]` to tell RevoltKit who you are!
(**OPTIONAL** if your members, proxies, and front are public!) Use `rk;auth [PluralKitToken]` if you've got any private information, or RevoltKit won't be able to proxy.
Finally, to complete setup, use `rk;fetch`! After this first time, every time you update your proxies on PluralKit, you'll have to run it again to update it on RevoltKit. It doesn't update automatically.""")

async def auth(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    arg = message.content.removeprefix(f"{prefix}fetch ")
    if arg != f"{prefix}auth":
        user['token'] = arg
        await message.channel.send(content="Token set!")
    else:
        user['token'] = None
        await message.channel.send(content="Token removed.")


async def id(message: Message):
    arg = message.content.removeprefix(f"{prefix}id ")
    if arg == f"{prefix}id":
        await message.channel.send(content=f"You need to add an id, {prefix}id [id]")
        return
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        users.append({'did': arg, 'rid': message.author.id, 'members': [], 'token': None, 'warn': True, 'proxy': True})
        await message.channel.send(content=f"Set id to {arg}! \nPlease use {prefix}fetch so i can find your proxy, if you want me to be able to access private members also add your token, My code shouldn't contain anything that edits your system, but this is still a security risk!")
    else:
        user['did'] = arg
        await message.channel.send(content=f"Set id to {arg}!")


async def fetch(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    members = []
    warn = False
    async for member in pluralkit.Client(user['token']).get_members(user['did']):
        try:
            if not member.proxy_tags:
                continue
            if len(member.proxy_tags.json()) == 0:
                continue
            members.append({'id': member.id.uuid, 'proxies': member.proxy_tags.json()})
        except:
            nonlocal warn
            warn = True
    user['members'] = members
    if warn and user['warn']:
        await message.channel.send(content=f"""There was an issue getting some of your members, you probably have some private members without having your token set, this is fine though!
        Use {prefix}auth [token] if you want me to be able to access private members, or {prefix}warn off to turn messages like these off.
        If you have your token set and are still seeing this please try to contact support.""")
    else:
        await message.channel.send(content=f"Done!")


async def save():
    while True:
        await asyncio.sleep(10)
        with open(path, 'w') as file:
            # Serialize and write the variable to the file
            file.write(json.dumps(users))


bot.run()