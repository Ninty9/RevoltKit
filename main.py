﻿import asyncio
import datetime
import json
import os
import shlex
import shutil
import traceback
from asyncio import sleep
from datetime import timedelta

import pluralkit
import pyvolt
from pluralkit import AutoproxyMode, Unauthorized, ProxyTag
from pyvolt import ReadyEvent, MessageCreateEvent, Message, Client, RelationshipStatus
import emoji
from setuptools.command.alias import alias

path = 'users.txt'
users = list()
prefix = os.getenv("PREFIX", "rk;")

self_bot = False

token = os.getenv("TOKEN")

bot = Client(token=token, bot=True)
help_messages = [""]

class Command:
    def __init__(self, name, description, run, shorthand = False):
        self.name = name
        self.description = description
        self.run = run
        self.shorthand = shorthand
        commandList.append(self)


async def proxy(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run `{prefix}setup.`")
        return
    arg = message.content.removeprefix(f"{prefix}proxy ")
    match arg:
        case "on":
            user['proxy'] = True
            await message.channel.send(content="Messages now be proxied!")
        case "off":
            user['proxy'] = False
            await message.channel.send(content="Messages will no longer be proxied. ):")
        case _:
            if arg == f"{prefix}proxy":
                if user['proxy']:
                    await message.channel.send(content=f"Proxying is currently turned **on**. To change this, run `{prefix}proxy off`.")
                    return
                else:
                    await message.channel.send(content=f"Proxying is currently turned **off**. To change this, run `{prefix}proxy on`.")
                    return
            else:
                await message.channel.send(content=f"Incorrect argument, use `{prefix}proxy [on/off]`")


async def remove(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}remove ")
    if arg == "confirm":
        users.remove(user)
        await message.channel.send(content="Removed you from my database! Thanks for using my services ^^")
    else:
        await message.channel.send(content=f"Are you sure? type `{prefix}remove confirm` to confirm")


async def error(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}error ")
    match arg:
        case "on":
            user['error'] = True
            await message.channel.send(content="Errors will now be displayed.")
        case "off":
            user['error'] = False
            await message.channel.send(content="Errors will no longer be displayed.")
        case _:
            if arg == f"{prefix}error":
                if user['error']:
                    await message.channel.send(content=f"Errors will currently be displayed. To change this, run {prefix}error off.")
                    return
                else:
                    await message.channel.send(content=f"Errors will not be displayed. To change this, run {prefix}error on.")
                    return
            else:
                await message.channel.send(content=f"Incorrect argument, use {prefix}error [on/off]")


async def case(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}case ")
    match arg:
        case "on":
            user['case'] = True
            await message.channel.send(content="Proxies are now case sensitive.")
        case "off":
            user['case'] = False
            await message.channel.send(content="Proxies are no longer case sensitive.")
        case _:
            if arg == f"{prefix}case":
                if user['case']:
                    await message.channel.send(content=f"Proxies are currently case sensitive. To change this, run `{prefix}case off`")
                    return
                else:
                    await message.channel.send(content=f"Proxies are not case sensitive. To change this, run `{prefix}case on`")
                    return
            else:
                await message.channel.send(content=f"Incorrect argument, use {prefix}case [on/off]")


async def setup(message: Message):
    # todo
    await message.channel.send(content="""Use `rk;id [SystemID or Discord ID]` to tell RevoltKit who you are! (Note: To obtain your Discord account ID, you'll need to enable Discord's Developer Mode. This is *not* your Discord username!)
(**OPTIONAL** if your **members, proxies, and front** are **public!**) Use `rk;auth [PluralKitToken]` if you've got private information, or RevoltKit won't be able to proxy properly.
Finally, to complete setup, use `rk;fetch`! After this first time, every time you update your information on PluralKit (such as proxy tags or members), you'll have to run it again to update it on RevoltKit. It doesn't update automatically.""")

async def explain(message: Message):
    # todo
    await message.channel.send(content="""Hi, I'm RevoltKit! I'm a bot that lets you use the PluralKit API to proxy as yourself in Revolt, using Revolt's Masquerade functionality! ^^
Both PluralKit and I function very similarly; we both check your messages to see if they match a pattern you've set, and re-send the message with the associated name, profile picture and color!

This is useful for folk who're multiple people in one body (aka systems). people who wanna roleplay without the hassle of swapping accounts all the time, or... any other reason you'd wanna have multiple identities without multiple accounts, really.

Due to Revolt limitations, proxied messages will show up with the `[BRIDGE]` tag; there's still definitely a person behind it, though! ^^;""")
    
async def support(message: Message):
    # todo
    await message.channel.send(content="""You can find my support server [here](https://rvlt.gg/ReTf1nbS)!""")

async def permcheck(message: Message):
    # todo
    await message.channel.send(content="""**Please note: I have no way of knowing whether I'm missing permissions!** Please manually check if I have the permissions I need!
__**Required**__:
- Manage Messages (to delete messages after I've proxied them)
- Masquerade (to proxy at all)
- View Channel & Send Messages in whatever channel you want me to be in
                               
**Recommended**:
- Manage Roles (to have different member colors)
- Send Embeds & Upload Attachments (to proxy attachments)""")


async def auth(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}auth ")
    if arg != f"{prefix}auth":
        user['token'] = arg
        await message.channel.send(content="Token set!")
    else:
        user['token'] = None
        await message.channel.send(content="Token removed.")


async def id_command(message: Message):
    arg = message.content.removeprefix(f"{prefix}id ")
    if arg == f"{prefix}id":
        await message.channel.send(content=f"You need to add an id, {prefix}id [id]")
        return
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        users.append({'did': arg, 'rid': message.author.id, 'members': [], 'token': None, 'error': True, 'proxy': True, 'case': False, 'auto': [], 'latch': False})
        await message.channel.send(content=f"Set id to {arg}! \nPlease use {prefix}fetch so I can find your proxy tags. If you want me to be able to access private members too, run {prefix}auth with your token! I don't edit your members, but this is still a security risk.")
    else:
        user['did'] = arg
        await message.channel.send(content=f"Set id to {arg}!")


async def fetch(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    members = []
    error = False
    try:
        async for member in pluralkit.Client(user['token'], user_agent="ninty0808@gmail.com").get_members(user['did']):
            try:
                if not member.proxy_tags:
                    continue
                if len(member.proxy_tags.json()) == 0:
                    continue
                members.append({'id': member.id.uuid, 'proxies': member.proxy_tags.json(), 'name': member.name})
            except:
                error = True
    except Exception as e:
        if user['error']:
            await message.channel.send(content=f"""There was an issue when getting your member list, I won't be able to proxy any messages!
                Please use `{prefix}auth [token]` if you want me to be able to access your privated member list, or `{prefix}error off` to turn messages like these off.
                **If you have your token set and are still seeing this please try to contact support** (`rk;support`)**, here is your error message:\n"""+str(e))
        return
    
    user['members'] = members
    await message.channel.send(content=f"PK info updated!")


async def auto(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}auto ")
    if type(message.channel) is not pyvolt.TextChannel:
        sid = message.channel.id
    else:
        sid = message.channel.server_id
        autoproxy = next((x for x in user['auto'] if x['server'] == sid), None)
    if arg == f"{prefix}auto":
        if autoproxy is None:
            user['auto'].append({'mode': AutoproxyMode.OFF.value, 'server':sid})
            autoproxy = next((x for x in user['auto'] if x['server'] == sid), None)
        await message.channel.send(content=f"Your current autoproxy mode is **{autoproxy['mode']}**.")
        return
    if autoproxy is not None:
        user['auto'].remove(autoproxy)
    match arg:
        case AutoproxyMode.OFF.value:
            user['auto'].append({'mode': AutoproxyMode.OFF.value, 'server':sid})
            await message.channel.send(content="Will no longer autoproxy in this server.")
        case AutoproxyMode.FRONT.value:
            user['auto'].append({'mode': AutoproxyMode.FRONT.value, 'server':sid})
            await message.channel.send(content="Will autoproxy with your front in this server.")
        case AutoproxyMode.LATCH.value:
            user['auto'].append({'mode': AutoproxyMode.LATCH.value, 'server': sid})
            await message.channel.send(content="Will autoproxy with latch in this server. (note: current latch is global)")
        case _:
            await message.channel.send(content=f"Incorrect argument, use {prefix}auto [off/front/latch]")


async def help_command(message: Message):
    for m in help_messages:
        await message.channel.send(content=m.removesuffix("\n"))
        await sleep(0.5)

async def switch_move(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}switch move ")
    if arg == f"{prefix}switch move":
        await message.channel.send(content=f":x: No time specified, move cancelled")
        return
    client = pluralkit.Client(user['token'], user_agent="ninty0808@gmail.com")
    minutes=0
    hours=0
    days=0
    for a in shlex.split(arg):
        if a.endswith("m"):
            minutes = int(a.removesuffix("m"))
            continue
        if a.endswith("h"):
            hours = int(a.removesuffix("h"))
            continue
        if a.endswith("d"):
            days = int(a.removesuffix("d"))
            continue
    time = timedelta(days=days, hours=hours, minutes=minutes)
    if time.total_seconds() == 0:
        await message.channel.send(content=":x: I can't move a switch to nowhere... Please give a time that isn't 0!")
        return

    switch1, switch2 = None, None
    try:
        async for s in client.get_switches(system=user['did'], limit=2):
            if switch1 is None:
                switch1 = s
            elif switch2 is None:
                switch2 = s
            else:
                break
        newtime = switch1.timestamp.datetime - time
        if switch2 is None:
            await message.channel.send(content=":x: I can't move your only switch registered!")
            return
        timestring = newtime.strftime("%H:%M:%S %b %d %Y")
        if newtime < switch2.timestamp.datetime:
            await message.channel.send(content=":x: Can't move your switch before your previous switch, as this would cause conflicts!")
            return
        await client.update_switch(switch=switch1.id, timestamp=newtime)
        await message.channel.send(content=f":white_check_mark: Switch moved to {timestring}")
        # todo?: actually add the time in
    except Unauthorized:
        if user['error']:
            await message.channel.send(content=f":x: I'm not authorised to do this. If you want to do this, use `{prefix}auth` with your token to authorise me and try again.")

async def switch_delete(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return

    client = pluralkit.Client(user['token'], user_agent="ninty0808@gmail.com")
    try:
        async for s in client.get_switches(system=user['did'], limit=1):
            await client.delete_switch(s.id)
            await message.channel.send(content=":white_check_mark: Switch deleted!")
            return
    except Unauthorized:
        if user['error']:
            await message.channel.send(content=f":x: I'm not authorised to do this. If you want to do this, use `{prefix}auth` with your token to authorise me and try again.")
    #todo: no switch found


async def switch_edit(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}switch edit ")
    if arg == f"{prefix}switch edit":
        await message.channel.send(content=f":x: You need to add a member!")
        return
    client = pluralkit.Client(user['token'], user_agent="ninty0808@gmail.com")
    mems = []
    for a in shlex.split(arg):
        mem = next((x for x in user['members'] if x['name'].lower() == a.lower()), None)
        if mem is None:
            mems.append(pluralkit.MemberId(id=a))
        else:
            mems.append(pluralkit.MemberId(uuid=mem['id']))
    try:
        async for s in client.get_switches(system=user['did'], limit=1):
            await client.update_switch(switch=s.id, members=mems)
            await message.channel.send(content=":white_check_mark: Switch logged!")
            return
    except Unauthorized:
        if user['error']:
            await message.channel.send(content=":x: I'm not authorised to do this. If you want to do this, use `{prefix}auth` with your token to authorise me and try again.")
    # todo: no switches found?
    return

async def switch_out(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    client = pluralkit.Client(user['token'], user_agent="ninty0808@gmail.com")
    try:
        await client.new_switch()
        await message.channel.send(content=":white_check_mark: Successfully switched out!")
    except Exception as e:
        await message.channel.send(content=":x: There was an error while switching:\n - " + str(e))


async def switch(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        await message.channel.send(content=f":x: I don't have you in my database; please run {prefix}setup.")
        return
    arg = message.content.removeprefix(f"{prefix}switch ")
    if arg == f"{prefix}switch":
        await message.channel.send(content=f":x: No member found to switch to.")
        return
    client = pluralkit.Client(user['token'], user_agent="ninty0808@gmail.com")
    mems = []
    for a in shlex.split(arg):
        mem = next((x for x in user['members'] if x['name'].lower() == a.lower()), None)
        if mem is None:
            mems.append(pluralkit.MemberId(id=a))
        else:
            mems.append(pluralkit.MemberId(uuid=mem['id']))
    try:
        await client.new_switch(*mems)
    except Exception as e:
        await message.channel.send(content=":x: There was an error while switching:\n - " + str(e))
        return
    #done?: words
    await message.channel.send(content=":white_check_mark: Successfully switched!")
    
    return

commandList: list[Command] = list()

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
    except:
        print("failure loading data, making backup of file")
        shutil.copy(path, path.removesuffix(".txt") + "backup" + str(datetime.datetime.date(datetime.datetime.now())) + ".txt")
    asyncio.create_task(save())
    Command(name="explain", description=f"usage: {prefix}explain | A short explanation of RevoltKit", run=explain)
    Command(name="permcheck", description=f"usage: {prefix}permcheck | Check what permissions RevoltKit needs\n> RevoltKit cannot actually check what permissions it needs due to issues outside of our control. For now, RevoltKit will tell you which permissions it *should* have, but server admins will need to manually check whether it actually has them.", run=permcheck)
    Command(name="setup", description=f"usage: {prefix}setup | A quick setup guide for RevoltKit", run=setup)
    Command(name="id", description=f"usage: {prefix}id [pk system id/discord id] | Set your PluralKit system ID or your Discord account ID, so RevoltKit can know who you are\n> Note that if you have private information, you may need to additionally run {prefix}auth", run=id_command)
    Command(name="auth", description=f"usage: {prefix}auth [token] | Give RevoltKit authorization to view private information and log switches", run=auth)
    Command(name="fetch", description=f"usage: {prefix}fetch | Tell RevoltKit to update your PluralKit information", run=fetch)
    Command(name="support", description=f"usage: {prefix}support | Link to [our support server](https://rvlt.gg/ReTf1nbS)\n", run=support)
    Command(name="proxy", description=f"usage: {prefix}proxy [on/off] | Turn proxying on or off globally", run=proxy)
    Command(name="remove", description=f"usage: {prefix}remove | Make RevoltKit forget everything it knows about you", run=remove)
    Command(name="error", description=f"usage: {prefix}error | Toggle error messages (such as authorization issues)", run=error)
    Command(name="help", description=f"usage: {prefix}help | You're looking at it right now!", run=help_command)
    Command(name="switch out", description=f"sw out", run=switch_out, shorthand=True)
    Command(name="switch move", description=f"sw move", run=switch_move, shorthand=True)
    Command(name="switch edit", description=f"sw edit", run=switch_edit, shorthand=True)
    Command(name="switch delete", description=f"sw delete", run=switch_delete, shorthand=True)
    Command(name="switch", description=f"usage: {prefix}switch [name] | Log a new switch with the specified members (Requires Auth)\nusage: {prefix}switch move 1d 6h 3m | Move a switch to some time ago (Requires Auth)\nusage: {prefix}switch edit | Edit your current switch (Requires Auth)\nusage: {prefix}switch delete | Delete your current switch (Requires Auth)", run=switch)
    Command(name="case", description=f"usage: {prefix}case | Toggle your proxy's case sensitivity", run=case)
    Command(name="autoproxy", description=f"usage: {prefix}auto [front/latch] | Set your autoproxy state per-server\n> Front mode will automatically use the first current fronter, while Latch mode will proxy as whoever proxied last *anywhere on Revolt*", run=auto)
    Command(name="auto", description="ap shorthand", run=auto, shorthand=True)
    Command(name="ap", description="ap shorthand", run=auto, shorthand=True)
    Command(name="sw out", description=f"sw out", run=switch_out, shorthand=True)
    Command(name="sw move", description="switch shorthand", run=switch_move, shorthand=True)
    Command(name="sw edit", description="switch shorthand", run=switch_edit, shorthand=True)
    Command(name="sw delete", description="switch shorthand", run=switch_delete, shorthand=True)
    Command(name="sw", description="switch shorthand", run=switch, shorthand=True)

    index = 0
    for command in commandList:
        if command.shorthand:
            continue
        help_messages[index] += "**" + command.name + "**\n" + command.description + "\n"
        if command.description.endswith("\n") or len(help_messages[index]) > 1500:
            index += 1
            help_messages.append("")

    print('Logged on as', bot.me)
    await bot.me.edit(status=pyvolt.UserStatusEdit(text="Use " + prefix + "setup to get started!", presence=pyvolt.Presence.online))


@bot.on(MessageCreateEvent)
async def on_message(event: MessageCreateEvent):
    message = event.message

    # don't respond to ourselves/others
    if (message.author.relationship is RelationshipStatus.user) ^ self_bot:
        return
    if message.author.bot:
        return

    if message.content.startswith(prefix):
        for command in commandList:
            if message.content.startswith(prefix+command.name):
                await command.run(message)
                return
        await message.channel.send(content=message.content.split()[0] + " is not a valid command; please use rk;help to double-check my commands.")
        return

    # todo: nameformat command

    # todo: case sensitivity
    # add a command to toggle it and if its true just convert the message to lowercase (only when checking proxy) and then als
    try:
        await send(message)
    except Exception as e:
        traceback.print_exc()
        await message.channel.send(content="**Encountered an error while sending message:**\n - " + str(e.__class__) + ": " + str(e) + "\nThis could either be a permissions issue or an issue with this bot.")

async def send(message: Message):
    user = next((x for x in users if x['rid'] == message.author.id), None)
    if user is None:
        return
    if not user['proxy']:
        return

    if message.content.startswith("\\"):
        user['latch'] = False
        return
    client = pluralkit.Client(token=user['token'], user_agent="ninty0808@gmail.com")
    proxier = None
    content = message.content

    try:
        for member in user['members']:
            if proxier is not None:
                break
            for proxy in member['proxies']:
                pre = proxy['prefix']
                suf = proxy['suffix']
                check = message.content
                if not user['case']:
                    if pre is not None:
                        pre = pre.lower()
                    if suf is not None:
                        suf = suf.lower()
                    check = check.lower()
                pt = ProxyTag(pre, suf)
                if pt(check):
                    user['latch'] = True
                    proxier = await client.get_member(member['id'])
                    user['members'].insert(0, user['members'].pop(user['members'].index(member)))
                    if pt.prefix is not None:
                        content = remove_prefix_ci(content, pre)
                    if pt.suffix is not None:
                        content = remove_suffix_ci(content, suf)
                    break

        if proxier is None:
            check = message.content
            newcheck = emoji.emojize(check, language='alias')
            if check != newcheck:
                check = newcheck
                if not user['case']:
                    check = check.lower()
                for member in user['members']:
                    if proxier is not None:
                        break
                    for proxy in member['proxies']:
                        pre = proxy['prefix']
                        suf = proxy['suffix']

                        if not user['case']:
                            if pre is not None:
                                pre = pre.lower()
                            if suf is not None:
                                suf = suf.lower()
                        pt = ProxyTag(pre, suf)
                        if pt(check):
                            user['latch'] = True
                            proxier = await client.get_member(member['id'])
                            user['members'].insert(0, user['members'].pop(user['members'].index(member)))
                            if pt.prefix is not None:
                                content = remove_prefix_ci(emoji.emojize(content, language='alias'), pre)
                            if pt.suffix is not None:
                                content = remove_suffix_ci(emoji.emojize(content, language='alias'), suf)
                            break

        if proxier is None:
            if type(message.channel) is not pyvolt.TextChannel:
                sid = message.channel.id
            else:
                sid = message.channel.server_id
            auto = next((x for x in user['auto'] if x['server'] == sid), None)
            if auto is None:
                return
            match auto['mode']:
                case AutoproxyMode.OFF.value:
                    return
                case AutoproxyMode.FRONT.value:
                    async for member in client.get_fronters(user['did']):
                        proxier = member
                        break
                case AutoproxyMode.LATCH.value:
                    for member in user['members']:
                        proxier = await client.get_member(member['id'])
                        break

    except Unauthorized:
        if user['error']:
            await message.channel.send(content=f""":warning: I'm not authorised to access this member or your current fronters!
Use {prefix}auth [token] to set your token or {prefix}error off to turn messages like this off.""")

    if proxier is None:
        return

    name = proxier.display_name
    if name is None:
        name = proxier.name

    manage = True
    try:
        if type(message.channel) is not pyvolt.GroupChannel:
            await bot.http.edit_role(server=message.channel.server.id, role="00000000000000000000000000")
        else:
            manage = False
    except pyvolt.Forbidden:
        manage = False
    except pyvolt.NotFound:
        _ = ""
    color = None
    if proxier.color is not None and manage:
        color = "#" + proxier.color.json()

    system = await client.get_system(proxier.system.id)
    tag = system.tag
    if tag is None:
        tag = ""
    cutoffpostfix = "..."
    reqlen = 32 - (len(tag)+len(cutoffpostfix)+1)
    if len(name) > reqlen:
        name = name[:reqlen]+cutoffpostfix
    if tag is not None:
        name += f" {tag}"

    avatar = proxier.avatar_url
    if proxier.webhook_avatar_url is not None:
        avatar = proxier.webhook_avatar_url

    try:
        if avatar is None:
            avatar = (await client.get_system(user['did'])).avatar_url
    except Unauthorized:
        _ = ""
    if avatar is None:
        avatar = "https://as2.ftcdn.net/jpg/00/64/67/63/1000_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.webp"
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


def remove_prefix_ci(s: str, prefix: str) -> str:
    if s.lower().startswith(prefix.lower()):
        return s[len(prefix):]
    return s

def remove_suffix_ci(s: str, suffix: str) -> str:
    if s.lower().endswith(suffix.lower()):
        return s[:-len(suffix)]
    return s

async def save():
    while True:
        await asyncio.sleep(10)
        with open(path, 'w') as file:
            # Serialize and write the variable to the file
            file.write(json.dumps(users))


bot.run()
