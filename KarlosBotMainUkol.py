import smtplib
from email.message import EmailMessage
from email.utils import formatdate
from pprint import pprint
import os 
import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Tuple, Any, List
import anything

from dotenv import load_dotenv  

load_dotenv() 

SMTP_SERVER     = os.environ.get('SMTP_SERVER')
SENDER_EMAIL    = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

class Bot:
    qemails : List[str] = [] #hodně safe  
    qnames : List[str] = []
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name
    
    def TryNewSubscriber(self, qemails, qnames):
        if self.name not in qnames:
            qemails.append(self.email)
            qnames.append(self.name)
        else:
            qemails[qnames.index(self.name)] = self.email

        print(qemails[qnames.index(self.name)])
        print(qnames[qnames.index(self.name)])

 
    def SendEmail(EmailListMentions):
        SMTP = SMTP_SSL_wrapper()
        for i in range(len(EmailListMentions)):
            print("a")

@bot.event
async def on_message(message: discord.Message) -> None:  
    if message.content.startswith("@"):
        messWithMentions = message.content[1:]
        PeopleListMenations = messWithMentions.split(" ")
        await message.channel.send(PeopleListMenations)
        #botEmail = Bot()

@bot.command()
async def poll(ctx: commands.Context) -> None:
    #subscriber = Bot(, ctx.member)
    print("?? coe")
    #subscriber.TryNewSubscriber()
    #print(subscriber)

@bot.command()
async def unsubscribe(ctx: commands.Context, email: str) -> None:
    #subscriber = Bot(email)
    await ctx.channel.send("coe??")

class CommandsOnSubscribe:
    qemails : List[str] = [] #hodně safe  
    qnames : List[str] = []

    def __init__(self, email, name):
        self.email = email
        self.name = name

    @property
    def subscribe(self, qemails, qnames):
        if self.name not in qnames:
            qemails.append(self.email)
            qnames.append(self.name)
            alreadyin = False
        else:
            qemails[qnames.index(self.name)] = self.email
            alreadyin = True

        return alreadyin

class CommandsOnSubscribeConv(commands.MemberConverter):
    async def convert(self, ctx, argument: str):
        member = await super().convert(ctx, argument)
        return CommandsOnSubscribe(argument, member.name) #email, name

@bot.command()
async def subscribe(ctx, *, member: CommandsOnSubscribe):
    is_new = member.subscribe
    if is_new:
        await ctx.send("You were added to subscriber list!")
    else:
        await ctx.send("You are already in subscribe list, your email was potentially changed!")
    print("funguje ?")


class SMTP_SSL_wrapper:
    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.port = 465
        self.username = username
        self.password = password

    def send_email(self, recipient: str, subject: str, content: str) -> EmailMessage:
        email_msg = EmailMessage()
        email_msg.set_content(content)
        email_msg['From'] = self.username
        email_msg['To'] = recipient
        email_msg['Date'] = formatdate(localtime=True)
        email_msg['Subject'] = subject
        
        s = smtplib.SMTP_SSL(self.server, port=self.port)
        s.login(self.username, self.password)
        errors = s.send_message(email_msg)
        s.quit()

        if len(errors):
            print('Errors occured during sending:')
            pprint(errors)
        else:
            print("OK - message submitted for delivery. Later on some errors might occur, but we won't know.")

if __name__ == '__main__':
    smtp_interface = SMTP_SSL_wrapper(
        server=SMTP_SERVER,
        username=SENDER_EMAIL,
        password=SENDER_PASSWORD
    )


bot.run(TOKEN)
