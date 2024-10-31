from typing import Final, List
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, ScheduledEvent, utils, Member, User, EventStatus

# Loading in the bot's discord token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Setting up bot intents
intents: Intents = Intents.default()
intents.members = True
intents.guild_scheduled_events = True
client: Client = Client(intents=intents)


# Detects when an event is created
@client.event
async def on_scheduled_event_create(event: ScheduledEvent) -> None:
    print(f"event '{event.name}' created")
    guild = event.guild
    role_name = "[EVENT] " + event.name
    role = utils.get(guild.roles, name=role_name)

    if role is None:
        role = await guild.create_role(name=role_name, mentionable=True)
        print(f"Role '{role_name}' created for event '{event.name}'.")

        creator: User = event.creator

        if creator:
            member: Member = guild.get_member(creator.id) or await guild.fetch_member(creator.id)
            await member.add_roles(role)
            print(
                f"Assigned role '{role.name}' to {member.display_name} for event '{event.name}'.")


# Detects when an event is deleted
@client.event
async def on_scheduled_event_delete(event: ScheduledEvent) -> None:
    print(f"event '{event.name}' deleted")
    await purge_event_role(event)


async def purge_event_role(event: ScheduledEvent):
    guild = event.guild
    role_name = "[EVENT] " + event.name
    print(f"Purging event role '{role_name}'")
    role = utils.get(guild.roles, name=role_name)

    if role:
        for member in guild.members:
            if role in member.roles:
                await member.remove_roles(role)
                print(f"Role '{role_name}' remove from {member.name}")

        await role.delete()
        print(f"Role '{role_name}' deleted for deleted event '{event.name}'.")


# Detect when user marks as interested
@client.event
async def on_scheduled_event_user_add(event: ScheduledEvent, user: User) -> None:
    print(f"{user.name} interested in '{event.name}' event")
    guild = event.guild
    member = guild.get_member(user.id) or await guild.fetch_member(user.id)
    role_name = "[EVENT] " + event.name
    role = utils.get(event.guild.roles, name=role_name)

    if role:
        await member.add_roles(role)
        print(
            f"Assigned role '{role.name}' to {user.display_name} for event '{event.name}'.")


# Detect when user unchecks being interested
@client.event
async def on_scheduled_event_user_remove(event: ScheduledEvent, user: User) -> None:
    print(f"{user.name} no longer interested in '{event.name}' event")
    guild = event.guild
    member = guild.get_member(user.id) or await guild.fetch_member(user.id)
    role_name = "[EVENT] " + event.name
    role = utils.get(event.guild.roles, name=role_name)

    if role:
        await member.remove_roles(role)
        print(
            f"Removed role '{role.name}' from {user.display_name} for event '{event.name}'.")


# Detect when event is updated
@client.event
async def on_scheduled_event_update(before: ScheduledEvent, after: ScheduledEvent) -> None:
    print(f"Event {before.name} updated")

    # Event name was changed
    if before.name != after.name:
        old_role_name = "[EVENT] " + before.name
        new_role_name = "[EVENT] " + after.name
        role = utils.get(after.guild.roles, name=old_role_name)
        await role.edit(name=new_role_name)
        print(
            f"Changed event role name from '[EVENT] {old_role_name}' to '[EVENT] {new_role_name}'")

    # Event ended
    if after.status == EventStatus.completed:
        await purge_event_role(after)


# Bot startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')


# Main entry point
def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
