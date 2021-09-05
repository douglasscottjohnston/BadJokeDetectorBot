import discord
import discord.ext
from discord.ext import commands
from discord.ext.commands import Greedy
import os
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-',intents=intents)

# for debugging the databases, uncomment to delete all the keys
# del db["jokes"]
# del db["responses"]
# del db["whitelist"]

#Global variables
if "jokes" not in db.keys():
  db["jokes"] = ["your mom", "Your mom", "You're mom","you're mom", "ur mom", "Ur mom", "urmom", "your mum", "Your mum", "You're mum","you're mum", "ur mum", "Ur mum", "urmum", "69", "deez nuts", "dez nuts", "dz nuts", "deeznuts", "deznuts", "dznuts"]

if "responses" not in db.keys():
  db["responses"] = [
  "This article might help you: https://www.wikihow.com/Write-a-Good-Joke",
  "Your career in comedy is looking bleak",
  "He'll be here all week folks"
  ]

if "whitelist" not in db.keys():
  db["whitelist"] = []
  print(db["whitelist"])

if "responding" not in db.keys():
  db["responding"] = True
  print("Bot is responding")

jokes = db["jokes"].value
responses = db["responses"].value
wlist = db["whitelist"].value
responding = db["responding"]



#Commands
@bot.command(name = "addJoke", description = "Adds a joke to the list of cached jokes, jokes are case insensitive")
@commands.has_permissions(administrator=True)
async def addJoke(ctx, *, message):
  message = message.lower()
  print("command caught")
  if message in jokes:
    await ctx.send(message + " is already in the list of bad jokes")
    return
  else:
    jokes.append(message)
    db["jokes"].value = jokes
    print('The bad joke \"' + message + '\" has been added to the list of bad jokes')
    await ctx.send('The bad joke \"' + message + '\" has been added to the list of bad jokes')
  #debug
  print(db.keys())
  print(db["jokes"])

@bot.command(name = "addResponse", description = "Adds a response to the list of cached responses")
@commands.has_permissions(administrator=True)
async def addResponse(ctx, *, message):
  if message in responses:
    await ctx.send(message + " is already in the list of responses")
    return
  else:
    responses.append(message)
    db["responses"].value = responses
    print('The resonse \"' + message + '\" has been added to the list of responses')
    await ctx.send('The resonse \"' + message + '\" has been added to the list of responses')
  #debug
  print(db.keys())
  print(db["responses"])

@bot.command(name = "clearJokes", description = "Clears the entire list of cached jokes")
@commands.has_permissions(administrator=True)
async def clearJokes(ctx):
  db["jokes"].value.clear()
  print(db["jokes"])
  await ctx.send("Jokes cleared from memory")

@bot.command(name = "clearResponses", description = "Clears the entire list of cached jokes")
@commands.has_permissions(administrator=True)
async def clearResponses(ctx):
  db["responses"].value.clear()
  print(db["responses"])
  await ctx.send("Responses cleared from memory")

@bot.command(name = "removeJoke", description = "Removes the specific joke from the list of cached jokes")
@commands.has_permissions(administrator=True)
async def removeJoke(ctx, *, message):
  for i in range(len(jokes)):
    if message == jokes[i]:
      del jokes[i]
  db["jokes"].value = jokes
  #debug
  print(jokes)
  print(db["jokes"])

  await ctx.send(message + ' was removed from the list of bad jokes')

@bot.command(name = "removeResponse", description = "Removes the specific response from the list of cached responses")
@commands.has_permissions(administrator=True)
async def removeResponse(ctx, *, message):
  for i in range(len(responses)):
    if message == responses[i]:
      del responses[i]
  db["responses"].value = responses
  #debug
  print(responses)
  print(db["responses"])

  await ctx.send(message + ' was removed from the list of responses')

@bot.command(name = "listJokes", description = "Lists all of the cached jokes")
@commands.has_permissions(administrator=True)
async def listJokes(ctx):
  await ctx.send("Here's all the bad jokes in memory:\n{}".format(jokes))

@bot.command(name = "listResponses", description = "Lists all of the cached responses")
@commands.has_permissions(administrator=True)
async def listResponses(ctx):
  await ctx.send("Here's all the responses in memory:\n{}".format(responses))

@bot.command(name = "responding", description = "Turns responding for the bot on or off, takes true or false as arguments")
@commands.has_permissions(administrator=True)
async def responding(ctx, args):
  print("command detected")
  if args.lower() == "true":
    responding = True
    db["responding"] = responding
    await ctx.send("Responding is on")
  else:
    responding = False
    db["responding"] = responding
    await ctx.send("Responding is off")

@bot.command(name = "whitelist", description = "Takes memtions of users and adds them to the whitelist")
@commands.has_permissions(administrator=True)
async def whitelist(ctx, *members: commands.Greedy[discord.Member]):
  if not members:
    userFriendly = "" #necissary to make the output readable for the end user because we store the whitelisted users by id
    for user in wlist:
      userFriendly += bot.get_user(user).name + ","
    response = "[" + userFriendly.rstrip(",") + "]" #so that it fits the format of the other command replys
    await ctx.send(response)
  else:
    names = ", ".join(x.name for x in members)
    print(names)
    if any(member in members for member in wlist):
      await ctx.send("{} is already on the whitelist".format(names))
    else:
      for member in members:
        wlist.append(member.id)
      db["whitelist"].value = wlist
      print(db["whitelist"])
      await ctx.send("{} now on the whitelist".format(names))

@bot.command(name = "unwhitelist", description = "takes mentions of users and removes them from the whitelist")
@commands.has_permissions(administrator=True)
async def unwhitelist(ctx, members: commands.Greedy[discord.Member]):
  reply = ""
  for member in members:
    if wlist.count(member.id) > 0:
      reply += "{} removed, ".format(member.name)
      wlist.remove(member.id)
      print(wlist)
    else:
      reply += "{} was not in the whitelist, ".format(member.name)
      print(wlist)
  await ctx.send(reply.rstrip(", "))

#Events
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(Message):
  await bot.process_commands(Message)
  
  if Message.author == bot.user:
    return

  if responding:
    print("looking for bad joke")
    print(Message.author.id)
    if Message.author.id in wlist: #ignores whitelisted users
        print("User whitelisted, ignoring message")
        return
    elif any(word.lower() in Message.content for word in jokes):
      print("BAD JOKE DETECTED!")
      await Message.channel.send(Message.author.mention + " BAD JOKE DETECTED!\n{}".format(random.choice(responses)))
    else:
      print("No bad joke detected")

  
  
  
keep_alive()
bot.run(os.getenv('TOKEN'))