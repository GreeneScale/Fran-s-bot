import os

import discord

import webscraping

import csv

from discord.ext import commands, tasks

from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord.')
    

@bot.command(name='setup', help='Call this command in the channel that you want your updates to be posted into.')
async def setup(ctx, interval: int = commands.parameter(default=24, description="the bot will check the websites every ___ hours")):
    my_task.change_interval(seconds=interval)
    my_task.start(ctx.channel)


@bot.command(name='addpage', help='Call this command to add a new page to the checked pages.')
async def addpage(ctx, page: str = commands.parameter(description="provide the link to the page you want checked")):
    with open ('activewebsites.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
        allwebsites = []
        for row in reader:
            allwebsites = allwebsites + row
    allwebsites.append(page)
    with open('activewebsites.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(allwebsites)
    await ctx.channel.send("|" + page + "| successfully added!")


@bot.command(name='showpages', help='Call this command to see a list of all currently checked pages')
async def showpages(ctx):
    with open ('activewebsites.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
        allwebsites = []
        for row in reader:
            allwebsites = allwebsites + row
    await ctx.channel.send(allwebsites)


@bot.command(name='removepage', help='Call this command to delete a page from the checked pages')
async def removepage(ctx, page: str = commands.parameter(description="provide the full link to the page you want to remove")):
    with open ('activewebsites.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
        allwebsites = []
        something_removed = False
        for row in reader:
            for link in row:
                if page != link:
                    allwebsites.append(link)
                elif page == link:
                    something_removed = True
    with open('activewebsites.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(allwebsites)
    if something_removed:
        await ctx.channel.send("|"+ page + "| successfully removed!")
    else:
        await ctx.channel.send("Unable to find |" + page +"| in checked pages")

# @bot.event
# async def on_message(message):
#     if message.author == bot.user.name:
#         return
#     test_string = "helllllooooooooo night city!"
#     if message.content == 'cyberpunk':
#         response = test_string
#         await message.channel.send(response)


def prettyWebsiteList(websiteList):
    pretty_string = "NEW CHAPTERS:\n"
    for website in websiteList:
        pretty_string += website + "\n"
    return pretty_string
        
def readAllWebsitesChapters():
    websiteChapterNumbers = {}
    with open('websiteswithchapters.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
        for row in reader:
            if len(row) == 2:
                websiteChapterNumbers[row[0]] = row[1]
            elif len(row) == 1:
                websiteChapterNumbers[row[0]] = 0
    return websiteChapterNumbers

def writeWebsiteChapterNumbers(websiteChapterNumbers):
    with open('websiteswithchapters.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key in websiteChapterNumbers.keys():
            print([key, websiteChapterNumbers[key]])
            writer.writerow([key, websiteChapterNumbers[key]])
        

async def checkForNewContent(allwebsites):
    priorWebsiteChapterNumbers = readAllWebsitesChapters()
    currentWebsiteChapterNumbers = await webscraping.getWebsiteChapterNums(allwebsites)
    websitesWithNewChapters = []

    for website in allwebsites:
        print(str(priorWebsiteChapterNumbers[website])+ " vs " + str(currentWebsiteChapterNumbers[website]) )
        if int(priorWebsiteChapterNumbers[website]) != int(currentWebsiteChapterNumbers[website]):
            websitesWithNewChapters.append(website)
            priorWebsiteChapterNumbers[website] = int(currentWebsiteChapterNumbers[website])
        else:
            priorWebsiteChapterNumbers[website] = currentWebsiteChapterNumbers[website]
    writeWebsiteChapterNumbers(priorWebsiteChapterNumbers)
    return websitesWithNewChapters


@tasks.loop()
async def my_task(target_channel_name):
    for channel in bot.guilds[0].channels:
        if str(channel.name) == str(target_channel_name):
            target_channel = channel
            break
    with open ('activewebsites.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
        allwebsites = []
        for row in reader:
            allwebsites = allwebsites + row

    websites_with_new_chapters = await checkForNewContent(allwebsites)
    
    results_message = prettyWebsiteList(websites_with_new_chapters)
    await target_channel.send(results_message)

bot.run(TOKEN)