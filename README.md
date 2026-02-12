# About RevoltKit
RevoltKit is a [Revolt](https://revolt.chat/) bot that uses the [PluralKit API](https://pluralkit.me/api/) to let you proxy and log switches!

It can:
- proxy messages via autoproxy (front and latch) and via proxy tags in message text the way [PluralKit](https://pluralkit.me/) does on Discord
- run [all the switch related commands that PluralKit can](https://pluralkit.me/commands/#switching-commands)

## Getting Started
This guide is intended for people who are at least somewhat familiar with using PluralKit on Discord and want to use RevoltKit to proxy messages (and/or log switches) on Revolt the way they do on Discord.

### Adding RevoltKit to a Server
Use [this link](https://stoat.chat/bot/01JQQH7BHF02HSVF8KYK1DVF8R) to invite the existing RevoltKit bot to your server. (Proxying and commands in group chats is not yet supported.)

#### Set Up Permissions
Make a new Role for your server and grant it these permissions:
- View Channel: to allow RevoltKit to detect the messages to be proxied
- Send Messages: to allow RevoltKit to send the proxied messages
- Manage Messages: to allow RevoltKit to delete the original message so there aren't duplicates
- Masquerade: to allow RevoltKit to post the new message with the display name of the proxy account
- Send Embeds: to allow RevoltKit to proxy posts with images or other attachments
- Upload Attachments: to allow RevoltKit to proxy posts with attachments
- Manage Roles (optional): to allow RevoltKit to change its role color so that proxied messages match the member's personal color

Be sure to add the RevoltKit bot to that Role as well!

### Using RevoltKit
Use `rk;setup` to get a tutorial (this guide covers the same steps in more detail) and `rk;help` to see the list of commands.

#### Setup
Use `rk;id [SystemID or Discord ID]` to tell RevoltKit who you are;

_Note: Brackets (`[]`) show where to fill in information, so for example if your system ID is `abcdef` then the command would be `rk;id abcdef`_
##### Using a System ID
Your `SystemID` is a five or six letter code that you can get by running the `pk;s id` command on Discord in a DM with the PluralKit bot or in a server that has PluralKit

##### Using a Discord ID
Your `Discord ID` is not the same as your Discord username; to get your Discord User ID number, please follow [the instructions from Discord here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID). (You may need to enable Developer Mode; there are instructions how to do so on that page as well.)

#### Optional: Authorize RevoltKit
If you have members set to private or want to log switches using RevoltKit, you will need to give RevoltKit your PluralKit auth token so it can access that information. (Otherwise, this step is optional.)

To get your PluralKit token, use the command `pk;token` in Discord in a DM with the PluralKit bot or in a server that has PluralKit (if you run it in a server, it will still DM you the token for privacy reasons).

Use `rk;auth [PluralKitToken]` to submit your token to RevoltKit.

_Warning: Be careful when running the command to authorize RevoltKit that you do so somewhere private, or else anyone who can see the command will also be able to access your private information and edit your system data on PluralKit._

#### Fetch Information From PluralKit
Use `rk;fetch` to fetch your information from PluralKit. After this first time, every time you update your system members or proxy tags on PluralKit, you'll have to run it again to update it on RevoltKit. However, if you are using the `front` autoproxy mode (`rk;auto front`) you don't need to run it every time you log a switch on PluralKit.

#### Optional: Set Up Autoproxy
Use `rk;auto [off/front/latch]` to set your autoproxy preferences.

Autoproxy settings work the same way on RevoltKit as they do [on PluralKit](https://pluralkit.me/commands/#autoproxy-commands):
- `rk;auto off  ` - Disables autoproxying for your system in the current server.
- `rk;auto front` - Sets your system's autoproxy in this server to proxy the first member currently registered as front.
- `rk;auto latch` - Sets your system's autoproxy in this server to proxy the last manually proxied member.

##### RevoltKit's Latch Mode
Unlike PluralKit where the last member to proxy in a specific server will be used again when posting in the same server, RevoltKit's `latch` setting currently latches across all of Revolt and has no timeout. You will still need to turn it on in each server, however once the mode is set to `latch` the last proxied member for that mode is tracked across all servers.

#### Optional: Log Switches using RevoltKit
When [authorized to do so](#Optional:Authorize-RevoltKit), RevoltKit can run all of the switch related commands that PluralKit can; [see more info on those here](https://pluralkit.me/commands/#switching-commands). Please note that while all the switch commands are supported, switch flags (such as the `-append` flag in the command `rk;sw edit -append [Name]`) are not supported yet.
