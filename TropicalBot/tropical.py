import discord
from contextlib import redirect_stdout
import textwrap
from discord.ext.commands import bot
from discord.ext import commands
from discord.ext.commands import *
from os import listdir
from os.path import isfile
from os.path import join
import datetime
import asyncio
import time
import random
import youtube_dl
import traceback
import json
import os
import io
import json
import PIL
import requests
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
import unicodedata

TOKEN = "NTEzNDQwODk4NDA3OTg5MjU4.DtJBSA.VPJOeRsf74mXANubjAfqv0IYcLU"

client = commands.Bot(command_prefix="!")
client.remove_command('help')

owners = [
    "481270883701358602"
]

bypass = [
    "382611318827384852",
    "481270883701358602",
    "275959603907264512",
    "424307935590744079"
]

@client.event
async def on_ready():
    print("Ready.")
    await client.change_presence(status=discord.Status.idle, game=discord.Game(name="for !help", type=3))

@client.event
async def on_server_join(server):
    with open("storage.json", "r") as f:
        data = json.load(f)
    if not server.id in data:
        data[server.id] = {}
        data[server.id]["welcome message"] = "Not Set"
        data[server.id]["anti links"] = "disabled"
        data[server.id]["welcome channel"] = "Not Set"
        data[server.id]["muterole"] = "Not Set"
        data[server.id]["logs"] = "Not Set"
        data[server.id]["farewell channel"] = "Not Set"
        data[server.id]["farewell message"] = "Not Set"
        data[server.id]["autorole"] = "Not Set"
        data[server.id]["img welcomer"] = "disabled"
    with open("storage.json", "w") as f:
        json.dump(data,f,indent=4)

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(color=(random.randint(0,0xffffff)))
    embed.add_field(name=":paperclip: | Costum Commands", value="**!cc add <command> <ouput>** - Adds a command, and you can trigger it by doing **!<command name>** \n **!cc delete <command>** - Deletes a command that you said to delete \n **!cc plugins** - Shows all of the avaliable commands you have")
    embed.add_field(name=":gear: | Settings Configs Up", value="**!set welcome <message>** - Set a message when a user joins, Variables: ``{member}`` - Mentions user \n ``{server}`` - Shows current server name \n ``{count}`` - The current server member count \n **!set farewell <message>** - Sets a message when a user leaves, Variables are the same for welcome \n **!set welcomechannel <channel>** - Sets the channel were the welcome and welcome image will go \n **!set farewellchannel <channel>** - Sets the channel were the farewell messages will go \n **!set logs <channel>** - Sets the moderation logs, and the messages go there \n **!set muterole** - There will be a list of roles to choose from, you set the muted role \n **!set autorole** - A list will pop up and you choose from there")
    embed.add_field(name=":tools: | Moderation", value="**!kick @user <reason>** - Kicks the user from the server, with a reason to go with the log message \n **!ban @user <reason>** - Bans the user from the server \n **!mute @user <reason>** - Gives the selected muted role to the user \n **!unmute @user** - Takes away the muted role from the user")
    embed.add_field(name=":trophy: | Enable Features", value="**!enable anti-link** - Enables the anti-link feature, which deletes every link from a user, except from an admin \n **!enable imgwelcome** - Enables the welcome image")
    embed.add_field(name=":package: | Disabling Features", value="**!disable anti-link** - Allows everyone to send links \n **!disable imgwelcomer** - Disables the welcome feature")
    embed.add_field(name=":interrobang: | Blacklist Words", value="**!blacklist add <word>** - Doesn't allow anyone to say this word \n **!blacklist delete <word>** - Deletes a word from the blacklisted words \n **!blacklist words** - Shows the blacklisted words, only for the people who have **Manage Server** permissions")
    embed.add_field(name=":gem: | Others", value="**!settings** - Shows your current configs")
    await client.say(embed=embed)

#Owner Commands 

