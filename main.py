from twitchio.ext import commands, pubsub
import twitchio
from twitchio.http import TwitchHTTP
from Library.twitchchatmaster.twitch_chat import *
import os 
import creds
import re
import requests
import settings
import threading
import random
import asyncio


class Bot(commands.Bot):
 
    conversations = {}
 
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
 
        super().__init__(token= creds.TWITCH_TOKEN, prefix='!', initial_channels=[creds.TWITCH_CHANNEL])
 
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as '+str(self.nick))
        
    def send_messages_to_chat(self, textresponse):
        #Send Messages to Chat?
        sendMessage = True
        my_chat = TwitchChat(oauth=creds.BOT_ACCOUNT_TWITCH_OAUTH, bot_name=creds.BOT_ACCOUNT_TWITCH_CHANNEL, channel_name=creds.SENDMESSAGE_TO_THIS_CHANNEL)
    
        if sendMessage:
            [my_chat.send_to_chat(textresponse)]
        
    def wordify(self, text, replacement_word, aLength):
        length = settings.wordlength
        if settings.wordlength < 0:
            length = len(replacement_word)

        words = text.split()
        suitable_words = [w for w in words if w != replacement_word and len(w) >= length]

        if suitable_words:
            word_to_change = random.choice(suitable_words)

            # Choose partial or full replacement
            if random.random() < 0.5:
                new_word = replacement_word
            else:
                max_start_index = max(0, len(word_to_change) - len(replacement_word))
                start_index = random.randint(0, max_start_index)
                new_word = word_to_change[:start_index] + replacement_word + word_to_change[start_index:]

            # Replace only the chosen word
            return text.replace(word_to_change, new_word, 1)  
        else:
            return False 


    async def event_message(self, message):
        theusername = message.author.name
        themessage = message.content
        if theusername == creds.BOT_ACCOUNT_TWITCH_CHANNEL:
            return
        print(f'{message.author.name}: {message.content}')
        if message.echo:
            return
        wordified = self.wordify(themessage, settings.wordify, settings.wordlength)
        if not wordified:
            return
        if random.random() < settings.chance:
            self.send_messages_to_chat(wordified)
        else:
            return

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
