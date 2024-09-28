#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the Discord bot.

Connecting, sending and receiving messages and doing custom actions.
"""

import re

import discord

from bot import Bot

class DiscordBot(discord.Client, Bot):
    """Bot implementing the discord protocol"""
    def __init__(self):
        Bot.__init__(self)
        self.CONFIG = {
            "token": ""
        }
        intents = discord.Intents.default()
        intents.message_content = True
        discord.Client.__init__(self, intents=intents)

    def begin(self):
        """Start the bot"""
        self.run(self.CONFIG.get("token"))

    async def checkMarvinActions(self, message):
        """Check if Marvin should perform any actions"""
        words = re.sub("[,.?:]", " ", message.content).strip().lower().split()
        if self.user.name.lower() in words:
            for action in self.ACTIONS:
                response = action(words)
                if response:
                    await message.channel.send(response)
        else:
            for action in self.GENERAL_ACTIONS:
                response = action(words)
                if response:
                    await message.channel.send(response)

    async def on_message(self, message):
        """Hook run on every message"""
        print(f"#{message.channel.name} <{message.author}> {message.content}")
        if message.author.name == self.user.name:
            # don't react to own messages
            return
        await self.checkMarvinActions(message)
