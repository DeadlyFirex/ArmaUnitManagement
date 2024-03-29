#! /usr/bin/python
import discord
from discord.ext import commands, tasks
from loguru import logger

from typing import Union
from json import load

import services.reader as reader

from services.config import Config
from utilities.fetch import run, refresh


cfg: Config = Config("./config.json").config
meta: dict = load(open("data/meta.json", "r"))
privileged: list = cfg.bot.privileged + [cfg.bot.owner]

bot: discord.ext.commands.Bot = commands.Bot(command_prefix=cfg.bot.prefix,
                                             intents=discord.Intents.all(),
                                             tree_cls=discord.app_commands.CommandTree)

forms_amount: Union[int, None] = None

file_logger = logger.add(
    sink="logs/bot-main.log",
    level="TRACE",
    rotation="15MB",
    compression="zip"
)


async def send_form(ctx: commands.Context, response: dict):
    embed = discord.Embed(title="Go to the form",
                          url=f"https://docs.google.com/forms/d/{cfg.forms.form_id}/edit"
                              f"#response={response['responseId']}",
                          description="A new application was submitted through the form.")
    embed.set_author(name=f"Application No. {response['count'] + 1}",
                     icon_url=cfg.bot.icon)
    for key, value in response["answers"].items():
        embed.add_field(name=meta["items"][key]["titleShort"], value=value, inline=False)
    embed.set_footer(text="Link to report")
    await ctx.send(embed=embed)


@bot.check
async def basic_check(ctx: commands.Context):
    if ctx.author.id in privileged and ctx.guild.id == cfg.bot.guild:
        logger.info(f"Command used by {ctx.author.display_name} ({ctx.author.id}): {ctx.command}")
        return True
    else:
        logger.info(f"User {ctx.author.display_name} ({ctx.author.id}) tried to use {ctx.command}")
        await ctx.send("You are not allowed to use this command.", delete_after=3); await ctx.message.delete(delay=3)
        return False


@tasks.loop(seconds=cfg.forms.refresh)
async def get_responses():
    global forms_amount
    forms_amount = reader.read_number("./counter")

    _ = run()
    if _[3] is True:
        await bot.get_channel(cfg.bot.channel).send(f"<@{cfg.bot.owner}>\nRefresh required! Please use the "
                                                    f"`refresh_credentials` command.")
        await bot.close()
        exit(75)
    if _[2] > forms_amount:
        response = reader.get_latest_response()

        embed = discord.Embed(title="Go to the form",
                              url=f"https://docs.google.com/forms/d/14piHUZRPa9Bst_eua2MjnNGYuf1uPaSBSIfMWrDhdug/edit"
                                  f"#response={response['responseId']}",
                              description="A new application was submitted through the form.")
        embed.set_author(name=f"Application No. {forms_amount + 1}",
                         icon_url="https://cdn.discordapp.com/avatars/1081353276773118002"
                                  "/6eb986f976cd37e95d0320cb7bec7d21.webp?size=32")
        for key, value in response["answers"].items():
            embed.add_field(name=meta["items"][key]["titleShort"], value=value, inline=False)
        embed.set_footer(text="Link to report")
        await bot.get_channel(cfg.bot.channel).send(embed=embed)


@logger.catch()
@bot.event
async def on_ready():
    global forms_amount

    # Initialize the targeted user and guild
    forms_amount = reader.read_number("./counter")

    # Log the bot status
    logger.info(f"Logged on as {bot.user}")
    logger.info(f"Home guild: {bot.get_guild(cfg.bot.guild).name}")
    logger.info(f"Current amount: {forms_amount}")

    get_responses.start()
    await bot.tree.sync()
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="with forms"))


@bot.hybrid_command(with_app_command=True, name="ping", description="Returns a pong.")
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")


@bot.hybrid_command(with_app_command=True, name="get_response_by_id", description="Fetches a response by identifier")
async def get_response_by_id(ctx: commands.Context, identifier: str = None):
    if identifier is None:
        await ctx.send("Please provide a valid response.")
        return
    try:
        response = reader.get_response(identifier)
        await send_form(ctx, response)
    except IOError as e:
        logger.warning(e.__str__())
        await ctx.send("Please provide a valid response.")
        return


@bot.hybrid_command(with_app_command=True, name="get_response_by_count", description="Fetches a response by count")
async def get_response_by_count(ctx: commands.Context, number: int = 0):
    try:
        response = reader.get_response_by_count(number)
        await send_form(ctx, response)
    except (IOError, IndexError) as e:
        logger.warning(e.__str__())
        await ctx.send("Please provide a valid response.")
        return


@bot.hybrid_command(with_app_command=True, name="refresh_responses", description="Manually refreshes the response data")
async def refresh_responses(ctx: commands.Context):
    global forms_amount

    forms_amount = run()[2]
    logger.info(f"Refreshed forms. {forms_amount} responses found.")
    await ctx.send(f"Refreshed forms. {forms_amount} responses found.")


@bot.hybrid_command(with_app_command=True, name="refresh_credentials",
                    description="Manually refreshes the credentials used to retrieve data")
async def refresh_credentials(ctx: commands.Context):
    await ctx.send("Refreshing credentials manually, this will make the bot "
                   "unresponsive until you complete the process.")
    _ = refresh()
    logger.info(f"Refreshed credentials.")


@refresh_credentials.error
async def refresh_credentials_error(ctx: commands.Context, error: commands.CommandError):
    pass




logger.info("Booting up...")
bot.run(token=cfg.bot.token)