@client.command(pass_context=True)
async def charinfo(ctx, *, characters: str):
    def to_string(c):
        digit = f'{ord(c):x}'
        name = unicodedata.name(c, 'Name not found.')
        return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'
    msg = '\n'.join(map(to_string, characters))
    if len(msg) > 2000:
        return await client.say('Output too long to display.')
    await client.say(msg)
   
@client.command(pass_context=True, hidden = True, name="eval")
async def _eval(ctx, *, body: str):
    last_result = None
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')
    if ctx.message.author.id == "481270883701358602":
            embed = discord.Embed(title = "running code", color = 0x0080c0)
            embed.add_field(name = "Output", value = f'```\n...\n```')
            m = await client.say(embed = embed)
            env = {
                'bot': client,
                'ctx': ctx,
                '_': last_result
            }
            env.update(globals())
            body = cleanup_code(body)
            stdout = io.StringIO()
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            try:
                exec(to_compile, env)
            except Exception as e:
                embed = discord.Embed(title = "error message", description = "error ocurred", color = 0xff0000)
                embed.add_field(name = "error", value = f'```\n{e.__class__.__name__}: {e}\n```')
                return await client.edit_message(m, embed = embed)
            func = env['func']
            
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                embed = discord.Embed(title = "error message", description = "error ocurred", color = 0xff0000)
                embed.add_field(name = "error", value = f'```\n{value}{traceback.format_exc()}\n```')
                await client.edit_message(m, embed = embed)
            else:
                value = stdout.getvalue()
                
                if ret is None:
                    if value:
                        if len(value) <= 1016:
                            embed = discord.Embed(title = "success message  Success", description = "completed", color = 0x0080c0)
                            embed.add_field(name = ":", value = f'```\n{value}\n```')
                            await client.edit_message(m, embed = embed)
                            pass
                        else:
                            embed = discord.Embed(title = "success message", description = "The function completed successfully", color = 0x0080c0)
                            embed.add_field(name = ":", value = f'```\nsending in file\n```')
                            await client.edit_message(m, embed = embed)
                            with open("out.txt", 'w') as f:
                                f.write(f"{value}")
                                f.close()
                                pass
                            with open("out.txt", 'r') as f:   
                                await client.send_file(ctx.message.channel, f)
                            pass
                    else:
                        embed = discord.Embed(title = "success message", description = "completed", color = 0x0080c0)
                        embed.add_field(name = ":", value = "```\nblank, :(\n```")
                        await client.edit_message(m, embed = embed)
                else:
                    if len(f"{value}{ret}") <= 1016:
                        last_result = ret
                        embed = discord.Embed(title = "success message", description = "completed", color = 0x0080c0)
                        embed.add_field(name = ":", value = f'```\n{value}{ret}\n```')
                        await client.edit_message(m, embed = embed)
                    else:
                        last_result = ret
                        embed = discord.Embed(title = "success message", description = "completed", color = 0x0080c0)
                        embed.add_field(name = ":", value = f'```\nOutput too long to display, sending in file\n```')
                        await client.edit_message(m, embed = embed)
                        with open("out.txt", 'w') as f:
                            f.write(f"{value}{ret}")
                            f.close()
                            pass
                        with open("out.txt", 'r') as f:   
                            await client.send_file(ctx.message.channel, f)
                        pass

@client.group(pass_context=True)
async def cc(ctx):
    if ctx.invoked_subcommand is None:
        await client.say("<:error:506132126610227200> You need to state a command inside the **Costum Command** group.")

