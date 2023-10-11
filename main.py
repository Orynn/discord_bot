import asyncio
from typing import Optional

import discord
from DiscordDatabase import DiscordDatabase
from DiscordDatabase.database import Database
from discord import Message, Client, Intents, Activity, User, Reaction

DB_GUILD_ID = 610107266682585089
activity: Activity = discord.Activity(name="brûler des preuves", type=discord.ActivityType.playing)
intents: Intents = discord.Intents.all()

client: Client = discord.Client(activity=activity, intents=intents)

# Database
db = DiscordDatabase(client=client, guild_id=DB_GUILD_ID)
db_frames: Optional[Database] = None
db_users: Optional[Database] = None
db_reactions: Optional[Database] = None

# IDs
channel_rp: int = 1156848894555209738


@client.event
async def on_ready() -> None:
    """
    :return:
    """
    global db_frames, db_users
    db_frames = await db.new(category_name="DATABASE", channel_name="frame")
    db_users = await db.new(category_name="DATABASE", channel_name="users")
    db_reactions = await db.new(category_name="DATABASE", channel_name="reactions")
    log_channel = client.get_channel(715187364422483989)  # trash
    await log_channel.send("im online")


@client.event
async def on_message(message: Message) -> None:
    """
    :param message:
    :return:
    """

    global db_frames, db_users
    channel_sent: int = message.channel.id
    id_author: int = message.author.id
    id_bot: int = client.user.id
    msg: str = message.content

    if id_author == id_bot:
        if msg == "im online":
            await asyncio.sleep(5)
            await message.delete()
        elif msg == await db_frames.get(key="0"):
            await message.add_reaction("✅")
        return

    if channel_sent == channel_rp:
        if await db_users.get(key=str(id_author)):
            actual_frame = await db_users.get(key=str(id_author))
        else:
            actual_frame = "0"
            await db_users.set(key=str(id_author), value=actual_frame)
        await db_frames.get(key=actual_frame)
        if msg == "rp":
            await message.channel.send(await db_frames.get(key=actual_frame))
        await message.delete()


@client.event
async def on_reaction_add(reaction: Reaction, user: User) -> None:
    """
    :param reaction:
    :param user:
    :return:
    """
    global db_frames, db_reactions, db_users
    id_bot: int = client.user.id
    id_user: int = user.id

    if reaction.message.author.id == id_bot:
        if await db_users.get(key=str(id_user)) == "0":
            if reaction.emoji == "✅":
                await db_users.set(key=str(id_user), value="1")
                await reaction.message.remove_reaction(emoji="✅")


client.run(token="MzE4ODAwNjA4ODg0Njg2ODU5.G2II2E.t6y1gMWHa7oQCNIcSzpIDSxcYlSQXVpD2dh6Oc")
