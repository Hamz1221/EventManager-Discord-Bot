from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, ScheduledEvent, utils, Member, User, EventStatus
import logging

# Loading in the bot's discord token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Setting up bot intents
intents: Intents = Intents.default()
intents.members = True
intents.guild_scheduled_events = True
client: Client = Client(intents=intents)

role_prefix = "[EVENT] "
logger = logging.getLogger("discord")


# Detects when an event is created
@client.event
async def on_scheduled_event_create(event: ScheduledEvent) -> None:
    logger.info(f"event '{event.name}' created")

    guild = event.guild
    role_name = role_prefix + event.name
    role = utils.get(guild.roles, name=role_name)

    if role is None:
        role = await guild.create_role(name=role_name, mentionable=True)
        logger.info(f"Role '{role_name}' created for event '{event.name}'.")

        creator: User = event.creator

        if creator:
            member: Member = guild.get_member(creator.id) or await guild.fetch_member(creator.id)
            await member.add_roles(role)
            logger.info(
                f"Assigned role '{role.name}' to {member.display_name} for event '{event.name}'.")


# Detects when an event is deleted
@client.event
async def on_scheduled_event_delete(event: ScheduledEvent) -> None:
    logger.info(f"event '{event.name}' deleted")

    await purge_event_role(event)


async def purge_event_role(event: ScheduledEvent):
    guild = event.guild
    role_name = role_prefix + event.name
    logger.info(f"Purging event role '{role_name}'")
    role = utils.get(guild.roles, name=role_name)

    if role:
        for member in guild.members:
            if role in member.roles:
                await member.remove_roles(role)
                logger.info(f"Role '{role_name}' remove from {member.name}")

        await role.delete()
        logger.info(
            f"Role '{role_name}' deleted for deleted event '{event.name}'.")


# Detect when user marks as interested
@client.event
async def on_scheduled_event_user_add(event: ScheduledEvent, user: User) -> None:
    logger.info(f"{user.name} interested in '{event.name}' event")

    guild = event.guild
    member = guild.get_member(user.id) or await guild.fetch_member(user.id)
    role_name = role_prefix + event.name
    role = utils.get(event.guild.roles, name=role_name)

    if role:
        await member.add_roles(role)
        logger.info(
            f"Assigned role '{role.name}' to {user.display_name} for event '{event.name}'.")


# Detect when user unchecks being interested
@client.event
async def on_scheduled_event_user_remove(event: ScheduledEvent, user: User) -> None:
    logger.info(f"{user.name} no longer interested in '{event.name}' event")

    guild = event.guild
    member = guild.get_member(user.id) or await guild.fetch_member(user.id)
    role_name = role_prefix + event.name
    role = utils.get(event.guild.roles, name=role_name)

    if role:
        await member.remove_roles(role)
        logger.info(
            f"Removed role '{role.name}' from {user.display_name} for event '{event.name}'.")


# Detect when event is updated
@client.event
async def on_scheduled_event_update(before: ScheduledEvent, after: ScheduledEvent) -> None:
    logger.info(f"Event {before.name} updated")

    # Event name was changed
    if before.name != after.name:
        old_role_name = role_prefix + before.name
        new_role_name = role_prefix + after.name
        role = utils.get(after.guild.roles, name=old_role_name)
        await role.edit(name=new_role_name)
        logger.info(
            f"Changed event role name from '{role_prefix}{old_role_name}' to '{role_prefix}{new_role_name}'")

    # Event ended
    if after.status == EventStatus.completed:
        await purge_event_role(after)


# Bot startup
@client.event
async def on_ready() -> None:
    logger.info(f'{client.user} is now running!')


# Main entry point
def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