@cc.command(pass_context=True)
async def add(ctx, command: str = None, *, output: str = None):
    with open("commands.json", "r") as f:
        cmd = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200> You need **Manage Server** permissions to proceed this command.")
        return
    if command in client.commands:
        await client.say(f"<:error:506132126610227200> **{command}** is already a command!")
        return
    if command is None:
        await client.say(f"<:error:506132126610227200> You need to support a command for me to add.")
        return
    if output is None:
        await client.say("<:error:506132126610227200> You need to add an output.")
        return
    if not server.id in cmd:
        cmd[server.id] = {}
    if server.id in cmd:
        cmd[server.id][command] = output
        embed = discord.Embed(color=0xff00ea)
        embed.add_field(name="<:check:506143689295396874> Added command!", value=f"Command name: {command} \n Command output: {output}")
        await client.say(embed=embed)
    with open("commands.json", "w") as f:
        json.dump(cmd,f,indent=4)

@cc.command(pass_context=True)
async def delete(ctx, command: str = None):
    with open("commands.json", "r") as f:
        cmd = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200> You need **Manage Server** permissions to proceed this command.")
        return
    if command in client.commands:
        await client.say(f"<:error:506132126610227200> **{command}** is already a command!")
        return
    if not command in cmd[server.id].keys():
        await client.say("<:error:506132126610227200> Command not found.")
        return
    if command is None:
        await client.say(f"<:error:506132126610227200> You need to support a command for me to delete.")
        return
    if not server.id in cmd:
        cmd[server.id] = {}
    if server.id in cmd:
        del cmd[server.id][command]
        embed = discord.Embed(color=0xff00ea)
        embed.add_field(name="<:check:506143689295396874> Deleted command!", value=f"Command name: {command}")
        await client.say(embed=embed)
    with open("commands.json", "w") as f:
        json.dump(cmd,f,indent=4)

@cc.command(pass_context=True)
async def plugins(ctx):
    with open("commands.json", "r") as f:
        cc = json.load(f)
    server = ctx.message.server
    if not server.id in cc:
        await client.say("<:error:506132126610227200> No plugins found.")
        return
    formatted = [f"{x+1}. {y}" for x,y in enumerate(cc[server.id].keys())]
    if server.id in cc:
        embed = discord.Embed(color=0xff00ea, title=f"Plugins for {server.name}", description="\n".join(formatted))
        await client.say(embed=embed)

@client.event
async def on_message(message):
    await client.process_commands(message)
    with open("commands.json", "r") as f:
        cc = json.load(f)
    server = message.server
    if not server.id in cc:
        cc[server.id] = {}
    command = message.content[1:]
    output = cc[server.id].get(command)
    if output:
        await client.send_message(message.channel, output)
    with open("storage.json", "r") as f:
        links = json.load(f)
    server = message.server
    author = message.author
    if author.server_permissions.administrator:
        return
    on = links[server.id]["anti links"]
    if on == "disabled":
        return
    if "https://" in message.content:
        await client.delete_message(message)
        await client.send_message(message.channel, f"{author.mention}, This server probits users from using links!")
    if "http://" in message.content:
        await client.delete_message(message)
        await client.send_message(message.channel, f"{author.mention}, This server probits users from using links!")
    with open("word blacklist.json", "r") as f:
        black = json.load(f)
    server = message.server
    author = message.author
    if author.server_permissions.administrator:
        return
    #Make sure it is a variable so it can see if it is in the list
    words = black[server.id]["blacklisted"]
    #Check if it is in the messasge.content or the message
    for word in message.content.split():
      if word in words:
        #Delete the word if in **word** list
        await client.delete_message(message)
        msg = await client.send_message(message.channel, "<:error:506132126610227200> That word is forbidden here!")
        await asyncio.sleep(3)
        await client.delete_message(msg)

#Mod-Logs

@client.group(pass_context=True)
async def set(ctx):
    if not ctx.invoked_subcommand:
        await client.say("**You need to state a settings command.**")

@set.command(pass_context=True)
async def welcome(ctx, *, welcomemsg = None):
    with open("storage.json", "r") as f:
        welcome = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if welcomemsg is None:
        await client.say("<:error:506132126610227200> **You need to state a message for me to set!**")
        return
    if not server.id in welcome:
        welcome[server.id] = {}
    if server.id in welcome:
        welcome[server.id]["welcome message"] = welcomemsg
    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="<:check:506143689295396874> Set welcome!", value=f"{welcomemsg}")
    await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(welcome,f,indent=4)

