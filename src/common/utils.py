import discord
from discord.channel import CategoryChannel, TextChannel, VoiceChannel
from .error import all_error_types


def find_category(channels, category_name):
    for item in channels:
        if type(item) is CategoryChannel and \
                str(item).lower() == category_name:
            return item.channels
    return None


def list_categories(channels):
    categories = []
    for item in channels:
        if type(item) is CategoryChannel and str(item) != 'Personal':
            categories.append(item)
    return categories


def get_channel_type(channel):
    if type(channel) is TextChannel:
        return "Text Channel"
    if type(channel) is VoiceChannel:
        return "Voice Channel"
    if type(channel) is CategoryChannel:
        return "Category Channel"


def create_simple_message(name, value, embed=None):
    if type(embed) != discord.Embed:
        embed = discord.Embed()
    return embed.add_field(name=name, value=value, inline=False)


def get_error_response(idx, embed=None):
    if idx >= len(all_error_types):
        return None
    item = all_error_types[idx]
    return create_simple_message(item['title'], item['msg'], embed)


def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def iterate_commands(content, commands, starts_with=True):
    for v, t in commands:
        if (starts_with and content.startswith(v)) or \
                (not starts_with and content == v):
            return t
    return None


def swap_items(items, idx1, idx2, error=None):
    if idx1 < len(items) and idx2 < len(items):
        temp = items[idx1]
        items[idx1] = items[idx2]
        items[idx2] = temp
    elif error:
        error()


def get_attribute(obj, items, default=None):
    for i in items:
        if obj is not None and i in obj:
            obj = obj[i]
        else:
            return default
    return obj
