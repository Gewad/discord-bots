import os
import re

import discord
from discord.ext import commands
from dotenv import load_dotenv

from gmovies.movies import movie_info

# Load environment variables from .env file
load_dotenv()

# Read the BOT_TOKEN from the environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# Read the guild and channel IDs from the environment variables
GUILD_ID = int(os.getenv("GUILD_ID") or "0")
CHANNEL_ID = int(os.getenv("CHANNEL_ID") or "0")

# Create a new Discord bot with the appropriate intents and cache settings
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    intents=intents, command_prefix="?", help_command=None, case_insensitive=True
)

# Define a regular expression pattern to match IMDB links or movie IDs
movie_pattern = r"(?:https?://)?(?:www\.)?imdb\.com/(?:title/)?(tt\d{7})/?"

# Ensure that the movies.txt file exists or create it if it doesn't
if not os.path.exists("movies.txt"):
    with open("movies.txt", "w") as file:
        pass


# Define a function to handle incoming messages
@bot.command(command_prefix="!", help="Submit a movie suggestion")  # type: ignore
async def submit(ctx: commands.context.Context, message: str):
    # Ignore messages from the bot itself to prevent an infinite loop
    if ctx.author == bot.user:
        return

    # Check if the message was sent in the specified channel on the specified guild
    if ctx.guild and ctx.guild.id == GUILD_ID and ctx.channel.id == CHANNEL_ID:
        print(f"{ctx.author} sent a message in {ctx.channel}: {message}")

        # Check if the message contains a valid movie suggestion
        match = re.search(movie_pattern, message)
        if match:
            # Extract the movie ID from the IMDB link or movie ID
            movie_id = match.group(1)

            # Check for available streaming services
            movie = movie_info(movie_id)
            if movie and movie.streaming_platforms:
                # TODO: Add suggestion to database

                # Send a confirmation message to the user
                await ctx.channel.send(
                    f"Thanks for the suggestion! I've added {movie_id} to my list of movies."
                )
            else:
                # Send an error message to the user
                await ctx.channel.send(
                    "Sorry, it looks like this movie is not available for streaming."
                )


# Define a function to set the guild and channel attributes once the bot is ready
@bot.event
async def on_ready():
    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{bot.guild.name} (id: {bot.guild.id})\n"
        f"Listening for messages in {bot.channel.name} (id: {bot.channel.id})"
    )


# Start the bot
bot.run(BOT_TOKEN)