@set.command(pass_context=True)
async def autorole(ctx):
    with open("storage.json", "r") as f:
        autorole = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: 
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = '\n '.join(roles);
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="Pick any role", value=f"{roles}")
    await client.say(embed=embed)
    msg = await client.wait_for_message(timeout=10, author=author)
    role = discord.utils.get(server.roles, name=msg.content)
    if role is None:
        await client.say("<:error:506132126610227200> **You chose an unknown role! P.S: Copy the role name!**")
        return
    if not server.id in autorole:
        autorole[server.id] = {}
    if server.id in autorole:
        autorole[server.id]["autorole"] = msg.content
        embed = discord.Embed(color=(random.randint(0, 0xffffff)))
        embed.add_field(name="<:check:506143689295396874> Set auto-role!", value=f"{msg.content}")
        await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(autorole,f,indent=4)

@set.command(pass_context=True)
async def muterole(ctx):
    with open("storage.json", "r") as f:
        muterole = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: 
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = '\n '.join(roles);
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="Pick any role", value=f"{roles}")
    await client.say(embed=embed)
    msg = await client.wait_for_message(timeout=10, author=author)
    role = discord.utils.get(server.roles, name=msg.content)
    if role is None:
        await client.say("<:error:506132126610227200> **You chose an unknown role! P.S: Copy the role name!**")
        return
    if not server.id in muterole:
        muterole[server.id] = {}
    if server.id in muterole:
        muterole[server.id]["muterole"] = msg.content
        embed = discord.Embed(color=(random.randint(0, 0xffffff)))
        embed.add_field(name="<:check:506143689295396874> Set mute-role!", value=f"{msg.content}")
        await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(muterole,f,indent=4)


@set.command(pass_context=True)
async def farewell(ctx, *, byemsg = None):
    with open("storage.json", "r") as f:
        bye = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if byemsg is None:
        await client.say("<:error:506132126610227200> **You need to state a message for me to set!**")
        return
    if not server.id in bye:
        bye[server.id] = {}
    if server.id in bye:
        bye[server.id]["farewell message"] = byemsg
    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="<:check:506143689295396874> Set farewell!", value=f"{byemsg}")
    await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(bye,f,indent=4)

@set.command(pass_context=True)
async def welcomechannel(ctx, *, channel = None):
    with open("storage.json", "r") as f:
        wchannel = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if channel is None:
        await client.say("<:error:506132126610227200> **You need to state a channel for me to set!**")
        return
    welchannel = discord.utils.get(server.channels, name=channel)
    if welchannel is None:
        await client.say("<:error:506132126610227200> **You inputted a unknown channel! Try again.**")
        return
    if not server.id in wchannel:
        wchannel[server.id] = {}
    if server.id in wchannel:
        wchannel[server.id]["welcome channel"] = channel
    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="<:check:506143689295396874> Set welcome channel!", value=f"{channel}")
    await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(wchannel,f,indent=4)

@set.command(pass_context=True)
async def logs(ctx, *, channel = None):
    with open("storage.json", "r") as f:
        logs = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if channel is None:
        await client.say("<:error:506132126610227200> **You need to state a channel for me to set!**")
        return
    welchannel = discord.utils.get(server.channels, name=channel)
    if welchannel is None:
        await client.say("<:error:506132126610227200> **You inputted a unknown channel! Try again.**")
        return
    if not server.id in logs:
        logs[server.id] = {}
    if server.id in logs:
        logs[server.id]["logs"] = channel
    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="<:check:506143689295396874> Set logs!", value=f"{channel}")
    await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(logs,f,indent=4)

