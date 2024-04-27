import discord
import os
import random
import asyncio
from discord import app_commands
from discord.ext import commands, tasks

#INVITE LINK = https://discord.com/api/oauth2/authorize?client_id=1124913708288725002&permissions=268446784&scope=bot%20applications.commands

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

DEFAULTTIMETOWAIT = 10
AUTHORIZEDCHANNELS = [1125967947299573851, 1121308289351831566]

bot = commands.Bot(command_prefix = '$', intents=INTENTS)
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = open(CURRENT_DIRECTORY + "/token.txt")
TOKEN = TOKEN_FILE.read()
TOKEN_FILE.close()

bot.remove_command("help")

@bot.event
async def on_ready():

    #synced = await bot.tree.sync(guild=None)
    print(f"ready")
    for guild in bot.guilds:
        print(guild.name + ":" + str(guild.id))
    sendRandomPicture.start()

@bot.event
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.CommandNotFound):
        await temporaryReply(interaction.message, "Command not recognized", DEFAULTTIMETOWAIT)
    if(isinstance(error, commands.MissingRequiredArgument)):
       await temporaryReply(interaction.message, "Command incomplete", DEFAULTTIMETOWAIT)

#this function handles the creation of a new role. this role must have the initials A.T. [1]
#and there cannot be another role by that name [2]. the role has no permitions but is taggable [3]
#gives the author that role, and deletes original command, only leaving the bot message [4]
@bot.command(name="create")
@app_commands.describe(role = "Enter AT Acronym")
async def create(interaction: discord.Interaction, roleA:str = commands.parameter(description= "Name starting with A"), roleT:str = commands.parameter(description= "Name starting with T")):
    try:
        message = interaction.message
        if(message.channel.id not in AUTHORIZEDCHANNELS):
            await message.delete()
            return
        guild = interaction.guild
        roleA.replace('[', "")
        roleA.replace(']', "")
        roleT.replace('[', "")
        roleT.replace(']', "")

        #[1]
        if(roleA[0].lower() != "a" or roleT[0].lower() != 't'):
            await temporaryReply(message, "This name does not comply with After Thought regulations", DEFAULTTIMETOWAIT)
            return
        newRoleName = buildRoleName(roleA, roleT)

        #[2]
        for role in guild.roles:
            if(newRoleName == role.name):
                await temporaryReply(message, "That group is already in the system records", DEFAULTTIMETOWAIT)
                return

        #[3]
        newRole = await guild.create_role(name=newRoleName, hoist=True, mentionable=True, permissions=discord.Permissions.none(),
                                        color=discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        #[4]
        await message.author.add_roles(newRole)
        await message.channel.send(f"<@{message.author.id}> has founded the group: {newRoleName}")

        await asyncio.sleep(DEFAULTTIMETOWAIT)
        await message.delete()
        return
    except Exception as e:
        temporaryReply(interaction.message, "an error has occured", DEFAULTTIMETOWAIT)
        return

#this function allows people to join a role which is already created
#they cannot join another role if that role has permissions [1]
#they cannot join a role they already have [2]
@bot.command(name="join")
async def join(interaction:discord.Interaction, roleA:str = commands.parameter(description= "Name starting with A",), 
                                                roleT:str = commands.parameter(description= "Name starting with T")):
    try:
        message = interaction.message
        if(message.channel.id not in AUTHORIZEDCHANNELS):
            await message.delete()
            return
        
        roleName = buildRoleName(roleA, roleT)
        role = discord.utils.get(message.guild.roles, name=roleName)

        if(role == None):
            await temporaryReply(message, "This group is not in any records", DEFAULTTIMETOWAIT)
            return
        
        #[1]
        if not(role.permissions == discord.Permissions.none()):
            await temporaryReply(message, "Access denied", DEFAULTTIMETOWAIT)
            return
        
        #[2]
        if(role in message.author.roles):
            await temporaryReply(message, "Records indicate user is already a member of this group", DEFAULTTIMETOWAIT)
            return
        
        await message.author.add_roles(role)
        await permenantReply(message, f" <@{message.author.id}> has joined the ranks of {roleName}", DEFAULTTIMETOWAIT)
        return
    except Exception as e:
            temporaryReply(interaction.message, "an error has occured", DEFAULTTIMETOWAIT)
            return

#this command allows users to leave a role which they've joined
#they cannot leave a role which has permissions, i.e. not created by the bot [1]
#they cannot leave a role they don't have [2]
#if after the user leaves the role is empty, that role is deleted [3]
@bot.command(name="leave")
async def leave(interaction: discord.Interaction, roleA:str = commands.parameter(description= "Name starting with A"), roleT:str = commands.parameter(description= "Name starting with T")):
    try:
        message = interaction.message
        if(message.channel.id not in AUTHORIZEDCHANNELS):
            await message.delete()
            return
        
        roleToLeave = discord.utils.get(message.guild.roles, name = buildRoleName(roleA, roleT))

        if(roleToLeave == None):
            await temporaryReply(message, "This group is not in any records", DEFAULTTIMETOWAIT)
            return
        #[1]
        if not (roleToLeave.permissions == discord.Permissions.none()):
            await temporaryReply(message, "Access denied", DEFAULTTIMETOWAIT)
            return

        #[2]
        if(roleToLeave not in message.author.roles):
            await temporaryReply(message, "Records indicate you are not a member of this group", DEFAULTTIMETOWAIT)
            return
        await message.author.remove_roles(roleToLeave)
        await permenantReply(message, f"<@{message.author.id}> has left {roleToLeave.name}", DEFAULTTIMETOWAIT)

        #[3]
        if(len(roleToLeave.members) == 0):
            await roleToLeave.delete()
        return
    except Exception as e:
        await temporaryReply(interaction.message, "an error has occured", DEFAULTTIMETOWAIT)
        return

#shows the open roles
@bot.command(name="list")
async def list(interaction: discord.Interaction):
    try:
        message = interaction.message
        if(message.channel.id not in AUTHORIZEDCHANNELS):
            await message.delete()
            return
        server = message.guild
        roleList = ""

        for role in server.roles:
            if(checkRole(role)):
                roleList += role.name + "\n"
        if(roleList == ""):
            roleList = "Records indicate no open groups at this time"
            await temporaryReply(interaction.message, roleList, DEFAULTTIMETOWAIT)

        await temporaryReply(interaction.message, "Records show the following open groups:\n"+roleList, 30)
        return
    except Exception as e:
        await temporaryReply(interaction.message, "an error has occured", DEFAULTTIMETOWAIT)
        return

@bot.command(name="help")
async def help(interaction: discord.Interaction):
    message = interaction.message
    if(message.channel.id not in AUTHORIZEDCHANNELS):
        await message.delete()
        return
    text = """This bot is used for creating, joining, and leaving custom groups.
replace [group] with 2 words,
the first beginning with A, and the second beginning with T\n
$help: display this message
$list: show a list of open groups
$create [group]: create a new group. must have the initials A.T.
$join [group]: join an existing group
$leave [group]: leave one of your current groups\n
if a group has no members, it will be automatically deleted."""

    await temporaryReply(message, text, 45)
    return

def checkRole(role:discord.Role):
    names = role.name.split(" ")
    if(len(names) != 2):
        return False
    if(names[0][0] != "A"):
        return False
    if(names[1][0] != "T"):
        return False
    if(role.permissions != discord.Permissions.none()):
        return False
    return True
#responds to user command, and deletes both messages after a set time

async def temporaryReply(originalMessage, replyText, timeToWait):
    replyMessage = await originalMessage.reply(replyText)
    await asyncio.sleep(timeToWait)
    await replyMessage.delete()
    await originalMessage.delete()
    return

async def permenantReply(originalMessage, text, timeToWait):
    await originalMessage.channel.send(text)
    await asyncio.sleep(timeToWait)
    await originalMessage.delete()
    return

#normalizes the input for the role the user wants to create/join/leave.
def buildRoleName(roleA, roleT):
    if(len(roleA) > 1):
        capA = roleA[0].upper() + roleA[1:].lower()
    else:
        capA = roleA[0].upper()
    if(len(roleT) > 1):
        capT = roleT[0].upper() + roleT[1:].lower()
    else:
        capT = roleT[0].upper()
    return capA + " " + capT

@tasks.loop(minutes = 30, count = None)
async def sendRandomPicture():
    #get my server
    basePath = "./AT Bot/Images/"
    server = None
    for guild in bot.guilds:
        if guild.id == 1117516040671342762:
            server = guild
            break

    if server == None:
        return
    
    randomIndex = random.randint(0, len(server.text_channels)-1)
    channel = server.text_channels[randomIndex]
    picturePath = basePath + os.listdir(basePath)[random.randint(0, len(os.listdir(basePath))-1)]
    picture = discord.File(picturePath)
    message = await channel.send(file = picture)
    print(message.channel.name)
    await asyncio.sleep(30)
    await message.delete()

bot.run(TOKEN)