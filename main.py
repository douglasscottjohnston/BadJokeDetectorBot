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
@bot.command()
async def addJoke(ctx, message):
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

@bot.command()
async def addResponse(ctx, message):
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

@bot.command()
async def clearJokes(ctx):
  db["jokes"].value.clear()
  print(db["jokes"])
  await ctx.send("Jokes cleared from memory")

@bot.command()
async def clearResponses(ctx):
  db["responses"].value.clear()
  print(db["responses"])
  await ctx.send("Responses cleared from memory")

@bot.command()
async def removeJoke(ctx, message):
  for i in range(len(jokes)):
    if message == jokes[i]:
      del jokes[i]
  db["jokes"].value = jokes
  #debug
  print(jokes)
  print(db["jokes"])

  await ctx.send(message + ' was removed from the list of bad jokes')

@bot.command()
async def removeResponse(ctx, message):
  for i in range(len(responses)):
    if message == responses[i]:
      del responses[i]
  db["responses"].value = responses
  #debug
  print(responses)
  print(db["responses"])

  await ctx.send(message + ' was removed from the list of bad jokes')

@bot.command()
async def listJokes(ctx):
  await ctx.send("Here's all the bad jokes in memory:\n{}".format(jokes))

@bot.command()
async def listResponses(ctx):
  await ctx.send("Here's all the responses in memory:\n{}".format(responses))

@bot.command()
async def responding(ctx, args):
  print("command detected")
  if args:
    responding = True
    db["responding"] = responding
    await ctx.send("Responding is on")
  else:
    responding = False
    db["responding"] = responding
    await ctx.send("Responding is off")

@bot.command()
async def whitelist(ctx, *members: commands.Greedy[discord.Member]):
  if not members:
    print(wlist)
    await ctx.send(wlist)
  else:
    if any(x.name in members for x in wlist):
      print(wlist)
      await ctx.send("{} is already on the whitelist".format(ctx.mentions[0]))
    else:
      wlist.append(n.name for n in members)
      db["whitelist"].value = wlist
      print(db["whitelist"])
      await ctx.send("{} now on the whitelist".format(members))

@bot.command()
async def unwhitelist(ctx, args):
    if args in wlist:
      wlist.remove(args)
      db["whitelist"].value = wlist
      #debug
      print(wlist)
      print(db["whitelist"])
      await ctx.send("{} was removed from the whitelist".format(args))
    else:
      print(db["whitelist"])
      print("{} is not on the whitelist".format(args))
      await ctx.send("{} is not on the whitelist".format(args))

#Events
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(Message):
  await bot.process_commands(Message)
  
  if Message.author == bot.user:
    return

  # if Message.content.startswith("-"):
  #   return

  # if "whitelist" in db.keys() and str(Message.author.id) in db["whitelist"]:
  #   print("User whitelisted, ignoring message")
  #   return

  if responding:
    print("looking for bad joke")
    if str(Message.author.id) in wlist:
        print("User whitelisted, ignoring message")
    elif any(word in Message.content for word in jokes):
      print("BAD JOKE DETECTED!")
      await Message.channel.send(Message.author.mention + " BAD JOKE DETECTED!\n{}".format(random.choice(responses)))
    else:
      print("No bad joke detected")

  
  
  
keep_alive()
bot.run(os.getenv('TOKEN'))