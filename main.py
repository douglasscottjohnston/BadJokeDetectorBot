import discord
import discord.ext
from discord.ext import commands
import os
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-',intents=intents)

#Global variables
bad_jokes = ["your mom", "Your mom", "You're mom","you're mom", "ur mom", "Ur mom", "urmom", "your mum", "Your mum", "You're mum","you're mum", "ur mum", "Ur mum", "urmum", "69", "deez nuts", "dez nuts", "dz nuts", "deeznuts", "deznuts", "dznuts"]

responses = [
  "This article might help you: https://www.wikihow.com/Write-a-Good-Joke",
  "Your career in comedy is looking bleak",
  "He'll be here all week folks"
]

if "responding" not in db.keys():
  db["responding"] = True
  print("Bot is responding")

#Commands
@bot.command()
async def addJoke(ctx, message):
  print("command caught")
  if "jokes" in db.keys():
    jokes = db["jokes"]
    if message in jokes:
      await ctx.send(message + " is already in the list of bad jokes")
      return
    else:
      jokes.append(message)
      db["jokes"] = jokes
      print('The bad joke \"' + message + '\" has been added to the list of bad jokes')
    await ctx.send('The bad joke \"' + message + '\" has been added to the list of bad jokes')

  else:
    db["jokes"] = message
    print('The bad joke \"' + message + '\" has been added to the list of bad jokes')
    await ctx.send('The bad joke \"' + message + '\" has been added to the list of bad jokes')
  print(db.keys())
  print(db["jokes"])

@bot.command()
async def addResponse(ctx, message):
  if "responses" in db.keys():
    respond = db["responses"]
    if message in respond:
      await ctx.send(message + " is already in the list of responses")
      return
    else:
      respond.append(message)
    print('The resonse \"' + message + '\" has been added to the list of responses')
    await ctx.send('The resonse \"' + message + '\" has been added to the list of responses')

  else:
    db["responses"] = message
    print('The resonse \"' + message + '\" has been added to the list of responses')
    await ctx.send('The resonse \"' + message + '\" has been added to the list of responses')
  print(db.keys())
  print(db["responses"])

@bot.command()
async def clearJokes(ctx):
  db["jokes"].clear()
  print(db["jokes"])
  await ctx.send("Jokes cleared from memory")

@bot.command()
async def clearResponses(ctx):
  db["responses"].clear()
  print(db["responses"])
  await ctx.send("Responses cleared from memory")

@bot.command()
async def removeJoke(ctx, message):
  temp = db["jokes"]
  i = 0
  while i < len(temp):
    if(temp[i] == message):
      del temp[i]
      db["jokes"] = temp
    i += 1
  print(db["jokes"])
  await ctx.send(message + ' was removed from the list of bad jokes')

@bot.command()
async def removeResponse(ctx, message):
  temp = db["responses"]
  i = 0
  while i < len(temp):
    if(temp[i] == message):
      del temp[i]
      db["responses"] = temp
  i += 1
  print(db["responses"])
  await ctx.send(message + ' was removed from the list of bad jokes')

@bot.command()
async def listJokes(ctx):
  await ctx.send("Here's all the bad jokes in memory:\n{}".format(db["jokes"]))

@bot.command()
async def listResponses(ctx):
  await ctx.send("Here's all the responses in memory:\n{}".format(db["responses"]))

@bot.command()
async def responding(ctx, args):
  print("command detected")
  if args:
    db["responding"] = True
    await ctx.send("Responding is on")
  else:
    db["responding"] = False
    await ctx.send("Responding is off")

@bot.command()
async def whitelist(ctx, *args):
  if not args:
    if "whitelist" in db.keys():
      await ctx.send(db["whitelist"])
    else:
      await ctx.send("A whitelist has not been created")
  else:
    if "whitelist" in db.keys():
      wlist = db["whitelist"]
      if args in wlist:
        print(db["whitelist"])
        await ctx.send(args + " is already on the whitelist")
      else:
        wlist.append(args)
        print(db["whitelist"])
        await ctx.send(args + " is now on the whitelist")
    else:
      db["whitelist"] = args
      print(db["whitelist"])
      await ctx.send(args + " is now on the whitelist")

@bot.command()
async def unwhitelist(ctx, args):
  if "whitelist" in db.keys():
    wlist = db["whitelist"]
    if args in wlist:
      for i in range(len(wlist)):
        if(wlist[i] == args):
          del wlist[i]
      db["whitelist"] = wlist
      print(db["whitelist"])
      await ctx.send(args + " was removed from the whitelist")
    else:
      print(db["whitelist"])
      await ctx.send(args + " is not on the whitelist")
  else:
    await ctx.send("A whitelist has not been created")

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

  if db["responding"]:
    respond = responses
    joke = bad_jokes

    if "responses" in db.keys() and len(db["responses"]) > 0:
      for r in db["responses"]:
        if r not in respond:
          respond.append(r)
      print(respond)
      print("Added cached responses")

    if "jokes" in db.keys() and len(db["jokes"]) > 0:
      for j in db["jokes"]:
        if j not in respond:
          joke.append(j)
      print(joke)
      print("Added cached jokes")

    print("looking for bad joke")
    if any(word in Message.content for word in joke):
      if "whitelsit" in db.keys() and str(Message.author.id) in db["whitelist"]:
        print("User whitelistded, ignoring message")
        return
      print("BAD JOKE DETECTED!")
      await Message.channel.send(Message.author.mention + " BAD JOKE DETECTED!\n{}".format(random.choice(respond)))

  
  
  
keep_alive()
bot.run(os.getenv('TOKEN'))