# About RevoltKit
RevoltKit is a [Revolt](https://revolt.chat/) bot that uses the [PluralKit API](https://pluralkit.me/api/) to let you proxy and log switches!

It can:
- proxy messages via autoproxy (front and latch) and via proxy tags in message text the way [PluralKit](https://pluralkit.me/) does on Discord
- run [all the switch related commands that PluralKit can](https://pluralkit.me/commands/#switching-commands)

## Getting Started
This guide is intended for people who are familiar with using PluralKit on Discord and want to use RevoltKit to proxy (and/or log switches) on Revolt the way they do on Discord.

### Adding RevoltKit to a Server
Use [this link](https://app.revolt.chat/bot/01JQQH7BHF02HSVF8KYK1DVF8R) to invite the existing RevoltKit bot to your server. (Proxying and commands in group chats is not yet supported.)

#### Set Up Permissions
Make a new Role for your server and grant it these permissions:
- Manage Roles
- Manage Messages
- Masquerade

Be sure to add the RevoltKit bot to that Role as well!

### Using RevoltKit
Use `rk;setup` to get a tutorial and `rk;help` to see the list of commands.

If you have members set to private or want to log switches using RevoltKit, you'll need to give RevoltKit your PluralKit auth token. To get your PluralKit token, use the command `pk;token` in Discord in a DM with the PluralKit bot or in a server that has PluralKit (if you run it in a server, it will still DM you the token for privacy reasons).
_Warning: Be careful when running the command to authorize RevoltKit that you do so somewhere private, or else anyone who can see the command will also be able to access your private information._

#### Optional: Set Up Autoproxy
Use `rk;auto [off/front/latch]` to set your autoproxy preferences

#### Optional: Log Switches using RevoltKit
RevoltKit can run all of the switch related commands that PluralKit can; [see more info on those here](https://pluralkit.me/commands/#switching-commands)

### Running Your Own Bot
This guide is intended for people with no experience making or running their own bots and want to run a fork of the bot from this repository.

#### 1. Setup
Follow the instructions [here](https://revolt.guide/docs/introduction/creating-a-bot-application) to set up a Revolt bot (and set the Name/Avatar/Description they way you want it), then copy the token for your bot

#### 2. Hosting
Hosting is where your bot's code will live and where it will run from. You can host it locally - on your own computer - or remotely - on a paid server somewhere else. If you host it locally, the bot will need to be running on your computer anytime it is active in the servers it is in. If you host it remotely, it will run on the server anytime the server is online (which is usually 24/7. Either way there may be issues with hosting that take the bot offline and need to be fixed.

##### 2a. Hosting Locally
Follow the instructions [here](https://revolt.guide/docs/introduction/installing-node.js-and-revolt.js) to install node.js and revolt.js on your computer.
- [ ] check that this is actually part of setup for this bot
- [ ] add more info on how to set this up

##### 2a. Hosting Remotely
- [ ] add options for where to host from
- [ ] add more info on how to set this up

#### 3. Adding Your Bot
Follow the instructions [here](https://revolt.guide/docs/introduction/adding-your-bot-to-your-server) to get the bot's invite link, then see [Adding the Bot to a Server or Group](#Adding-the-Bot-to-a-Server-or-Group) above, but use your own link