@set.command(pass_context=True)
async def farewellchannel(ctx, *, channel = None):
    with open("storage.json", "r") as f:
        wchannel = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if channel is None:
        await client.say("<:error:506132126610227200> **You need to state a channel for me to set!**")
        return
    byechannel = discord.utils.get(server.channels, name=channel)
    if byechannel is None:
        await client.say("<:error:506132126610227200> **You inputted a unknown channel! Try again.**")
        return
    if not server.id in wchannel:
        wchannel[server.id] = {}
    if server.id in wchannel:
        wchannel[server.id]["farewell channel"] = channel
    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="<:check:506143689295396874> Set farewell channel!", value=f"{channel}")
    await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(wchannel,f,indent=4)

@client.event
async def on_member_join(member):
    with open("storage.json", "r") as f:
        welcomer = json.load(f)
    server = member.server
    if not server.id in welcomer:
        welcomer[server.id] = {}
    role = welcomer[server.id]["autorole"]
    autorole = discord.utils.get(server.roles, name=role)
    welcomemsg = welcomer[server.id]["welcome message"].format(**{'member': member.mention, 'server': server.name, 'count': server.member_count})
    channel = welcomer[server.id]["welcome channel"]
    wchannel = discord.utils.get(server.channels, name=channel)
    imgwelcome = welcomer[server.id]
    if imgwelcome == "disabled":
        return
    if welcomemsg == "Not Set":
        return
    if role == "Not Set":
        return
    await client.send_message(wchannel, welcomemsg)
    url = member.avatar_url
    basewidth = 190

    if not url:
        url = member.default_avatar_url
    response = requests.get(url)
    background = Image.open(BytesIO(response.content)).convert("RGBA")
    foreground = Image.open(f"welcome.png").convert("RGBA")
    wpercent = (basewidth / float(background.size[0]))
    hsize = int((float(background.size[1]) * float(wpercent)))
    final = background.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    bg = Image.new("RGBA", foreground.size)
    bg.paste(final, (207, 0), final)
    bg.paste(foreground, (0,0), foreground)
    font_type = ImageFont.truetype('Calligraffitti-Regular.ttf', 50)
    draw = ImageDraw.Draw(bg)
    msg=f"{member}"
    w, h = draw.textsize(msg, font=font_type)
    draw.text(((bg.width-w)//2, 207), text=msg, font=font_type)
    bg.save("w.png")
    await client.send_file(wchannel, "w.png")
    await client.add_roles(member, autorole)

@client.event
async def on_member_remove(member):
    with open("storage.json", "r") as f:
        bye = json.load(f)
    server = member.server
    if not server.id in bye:
        bye[server.id] = {}
    byemsg = bye[server.id]["farewell message"].format(**{'member': member, 'server': server.name, 'count': server.member_count})
    channel = bye[server.id]["farewell channel"]
    byechannel = discord.utils.get(server.channels, name=channel)
    if byemsg == "Not Set":
        return
    await client.send_message(byechannel, byemsg)

#Settings

@client.command(pass_context=True)
async def settings(ctx):
    with open("storage.json", "r") as f:
        settings = json.load(f)
    server = ctx.message.server
    if not server.id in settings:
        settings[server.id] = {}
    logging = settings[server.id]["logs"]
    muterole = settings[server.id]["muterole"]
    wchannel = settings[server.id]["welcome channel"]
    fchannel = settings[server.id]["farewell channel"]
    autorole = settings[server.id]["autorole"]
    fmsg = settings[server.id]["farewell message"]
    wmsg = settings[server.id]["welcome message"]
    anti = settings[server.id]["anti links"]
    wimg = settings[server.id]["img welcomer"]

    msgs = f"""
        Welcome Message: {wmsg}

        Farewell Message: {fmsg}

        Welcome Image: {wimg}
    """

    channels = f"""
        Welcome Channel: {wchannel}

        Farewell Channel: {fchannel}

        Logging channel: {logging}

    """

    automod = f"""

        Anti-Links: {anti}

        Muted Role: {muterole}

        Auto Role:{autorole}

    """

    embed = discord.Embed(color=(random.randint(0, 0xffffff)))
    embed.add_field(name="Configed Messages", value=msgs, inline=False)
    embed.add_field(name="Configed Channels", value=channels, inline=False)
    embed.add_field(name="Auto-Mod", value=automod, inline=False)
    await client.say(embed=embed)

    

#Enable Commands

@client.group(pass_context=True)
async def enable(ctx):
    if not ctx.invoked_subcommand:
        await client.say("**You need something to enable!**")

@enable.command(pass_context=True, name="anti-link")
async def link(ctx):
    with open("storage.json", "r") as f:
        links = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if not server.id in links:
        links[server.id] = {}
    if server.id in links:
        links[server.id]["anti links"] = "enabled"
        embed = discord.Embed(color=(random.randint(0, 0xffffff)))
        embed.add_field(name="<:check:506143689295396874> Enabled anti-links", value="You have currently enabled Anti-Link! This will prohibit the content of **https://** and **http://**")
        await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(links,f,indent=4)

@enable.command(pass_context=True)
async def imgwelcomer(ctx):
    with open("storage.json", "r") as f:
        welcomer = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if not server.id in welcomer:
        welcomer[server.id] = {}
    if server.id in welcomer:
        welcomer[server.id]["img welcomer"] = "enabled"
        embed = discord.Embed(color=(random.randint(0, 0xffffff)))
        embed.add_field(name="<:check:506143689295396874> Enabled Image Welcomer", value="A image with the users name and a welcome message will be shown on an image, when the user joins!")
        await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(welcomer,f,indent=4)


#Disable Commands
@client.group(pass_context=True)
async def disable(ctx):
    if not ctx.invoked_subcommand:
        await client.say("**You need something to disable!**")

@disable.command(pass_context=True, name="anti-link")
async def link(ctx):
    with open("storage.json", "r") as f:
        links = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``Manage Server`` permissions!**")
        return
    if not server.id in links:
        links[server.id] = {}
    if server.id in links:
        links[server.id]["anti links"] = "disabled"
        embed = discord.Embed(color=(random.randint(0, 0xffffff)))
        embed.add_field(name="<:check:506143689295396874> Disabled anti-links", value="Users are aloud to use links!")
        await client.say(embed=embed)
    with open("storage.json", "w") as f:
        json.dump(links,f,indent=4)


#Pil Testing
@client.command(pass_context=True)
async def test(ctx):
        author = ctx.message.author
        basewidth = 190
        url = author.avatar_url
        if not url:
            url = author.default_avatar_url
        response = requests.get(url)
        background = Image.open(BytesIO(response.content)).convert("RGBA")
        foreground = Image.open(f"test.png").convert("RGBA")
        wpercent = (basewidth / float(background.size[0]))
        hsize = int((float(background.size[1]) * float(wpercent)))
        final = background.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        bg = Image.new("RGBA", foreground.size)
        bg.paste(final, (207, 0), final)
        bg.paste(foreground, (0,0), foreground)
        font_type = ImageFont.truetype('Calligraffitti-Regular.ttf', 50)
        draw = ImageDraw.Draw(bg)
        msg=f"{author}"
        w, h = draw.textsize(msg, font=font_type)
        draw.text(((bg.width-w)//2, 207), text=msg, font=font_type)
        bg.save("test1.png")
        embed = discord.Embed(description=":alarm_clock:  **Please wait patiently, I am loading the image!**", color=(random.randint(0, 0xffffff)))
        msg = await client.say(embed=embed)
        await client.send_file(ctx.message.channel, "test1.png")
        await client.delete_message(msg)

#Moderation

@client.command(pass_context=True)
async def kick(ctx, user: discord.Member = None, *, reason = None):
    with open("storage.json", "r") as f:
        kicked = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.kick_members:
        await client.say("<:error:506132126610227200>  **You need ``Kick Members`` permissions!**")
        return
    chan = kicked[server.id]["logs"]
    channel = discord.utils.get(server.channels, name=chan)
    if not server.id in kicked:
        kicked[server.id] = {}
    if user is None:
        await client.say("<:error:506132126610227200> Please specify a user!")
        return
    if chan == "Not Set":
        await client.kick(user)
        await client.say(f"{author}, |<:check:506143689295396874>| **Kicked {user}**")
        return
    if user.server_permissions.administrator:
        await client.say("<:error:506132126610227200> **That user has admin!**")
        return
    if author.roles < user.roles:
        await client.say("You can't kick a person that is over your role!")
        return
    await client.kick(user)
    await client.say(f"{author}, |<:check:506143689295396874>| **Kicked {user}**")
    embed = discord.Embed(color=(random.randint(0,0xffffff)), timestamp=datetime.datetime.utcnow())
    embed.add_field(name=f"{user} Was kicked", value=f"User: ```{user}``` \n Reason: ```{reason}``` \n Moderator/Author: ```{author}```")
    await client.send_message(channel, embed=embed)

@client.command(pass_context=True)
async def ban(ctx, user: discord.Member = None, *, reason = None):
    with open("storage.json", "r") as f:
        kicked = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.ban_members:
        await client.say("<:error:506132126610227200>  **You need ``Ban Members`` permissions!**")
        return
    chan = kicked[server.id]["logs"]
    channel = discord.utils.get(server.channels, name=chan)
    if not server.id in kicked:
        kicked[server.id] = {}
    if user is None:
        await client.say("<:error:506132126610227200> Please specify a user!")
        return
    if chan == "Not Set":
        await client.ban(user)
        await client.say(f"{author}, |<:check:506143689295396874>| **Banned {user}**")
        return
    if user.server_permissions.administrator:
        await client.say("<:error:506132126610227200> **That user has admin!**")
        return
    if author.roles < user.roles:
        await client.say("You can't ban a person that is over your role!")
        return
    await client.kick(user)
    await client.say(f"{author}, |<:check:506143689295396874>| **Banned {user}**")
    embed = discord.Embed(color=(random.randint(0,0xffffff)), timestamp=datetime.datetime.utcnow())
    embed.add_field(name=f"{user} Was banned", value=f"User: ```{user}``` \n Reason: ```{reason}``` \n Moderator/Author: ```{author}```")
    await client.send_message(channel, embed=embed)
    
@client.command(pass_context=True)
async def mute(ctx, user: discord.Member = None, *, reason = None):
    with open("storage.json", "r") as f:
        muted = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.mute_members:
        await client.say("<:error:506132126610227200>  **You need ``Mute Members`` permissions!**")
        return
    mute = muted[server.id]["muterole"]
    mutedrole = discord.utils.get(server.roles, name=mute)
    chan = muted[server.id]["logs"]
    channel = discord.utils.get(server.channels, name=chan)
    if mute == "Not Set":
        await client.say("<:error:506132126610227200> There is no mute role for this server! You can set it by doing: **!set muterole**, it will show you a embed with all of the roles!")
        return
    if chan == "Not Set":
        await client.add_roles(user, mutedrole)
        await client.say(f"{author}, |<:check:506143689295396874>| **Muted {user}**")
        return
    if user is None:
        await client.say("<:error:506132126610227200> Please specify a user!")
        return
    if user.server_permissions.administrator:
        await client.say("<:error:506132126610227200> **That user has admin!**")
        return
    if author.roles < user.roles:
        await client.say("You can't mute a person that is over your role!")
        return
    await client.add_roles(user, mutedrole)
    await client.say(f"{author}, |<:check:506143689295396874>| **Muted {user}**")
    embed = discord.Embed(color=(random.randint(0,0xffffff)), timestamp=datetime.datetime.utcnow())
    embed.add_field(name=f"{user} Was muted", value=f"User: ```{user}``` \n Reason: ```{reason}``` \n Moderator/Author: ```{author}```")
    await client.send_message(channel, embed=embed)

@client.command(pass_context=True)
async def unmute(ctx, user: discord.Member = None):
    with open("storage.json", "r") as f:
        muted = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.mute_members:
        await client.say("<:error:506132126610227200>  **You need ``Mute Members`` permissions!**")
        return
    mute = muted[server.id]["muterole"]
    mutedrole = discord.utils.get(server.roles, name=mute)
    chan = muted[server.id]["logs"]
    channel = discord.utils.get(server.channels, name=chan)
    if mute == "Not Set":
        await client.say("<:error:506132126610227200> There is no mute role for this server! You can set it by doing: **!set muterole**, it will show you a embed with all of the roles!")
        return
    if chan == "Not Set":
        await client.remove_roles(user, mutedrole)
        await client.say(f"{author}, |<:check:506143689295396874>| **Unmuted {user}**")
        return
    if user is None:
        await client.say("<:error:506132126610227200> Please specify a user!")
        return
    if user.server_permissions.administrator:
        await client.say("<:error:506132126610227200> **That user has admin!**")
        return
    await client.remove_roles(user, mutedrole)
    await client.say(f"{author}, |<:check:506143689295396874>| **Unmuted {user}**")
    embed = discord.Embed(color=(random.randint(0,0xffffff)), timestamp=datetime.datetime.utcnow())
    embed.add_field(name=f"{user} Was unmuted", value=f"User: ```{user}``` \nModerator/Author: ```{author}```")
    await client.send_message(channel, embed=embed)


#Black Listing

@client.group(pass_context=True)
async def blacklist(ctx):
    #Check if it is invoked or not
    if not ctx.invoked_subcommand:
        await client.say("You need to have a blackisted word!")

@blacklist.command(pass_context=True)
async def add(ctx, word: str):
    with open("word blacklist.json", "r") as f:
        black = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``BManage Server`` permissions!**")
        return
    #Check if there is a server or not
    if not server.id in black:
        black[server.id] = {"blacklisted": []}
    #Add the blacklist word
    if server.id in black:
        black[server.id]["blacklisted"].append(word)
        embed = discord.Embed(color=(random.randint(0, 0xffffff)), description="<:check:506143689295396874> Added that word.")
        await client.say(embed=embed)
    with open("word blacklist.json", "w") as f:
        json.dump(black,f,indent=4)

@blacklist.command(pass_context=True)
async def delete(ctx, word):
    with open("word blacklist.json", "r") as f:
        black = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``BManage Server`` permissions!**")
        return
    if not server.id in black:
        black[server.id] = {"blacklisted": []}
    if not word in black[server.id]["blacklisted"]:
        await client.say("<:error:506132126610227200> **Word not found!**")
        return
    if server.id in black:
        #Remove the blacklisted word
        black[server.id]["blacklisted"].remove(word)
        embed = discord.Embed(color=(random.randint(0, 0xffffff)), description="<:check:506143689295396874> Deleted the word.")
        await client.say(embed=embed)
    with open("word blacklist.json", "w") as f:
        json.dump(black,f,indent=4)


@blacklist.command(pass_context=True)
async def words(ctx):
    with open("word blacklist.json", "r") as f:
        black = json.load(f)
    server = ctx.message.server
    author = ctx.message.author
    if not author.server_permissions.manage_server:
        await client.say("<:error:506132126610227200>  **You need ``BManage Server`` permissions!**")
        return
    if not black[server.id]["blacklisted"]:
        await client.say("<:error:506132126610227200> **No words found.**")
        return
    formatted = [f"{x+1}. {y}" for x,y in enumerate(black[server.id]["blacklisted"])]
    if server.id in black:
        embed = discord.Embed(color=0xff00ea, title=f"Blacklisted words for {server.name}", description="\n".join(formatted))
        await client.say(embed=embed)
        
client.run(TOKEN)
