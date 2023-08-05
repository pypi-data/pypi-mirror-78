from operator import attrgetter

from twitchbot import (
    Command,
    commands,
    CommandContext,
    Message, get_all_custom_commands,
    InvalidArgumentsError,
    get_command)


# @Command('list')
# async def cmd_list(msg: Message, *args):
#     for c in channels.values():
#         await msg.reply(
#             whisper=True,
#             msg=f'channel: {c.name}, viewers: {c.chatters.viewer_count}, is_mod: {c.is_mod}, is_live: {c.live}')


@Command('commands', context=CommandContext.BOTH, help='lists all commands')
async def cmd_commands(msg: Message, *args):
    custom_commands = ', '.join(map(attrgetter('name'), get_all_custom_commands(msg.channel_name)))
    global_commands = ', '.join(map(attrgetter('fullname'), commands.values()))

    await msg.reply(whisper=True, msg=f'GLOBAL: {global_commands}')
    if custom_commands:
        await msg.reply(whisper=True, msg=f'CUSTOM: {custom_commands}')


@Command(name='help', syntax='<command>', help='gets the help text for a command')
async def cmd_help(msg: Message, *args):
    if not args:
        raise InvalidArgumentsError(reason='missing required argument', cmd=cmd_help)

    cmd = get_command(args[0])
    if not cmd:
        raise InvalidArgumentsError(reason=f'command not found', cmd=cmd_help)

    await msg.reply(msg=f'help for {cmd.fullname} - syntax: {cmd.syntax} - help: {cmd.help}')
